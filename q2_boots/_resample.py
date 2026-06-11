# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import random

from rachis import Artifact
from rachis.plugin import (
    IContext, CaptureHolder, NP_RNG_SIZE, get_np_random_seed
)


def resample(ctx, table, sampling_depth, n, replacement, random_seed=None):
    rarefy_action = ctx.get_action('feature_table', 'rarefy')
    resampled_tables = []

    random_int = CaptureHolder.get_or_set(random_seed, get_np_random_seed)

    # Seed once at the start for deterministic sequence generation
    random.seed(random_int)
    for _ in range(n):
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}