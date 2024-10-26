from __future__ import annotations

from typing import TYPE_CHECKING

from ...types.alignment import Alignment
from ..projectile import Projectile

if TYPE_CHECKING:
    from ...maps.tilemap import Tilemap
    from ..sprite import Sprite


class ShowSprite(Projectile):
    def __init__(
        self,
        px: float,
        py: float,
        sprite: Sprite,
        tilemap: Tilemap,
        layer: int = 0,
        dyn_id: int = 0,
    ):
        super().__init__(
            px, py, 0.0, 0.0, 0.0, Alignment.NEUTRAL, tilemap, "SpriteEffect"
        )

        self.layer = layer
        self.sprite: Sprite = sprite

    def update(self, elapsed_time: float):
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def draw_self(self, ox: float, oy: float, camera_name: str):
        if self.sprite is None:
            return

        self.sprite.draw_self(self.px - ox, self.py - oy, camera_name)
