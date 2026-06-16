"""Planning sign placement script.

Places each traffic sign at the center of a randomly chosen driveable tile,
rotated to face the robot's starting tile (0, 0).

Sign index is derived from the entity key (e.g. "map_0/sign_stop_3" → index 3).
Tile centers and yaw are in tile units / radians, matching `unit: tiles` in
frames.yaml.
"""

import math
import os
import sys

_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from planning_map_state import SIGN_POSITIONS  # noqa: E402

from packages.duckiematrix_engine.entities.matrix_entity import (  # noqa: E402
    MatrixEntityBehavior,
)

# Robot starts at center of tile (0, 0) in tile units.
_ROBOT_X: float = 0.5
_ROBOT_Y: float = 0.5


class PlanningSignPlacementScript(MatrixEntityBehavior):
    """Places a traffic sign at a randomly chosen driveable tile, facing the robot."""

    def __init__(self, matrix_key: str, world_key: str | None) -> None:
        super().__init__(matrix_key, world_key)
        # matrix_key looks like "map_0/sign_stop_3"; the last token is the index.
        sign_index = int(matrix_key.rsplit("_", 1)[-1])
        tile_i, tile_j = SIGN_POSITIONS[sign_index]
        # Place at tile center in tile units.
        self._x: float = tile_i + 0.5
        self._y: float = tile_j + 0.5
        # Rotate to face the robot start position.
        dx = _ROBOT_X - self._x
        dy = _ROBOT_Y - self._y
        self._yaw: float = math.atan2(dy, dx)

    def update(self, _: float) -> None:
        if self.state:
            self.state.x = self._x
            self.state.y = self._y
            self.state.yaw = self._yaw
            self.state.commit()
