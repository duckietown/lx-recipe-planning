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

# Tiles that must stay free of holes AND signs, so the planning query is always
# solvable:
#   - START_TILE: the robot's start tile.
#   - GOAL_TILE: the planning goal tile. This MUST match the goal used by the
#     planning agent (FriendlyPose(7.5 * tile_size, ...) -> tile (GRID-1, GRID-1)).
START_TILE: tuple[int, int] = (0, 0)
GOAL_TILE: tuple[int, int] = (_GRID - 1, _GRID - 1)
RESERVED_TILES: frozenset[tuple[int, int]] = frozenset({START_TILE, GOAL_TILE})

# Candidate tiles for holes: inner grid only (rows/cols 1–6), minus reserved.
_inner = [
    (i, j)
    for i in range(1, _GRID - 1)
    for j in range(1, _GRID - 1)
    if (i, j) not in RESERVED_TILES
]
random.shuffle(_inner)

HOLES: frozenset[tuple[int, int]] = frozenset(_inner[:_N_HOLES])

# Driveable tiles: full grid minus holes, minus reserved (start + goal) tiles.
_driveable = [
    (i, j)
    for i in range(_GRID)
    for j in range(_GRID)
    if (i, j) not in HOLES and (i, j) not in RESERVED_TILES
]
random.shuffle(_driveable)

SIGN_POSITIONS: list[tuple[int, int]] = _driveable[:_N_SIGNS]
