# ----------------------------------------------------------------------------
# Copyright (c) 2024, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from random import Random

from rachis import Artifact
from rachis.plugin import (
    IContext, CaptureHolder, get_np_random_seed, NP_RNG_BITS
)


def resample(ctx: IContext,
             table: Artifact,
             sampling_depth: int,
             n: int,
             replacement: bool,
             random_seed: CaptureHolder[int] = None) -> \
        tuple[dict[str, Artifact]]:
    rarefy_action = ctx.get_action(
        'feature_table', 'rarefy', record_provenance=False
    )

    resampled_tables = []
    random_int = CaptureHolder.get_or_set(random_seed, get_np_random_seed)
    rng = Random(random_int)
    random_seeds = [rng.getrandbits(NP_RNG_BITS) for _ in range(n)]
    for _random_seed in random_seeds:
        resampled_table, = rarefy_action(table=table,
                                         sampling_depth=sampling_depth,
                                         with_replacement=replacement,
                                         random_seed=_random_seed)
        resampled_tables.append(resampled_table)

    return {f'resampled-table-{i}': t for i, t in enumerate(resampled_tables)}
