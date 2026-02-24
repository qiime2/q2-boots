# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import random

from .util import set_random_seed_if_needed, MIN_RECOMMENDED_NP_RNG_BITS

from rachis.core.type import CaptureHolder


def resample(ctx, table, sampling_depth, n, replacement,
             random_seed: CaptureHolder = None):
    rarefy_action = ctx.get_action('feature_table', 'rarefy')
    resampled_tables = []

    set_random_seed_if_needed(random_seed)

    random.seed(random_seed.value)
    for _ in range(n):
        _random_seed = random.randrange(2**MIN_RECOMMENDED_NP_RNG_BITS)
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement,
                                         random_seed=_random_seed)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}
