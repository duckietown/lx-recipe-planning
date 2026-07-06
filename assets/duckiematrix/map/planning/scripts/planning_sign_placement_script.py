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

# Robot start position, in tile units (bottom-left of the map).
_ROBOT_X: float = 0.5
_ROBOT_Y: float = 0.5

# The duckiematrix sign_stop mesh renders half a tile up-right (+x, +y) of its
# frame. So we place the frame on the tile's origin corner (integer tile
# coords), which lands the visible sign on the tile center.
_SIGN_RENDER_OFFSET: float = 0.5


class PlanningSignPlacementScript(MatrixEntityBehavior):
    """Places a traffic sign at a randomly chosen driveable tile, facing the robot."""

    def __init__(self, matrix_key: str, world_key: str | None) -> None:
        super().__init__(matrix_key, world_key)
        # matrix_key looks like "map_0/sign_stop_3"; the last token is the index.
        sign_index = int(matrix_key.rsplit("_", 1)[-1])
        tile_i, tile_j = SIGN_POSITIONS[sign_index]
        # Frame on the tile origin corner; the mesh's +0.5 render offset then
        # lands the visible sign on the center of tile (tile_i, tile_j).
        self._x: float = float(tile_i)
        self._y: float = float(tile_j)
        # Face towards the robot start, computed from the sign's *rendered*
        # position (frame + render offset). The mesh's visible face points
        # opposite its yaw, so aim the yaw away from the robot.
        dx = (self._x + _SIGN_RENDER_OFFSET) - _ROBOT_X
        dy = (self._y + _SIGN_RENDER_OFFSET) - _ROBOT_Y
        self._yaw: float = math.atan2(dy, dx)

    def update(self, _: float) -> None:
        if self.state:
            self.state.x = self._x
            self.state.y = self._y
            self.state.yaw = self._yaw
            self.state.commit()
