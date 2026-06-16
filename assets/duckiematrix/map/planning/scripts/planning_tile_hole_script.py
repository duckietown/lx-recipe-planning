"""Planning tile hole script.

Moves a tile off-map if it was randomly chosen as a 'hole' by the shared
planning_map_state module.  Tiles that are not selected do nothing.
"""

import os
import sys

# Ensure the scripts directory is importable so planning_map_state can be
# found regardless of the working directory when duckiematrix loads scripts.
_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from planning_map_state import HOLES  # noqa: E402

from packages.duckiematrix_engine.entities.matrix_entity import (  # noqa: E402
    MatrixEntityBehavior,
)


class PlanningTileHoleScript(MatrixEntityBehavior):
    """Moves a randomly selected tile to an off-map position to create a hole."""

    def __init__(self, matrix_key: str, world_key: str | None) -> None:
        super().__init__(matrix_key, world_key)
        # matrix_key looks like "map_0/tile_3_4"; parse the i, j indices.
        name = matrix_key.rsplit("/", 1)[-1]   # "tile_3_4"
        _, i_str, j_str = name.split("_")
        self._is_hole: bool = (int(i_str), int(j_str)) in HOLES

    def update(self, _: float) -> None:
        if self._is_hole and self.state:
            self.state.x = -100.0
            self.state.y = -100.0
            self.state.commit()
