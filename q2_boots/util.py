# ----------------------------------------------------------------------------
# Copyright (c) 2026, Caporaso Lab (https://cap-lab.bio).
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import random

from rachis.core.type import CaptureHolder

# Numpy recommends using at least 128 bits of entropy to seed its rng which is
# where this is gonna end up. This won't quite shake out like that given we are
# seeding Python's rng with something else but we are gonna try our best.
MIN_RECOMMENDED_NP_RNG_BITS = 128


def set_random_seed_if_needed(random_seed: CaptureHolder):
    if random_seed.value is None:
        random_seed.set_value(random.randrange(2**MIN_RECOMMENDED_NP_RNG_BITS))
