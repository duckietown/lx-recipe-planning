"""Shared random map state for the planning map.

Computed once at module import time (Python caches modules, so both
planning_tile_hole_script and planning_sign_placement_script will import
this exact module instance and see the same HOLES / SIGN_POSITIONS).

No fixed seed — Python's random is time-seeded by default, so the layout
differs on every map launch.
"""

import random

_GRID: int = 8
_N_HOLES: int = 10
_N_SIGNS: int = 8

# Candidate tiles for holes: inner grid only (rows/cols 1–6).
_inner = [(i, j) for i in range(1, _GRID - 1) for j in range(1, _GRID - 1)]
random.shuffle(_inner)

HOLES: frozenset[tuple[int, int]] = frozenset(map(tuple, _inner[:_N_HOLES]))

# Driveable tiles: full grid minus holes, minus vehicle start tile (0, 0).
_driveable = [
    (i, j)
    for i in range(_GRID)
    for j in range(_GRID)
    if (i, j) not in HOLES and (i, j) != (0, 0)
]
random.shuffle(_driveable)

SIGN_POSITIONS: list[tuple[int, int]] = _driveable[:_N_SIGNS]
