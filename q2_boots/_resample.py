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


def resample(ctx: IContext,
             table: Artifact,
             sampling_depth: int,
             n: int,
             replacement: bool,
             random_seed: CaptureHolder[int] = None) -> \
        tuple[dict[str, Artifact]]:
    rarefy_action = ctx.get_action('feature_table', 'rarefy')
    resampled_tables = []

    random_int = CaptureHolder.get_or_set(random_seed, get_np_random_seed)

    random.seed(random_int)
    for _ in range(n):
        _random_seed = random.randrange(NP_RNG_SIZE)
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement,
                                         random_seed=_random_seed)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}
