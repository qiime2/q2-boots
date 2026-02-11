# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import random

# Numpy recommends using at least 128 bits of entropy to seed its rng which is
# where this is gonna end up. This won't quite shake out like that given we are
# seeding Python's rng with something else but we are gonna try our best.
MIN_RECOMMENDED_NP_RNG_BITS = 128


def resample(ctx, table, sampling_depth, n, replacement, random_seed=None):
    rarefy_action = ctx.get_action('feature_table', 'rarefy')
    resampled_tables = []

    random.seed(random_seed)
    for _ in range(n):
        _random_seed = random.randrange(2**MIN_RECOMMENDED_NP_RNG_BITS)
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement,
                                         random_seed=_random_seed)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}
