import gc
import logging
import os
from collections import defaultdict
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import zarr
from scipy.stats import norm
from tqdm.contrib.concurrent import thread_map

import gsMap.utils.jackknife as jk
from gsMap.config import SpatialLDSCConfig
from gsMap.utils.regression_read import _read_sumstats, _read_w_ld, _read_ref_ld_v2

logger = logging.getLogger('gsMap.spatial_ldsc')


# %%
def _coef_new(jknife):
    est_ = jknife.jknife_est[0, 0] / Nbar
    se_ = jknife.jknife_se[0, 0] / Nbar
    return est_, se_


def append_intercept(x):
    n_row = x.shape[0]
    intercept = np.ones((n_row, 1))
    x_new = np.concatenate((x, intercept), axis=1)
    return x_new


def filter_sumstats_by_chisq(sumstats, chisq_max):
    before_len = len(sumstats)
    if chisq_max is None:
        chisq_max = max(0.001 * sumstats.N.max(), 80)
        logger.info(f'No chi^2 threshold provided, using {chisq_max} as default')
    sumstats['chisq'] = sumstats.Z ** 2
    sumstats = sumstats[sumstats.chisq < chisq_max]
    after_len = len(sumstats)
    if after_len < before_len:
        logger.info(f'Removed {before_len - after_len} SNPs with chi^2 > {chisq_max} ({after_len} SNPs remain)')
    else:
        logger.info(f'No SNPs removed with chi^2 > {chisq_max} ({after_len} SNPs remain)')
    return sumstats


def aggregate(y, x, N, M, intercept=1):
    num = M * (np.mean(y) - intercept)
    denom = np.mean(np.multiply(x, N))
    return num / denom


def weights(ld, w_ld, N, M, hsq, intercept=1):
    M = float(M)
    hsq = np.clip(hsq, 0.0, 1.0)
    ld = np.maximum(ld, 1.0)
    w_ld = np.maximum(w_ld, 1.0)
    c = hsq * N / M
    het_w = 1.0 / (2 * np.square(intercept + np.multiply(c, ld)))
    oc_w = 1.0 / w_ld
    w = np.multiply(het_w, oc_w)
    return w


def jackknife_for_processmap(spot_id):
    # calculate the initial weight for each spot
    spot_spatial_annotation = spatial_annotation[:, spot_id]
    spot_x_tot_precomputed = spot_spatial_annotation + ref_ld_baseline_column_sum
    initial_w = (
        get_weight_optimized(sumstats, x_tot_precomputed=spot_x_tot_precomputed,
                             M_tot=10000, w_ld=w_ld_common_snp, intercept=1)
        .astype(np.float32)
        .reshape((-1, 1)))

    # apply the weight to baseline annotation, spatial annotation and CHISQ
    initial_w_scaled = initial_w / np.sum(initial_w)
    baseline_annotation_spot = baseline_annotation * initial_w_scaled
    spatial_annotation_spot = spot_spatial_annotation.reshape((-1, 1)) * initial_w_scaled
    CHISQ = sumstats.chisq.values.reshape((-1, 1))
    y = CHISQ * initial_w_scaled

    # run the jackknife
    x_focal = np.concatenate((spatial_annotation_spot,
                              baseline_annotation_spot), axis=1)
    try:
        jknife = jk.LstsqJackknifeFast(x_focal, y, n_blocks)
        # LinAlgError
    except np.linalg.LinAlgError as e:
        logger.warning(f'LinAlgError: {e}')
        return np.nan, np.nan
    return _coef_new(jknife)


# Updated function
def get_weight_optimized(sumstats, x_tot_precomputed, M_tot, w_ld, intercept=1):
    tot_agg = aggregate(sumstats.chisq, x_tot_precomputed, sumstats.N, M_tot, intercept)
    initial_w = weights(x_tot_precomputed, w_ld.LD_weights.values, sumstats.N.values, M_tot, tot_agg, intercept)
    initial_w = np.sqrt(initial_w)
    return initial_w


def _preprocess_sumstats(trait_name, sumstat_file_path, baseline_and_w_ld_common_snp: pd.Index, chisq_max=None):
    # Load the gwas summary statistics
    sumstats = _read_sumstats(fh=sumstat_file_path, alleles=False, dropna=False)
    sumstats.set_index('SNP', inplace=True)
    sumstats = sumstats.astype(np.float32)
    sumstats = filter_sumstats_by_chisq(sumstats, chisq_max)

    # NB: The intersection order is essential for keeping the same order of SNPs by its BP location
    common_snp = baseline_and_w_ld_common_snp.intersection(sumstats.index)
    if len(common_snp) < 200000:
        logger.warning(f'WARNING: number of SNPs less than 200k; for {trait_name} this is almost always bad.')

    sumstats = sumstats.loc[common_snp]

    # get the common index position of baseline_and_w_ld_common_snp for quick access
    sumstats['common_index_pos'] = pd.Index(baseline_and_w_ld_common_snp).get_indexer(sumstats.index)
    return sumstats


def _get_sumstats_from_sumstats_dict(sumstats_config_dict: dict, baseline_and_w_ld_common_snp: pd.Index,
                                     chisq_max=None):
    # first validate if all sumstats file exists
    logger.info('Validating sumstats files...')
    for trait_name, sumstat_file_path in sumstats_config_dict.items():
        if not os.path.exists(sumstat_file_path):
            raise FileNotFoundError(f'{sumstat_file_path} not found')
    # then load all sumstats
    sumstats_cleaned_dict = {}
    for trait_name, sumstat_file_path in sumstats_config_dict.items():
        sumstats_cleaned_dict[trait_name] = _preprocess_sumstats(trait_name, sumstat_file_path,
                                                                 baseline_and_w_ld_common_snp, chisq_max)
    logger.info('cleaned sumstats loaded')
    return sumstats_cleaned_dict


class S_LDSC_Boost_with_pre_calculate_SNP_Gene_weight_matrix:
    def __init__(self, config: SpatialLDSCConfig, common_snp_among_all_sumstats_pos):
        self.config = config
        mk_score = pd.read_feather(config.mkscore_feather_path).set_index('HUMAN_GENE_SYM')
        mk_score_genes = mk_score.index

        snp_gene_weight_adata = ad.read_h5ad(config.snp_gene_weight_adata_path)
        common_genes = mk_score_genes.intersection(snp_gene_weight_adata.var.index)
        common_snps = snp_gene_weight_adata.obs.index
        # self.snp_gene_weight_adata = snp_gene_weight_adata[common_snp_among_all_sumstats:, common_genes.to_list()]
        self.snp_gene_weight_matrix = snp_gene_weight_adata[common_snp_among_all_sumstats_pos, common_genes.to_list()].X
        self.mk_score_common = mk_score.loc[common_genes]

        # calculate the chunk number
        self.chunk_starts = list(range(0, self.mk_score_common.shape[1], self.config.spots_per_chunk_quick_mode))

    def fetch_ldscore_by_chunk(self, chunk_index):
        chunk_start = self.chunk_starts[chunk_index]
        mk_score_chunk = self.mk_score_common.iloc[:,
                         chunk_start:chunk_start + self.config.spots_per_chunk_quick_mode]
        ldscore_chunk = self.calculate_ldscore_use_SNP_Gene_weight_matrix_by_chunk(
            mk_score_chunk,
            drop_dummy_na=False,
        )

        spots_name = self.mk_score_common.columns[chunk_start:chunk_start + self.config.spots_per_chunk_quick_mode]
        return ldscore_chunk, spots_name

    def calculate_ldscore_use_SNP_Gene_weight_matrix_by_chunk(self,
                                                              mk_score_chunk,
                                                              drop_dummy_na=True,
                                                              ):

        if drop_dummy_na:
            ldscore_chr_chunk = self.snp_gene_weight_matrix[:, :-1] @ mk_score_chunk
        else:
            ldscore_chr_chunk = self.snp_gene_weight_matrix @ mk_score_chunk

        return ldscore_chr_chunk


def _get_sumstats_with_common_snp_from_sumstats_dict(sumstats_config_dict: dict, baseline_and_w_ld_common_snp: pd.Index,
                                                     chisq_max=None):
    # first validate if all sumstats file exists
    logger.info('Validating sumstats files...')
    for trait_name, sumstat_file_path in sumstats_config_dict.items():
        if not os.path.exists(sumstat_file_path):
            raise FileNotFoundError(f'{sumstat_file_path} not found')
    # then load all sumstats
    sumstats_cleaned_dict = {}
    for trait_name, sumstat_file_path in sumstats_config_dict.items():
        sumstats_cleaned_dict[trait_name] = _preprocess_sumstats(trait_name, sumstat_file_path,
                                                                 baseline_and_w_ld_common_snp, chisq_max)
    # get the common snps among all sumstats
    common_snp_among_all_sumstats = None
    for trait_name, sumstats in sumstats_cleaned_dict.items():
        if common_snp_among_all_sumstats is None:
            common_snp_among_all_sumstats = sumstats.index
        else:
            common_snp_among_all_sumstats = common_snp_among_all_sumstats.intersection(sumstats.index)

    # filter the common snps among all sumstats
    for trait_name, sumstats in sumstats_cleaned_dict.items():
        sumstats_cleaned_dict[trait_name] = sumstats.loc[common_snp_among_all_sumstats]

    logger.info(f'Common SNPs among all sumstats: {len(common_snp_among_all_sumstats)}')
    return sumstats_cleaned_dict, common_snp_among_all_sumstats


def run_spatial_ldsc(config: SpatialLDSCConfig):
    global spatial_annotation, baseline_annotation, n_blocks, Nbar, sumstats, ref_ld_baseline_column_sum, w_ld_common_snp
    # config
    n_blocks = config.n_blocks
    sample_name = config.sample_name

    print(f'------Running Spatial LDSC for {sample_name}...')
    # Load the regression weights
    w_ld = _read_w_ld(config.w_file)
    w_ld_cname = w_ld.columns[1]
    w_ld.set_index('SNP', inplace=True)

    ld_file_baseline = f'{config.ldscore_save_dir}/baseline/baseline.'

    ref_ld_baseline = _read_ref_ld_v2(ld_file_baseline)
    # n_annot_baseline = len(ref_ld_baseline.columns)
    # M_annot_baseline = _read_M_v2(ld_file_baseline, n_annot_baseline, config.not_M_5_50)

    # common snp between baseline and w_ld
    baseline_and_w_ld_common_snp = ref_ld_baseline.index.intersection(w_ld.index)
    baseline_and_w_ld_common_snp_pos = pd.Index(ref_ld_baseline.index).get_indexer(baseline_and_w_ld_common_snp)

    # Clean the sumstats
    sumstats_cleaned_dict, common_snp_among_all_sumstats = _get_sumstats_with_common_snp_from_sumstats_dict(
        config.sumstats_config_dict, baseline_and_w_ld_common_snp,
        chisq_max=config.chisq_max)
    common_snp_among_all_sumstats_pos = ref_ld_baseline.index.get_indexer(common_snp_among_all_sumstats)

    # insure the order is monotonic
    assert pd.Series(
        common_snp_among_all_sumstats_pos).is_monotonic_increasing, 'common_snp_among_all_sumstats_pos is not monotonic increasing'

    if len(common_snp_among_all_sumstats) < 200000:
        logger.warning(
            f'!!!!! WARNING: number of SNPs less than 200k; for {sample_name} this is almost always bad. Please check the sumstats files.')

    ref_ld_baseline = ref_ld_baseline.loc[common_snp_among_all_sumstats]
    w_ld = w_ld.loc[common_snp_among_all_sumstats]

    # load additional baseline annotations
    if config.use_additional_baseline_annotation:
        print('Using additional baseline annotations')
        ld_file_baseline_additional = f'{config.ldscore_save_dir}/additional_baseline/baseline.'
        ref_ld_baseline_additional = _read_ref_ld_v2(ld_file_baseline_additional)
        n_annot_baseline_additional = len(ref_ld_baseline_additional.columns)
        logger.info(f'{len(ref_ld_baseline_additional.columns)} additional baseline annotations loaded')
        # M_annot_baseline_additional = _read_M_v2(ld_file_baseline_additional, n_annot_baseline_additional,
        #                                             config.not_M_5_50)
        ref_ld_baseline_additional = ref_ld_baseline_additional.loc[common_snp_among_all_sumstats]
        ref_ld_baseline = pd.concat([ref_ld_baseline, ref_ld_baseline_additional], axis=1)
        del ref_ld_baseline_additional

    # Detect available chunk files
    if config.ldscore_save_format == 'quick_mode':
        s_ldsc = S_LDSC_Boost_with_pre_calculate_SNP_Gene_weight_matrix(config, common_snp_among_all_sumstats_pos)
        total_chunk_number_found = len(s_ldsc.chunk_starts)
        print(f'Split data into {total_chunk_number_found} chunks')
    else:
        all_file = os.listdir(config.ldscore_save_dir)
        total_chunk_number_found = sum('chunk' in name for name in all_file)
        print(f'Find {total_chunk_number_found} chunked files in {config.ldscore_save_dir}')

    if config.all_chunk is None:
        if config.chunk_range is not None:
            assert config.chunk_range[0] >= 1 and config.chunk_range[
                1] <= total_chunk_number_found, 'Chunk range out of bound. It should be in [1, all_chunk]'
            print(
                f'chunk range provided, using chunked files from {config.chunk_range[0]} to {config.chunk_range[1]}')
            start_chunk, end_chunk = config.chunk_range
        else:
            start_chunk, end_chunk = 1, total_chunk_number_found
    else:
        all_chunk = config.all_chunk
        print(f'using {all_chunk} chunked files by provided argument')
        print(f'\t')
        print(f'Input {all_chunk} chunked files')
        start_chunk, end_chunk = 1, all_chunk

    running_chunk_number = end_chunk - start_chunk + 1

    # Process each chunk
    output_dict = defaultdict(list)
    zarr_path = Path(config.ldscore_save_dir) / f'{config.sample_name}.ldscore.zarr'
    if config.ldscore_save_format == 'zarr':
        assert zarr_path.exists(), f'{zarr_path} not found, which is required for zarr format'
        zarr_file = zarr.open(str(zarr_path))
        spots_name = zarr_file.attrs['spot_names']

    for chunk_index in range(start_chunk, end_chunk + 1):
        if config.ldscore_save_format == 'feather':
            ref_ld_spatial, spatial_annotation_cnames = load_ldscore_chunk_from_feather(chunk_index,
                                                                                        common_snp_among_all_sumstats_pos,
                                                                                        config,
                                                                                        )
        elif config.ldscore_save_format == 'zarr':
            ref_ld_spatial = zarr_file.blocks[:, chunk_index - 1][common_snp_among_all_sumstats_pos]
            start_spot = (chunk_index - 1) * zarr_file.chunks[1]
            ref_ld_spatial = ref_ld_spatial.astype(np.float32, copy=False)
            spatial_annotation_cnames = spots_name[start_spot:start_spot + zarr_file.chunks[1]]
        elif config.ldscore_save_format == 'quick_mode':
            ref_ld_spatial, spatial_annotation_cnames = s_ldsc.fetch_ldscore_by_chunk(chunk_index - 1)
        else:
            raise ValueError(f'Invalid ld score save format: {config.ldscore_save_format}')

        # get the x_tot_precomputed matrix by adding baseline and spatial annotation
        ref_ld_baseline_column_sum = ref_ld_baseline.sum(axis=1).values
        # x_tot_precomputed = ref_ld_spatial + ref_ld_baseline_column_sum

        for trait_name, sumstats in sumstats_cleaned_dict.items():

            spatial_annotation = ref_ld_spatial.astype(np.float32, copy=False)
            baseline_annotation = ref_ld_baseline.copy().astype(np.float32, copy=False)
            w_ld_common_snp = w_ld.astype(np.float32, copy=False)

            # weight the baseline annotation by N
            baseline_annotation = baseline_annotation * sumstats.N.values.reshape((-1, 1)) / sumstats.N.mean()
            # append intercept
            baseline_annotation = append_intercept(baseline_annotation)

            # Run the jackknife
            Nbar = sumstats.N.mean()
            chunk_size = spatial_annotation.shape[1]
            out_chunk = thread_map(jackknife_for_processmap, range(chunk_size),
                                   max_workers=config.num_processes,
                                   chunksize=10,
                                   desc=f'Chunk-{chunk_index}/Total-chunk-{running_chunk_number} for {trait_name}',
                                   )

            # cache the results
            out_chunk = pd.DataFrame.from_records(out_chunk,
                                                  columns=['beta', 'se', ],
                                                  index=spatial_annotation_cnames)
            # get the spots with nan
            nan_spots = out_chunk[out_chunk.isna().any(axis=1)].index
            if len(nan_spots) > 0:
                logger.info(f'Nan spots: {nan_spots} in chunk-{chunk_index} for {trait_name}. They are removed.')
            # drop the nan
            out_chunk = out_chunk.dropna()

            out_chunk['z'] = out_chunk.beta / out_chunk.se
            out_chunk['p'] = norm.sf(out_chunk['z'])
            output_dict[trait_name].append(out_chunk)

        del ref_ld_spatial, spatial_annotation, baseline_annotation, w_ld_common_snp
        gc.collect()

    # Save the results
    out_dir = config.ldsc_save_dir
    for trait_name, out_chunk_list in output_dict.items():
        out_all = pd.concat(out_chunk_list, axis=0)
        if running_chunk_number == total_chunk_number_found:
            out_file_name = out_dir / f'{sample_name}_{trait_name}.csv.gz'
        else:
            out_file_name = out_dir / f'{sample_name}_{trait_name}_chunk{start_chunk}-{end_chunk}.csv.gz'
        out_all['spot'] = out_all.index
        out_all = out_all[['spot', 'beta', 'se', 'z', 'p']]
        out_all.to_csv(out_file_name, compression='gzip', index=False)

        logger.info(f'Output saved to {out_file_name} for {trait_name}')
    logger.info(f'------Spatial LDSC for {sample_name} finished!')


def load_ldscore_chunk_from_feather(chunk_index, common_snp_among_all_sumstats_pos, config, ):
    # Load the spatial annotations for this chunk
    sample_name = config.sample_name
    ld_file_spatial = f'{config.ldscore_save_dir}/{sample_name}_chunk{chunk_index}/{sample_name}.'
    ref_ld_spatial = _read_ref_ld_v2(ld_file_spatial)
    ref_ld_spatial = ref_ld_spatial.iloc[common_snp_among_all_sumstats_pos]
    ref_ld_spatial = ref_ld_spatial.astype(np.float32, copy=False)

    spatial_annotation_cnames = ref_ld_spatial.columns
    return ref_ld_spatial.values, spatial_annotation_cnames
