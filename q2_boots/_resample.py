# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import random

from rachis import Artifact
from rachis.plugin import CaptureHolder, NP_RNG_SIZE, set_np_random_seed


def resample(ctx,
             table: Artifact,
             sampling_depth: int,
             n: int,
             replacement: bool,
             random_seed: CaptureHolder = None) -> tuple[dict[str, Artifact]]:
    rarefy_action = ctx.get_action('feature_table', 'rarefy')
    resampled_tables = []

    set_np_random_seed(random_seed)

    random.seed(random_seed.value)
    for _ in range(n):
        _random_seed = random.randrange(NP_RNG_SIZE)
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement,
                                         random_seed=_random_seed)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}
