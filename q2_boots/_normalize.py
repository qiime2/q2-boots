# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import biom
import random


def _bootstrap_iteration(table: biom.Table, sampling_depth: int) -> biom.Table:
    table = table.filter(lambda v, i, m: v.sum() >= sampling_depth,
                         inplace=False, axis='sample')

    table = table.subsample(sampling_depth, axis='sample', by_id=False,
                            with_replacement=True)

    if table.is_empty():
        return ValueError('The output table contains no samples or features.'
                          'Verify your table is valid and that you provided a '
                          'shallow enough samplign depth')

    return table


def resample(ctx, table, sampling_depth, n=1, with_replacement=True,
             random_seed=None):

    if random_seed is not None:
        random.seed(random_seed)

    _iteration = ctx.get_action('feature_table', 'rarefy')

    tables = []

    for i in range(n):
        tables.append(_iteration(table=table, sampling_depth=sampling_depth,
                                 with_replacement=with_replacement)[0])

    return tables
