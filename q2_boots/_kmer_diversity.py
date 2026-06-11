# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
from skbio import OrdinationResults
import qiime2

from rachis import Artifact, Visualization
from rachis.plugin import IContext, CaptureHolder, get_np_random_seed

from q2_boots._alpha import (_validate_alpha_metric, _get_alpha_metric_action,
                             _alpha_collection_from_tables)
from q2_boots._beta import (_validate_beta_metric, _get_beta_metric_action,
                            _beta_collection_from_tables)


def kmer_diversity(ctx, table, sequences, sampling_depth, metadata, n,
                   replacement, kmer_size=16, tfidf=False, max_df=1.0,
                   min_df=1, max_features=None, alpha_average_method='median',
                   beta_average_method='medoid', pc_dimensions=3,
                   color_by=None, norm='None',
                   alpha_metrics=None,
                   beta_metrics=None,
                   random_seed=None):
    random_int = CaptureHolder.get_or_set(random_seed, get_np_random_seed)
    resample_action = ctx.get_action('boots', 'resample')
    kmerize_action = ctx.get_action('kmerizer', 'seqs_to_kmers')
    alpha_average_action = ctx.get_action('boots', 'alpha_average')
    beta_average_action = ctx.get_action('boots', 'beta_average')
    pcoa_action = ctx.get_action('diversity', 'pcoa')
    scatter_action = ctx.get_action('vizard', 'scatterplot_2d')

    if alpha_metrics is None:
        alpha_metrics = ['pielou_e', 'observed_features', 'shannon']
    if beta_metrics is None:
        beta_metrics = ['braycurtis', 'jaccard']

    for alpha_metric in alpha_metrics:
        _validate_alpha_metric(alpha_metric, phylogeny=None)
    for beta_metric in beta_metrics:
        _validate_beta_metric(beta_metric, phylogeny=None)

    resampled_tables, = resample_action(table=table,
                                        sampling_depth=sampling_depth,
                                        n=n,
                                        replacement=replacement,
                                        random_seed=random_int)
    kmer_tables = {}
    for key, resampled_table in resampled_tables.items():
        kmer_table, = kmerize_action(
            sequences, resampled_table, kmer_size, tfidf, max_df, min_df,
            max_features, norm)
        kmer_tables[key] = kmer_table

    alpha_vectors = {}
    for alpha_metric in alpha_metrics:
        alpha_metric_action = _get_alpha_metric_action(
            ctx, alpha_metric, phylogeny=None)
        alpha_collection = _alpha_collection_from_tables(
            kmer_tables, alpha_metric_action)
        avg_alpha_vector, = alpha_average_action(
            alpha_collection, alpha_average_method)
        alpha_vectors[alpha_metric] = avg_alpha_vector
        import pandas as pd
        alpha_series = avg_alpha_vector.view(pd.Series)
        alpha_df = alpha_series.to_frame(name=alpha_metric)
        alpha_df.index.name = 'sample-id'
        alpha_metadata = qiime2.Metadata(alpha_df)
        metadata = alpha_metadata.merge(metadata)

    beta_dms = {}
    for beta_metric in beta_metrics:
        beta_metric_action = _get_beta_metric_action(
            ctx, beta_metric, phylogeny=None)
        beta_collection = _beta_collection_from_tables(
            kmer_tables, beta_metric_action)
        avg_beta_dm, = beta_average_action(
            beta_collection, beta_average_method)
        beta_dms[beta_metric] = avg_beta_dm

    pcoas = {}
    for key, dm in beta_dms.items():
        pcoa_results, = pcoa_action(dm)
        pcoas[key] = pcoa_results

    for pcoa, name in zip(pcoas.values(), beta_metrics):
        pc_result = pcoa.view(OrdinationResults)
        prop_explained = pc_result.proportion_explained[:pc_dimensions].values
        prop_explained = np.nan_to_num(prop_explained)
        pc_result = pcoa.view(qiime2.Metadata).to_dataframe().iloc[:, :pc_dimensions]
        pc_result.columns = ['{0} {1} ({2}%)'.format(name, c, int(p * 100)) for
                             c, p in zip(pc_result.columns, prop_explained)]
        metadata = qiime2.Metadata(pc_result).merge(metadata)

    scatter_plot, = scatter_action(metadata=metadata, color_by=color_by)

    return (resampled_tables, kmer_tables, alpha_vectors,
            beta_dms, pcoas, scatter_plot)
