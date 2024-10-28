from typing import List, Optional, Union

from ...types.direction import Direction
from ...types.gate_color import GateColor
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ..dynamic import Dynamic
from .gate import Gate


class ColorGate(Gate):

    def __init__(
        self,
        px: float,
        py: float,
        name: str = "ColorGate",
        *,
        color: GateColor,
        tilemap=None,
        dyn_id: int = -1,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        graphic_state: GraphicState,
        facing_direction: Direction,
    ):
        super().__init__(
            px,
            py,
            name,
            tilemap=tilemap,
            dyn_id=dyn_id,
            tileset_name=tileset_name,
            image_name=image_name,
            sprite_name=sprite_name,
            graphic_state=graphic_state,
            facing_direction=facing_direction,
            bombable=False,
        )
        self.color = color
        self.type = ObjectType.COLOR_GATE

    def update(self, elapsed_time, float, target: Optional[Dynamic] = None):
        self.open = self.engine.gate_color == self.color
        super().update(elapsed_time, target)

    def on_interaction(self, target: Dynamic, nature: Nature):
        return False

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height, tilemap):
        gate = ColorGate(
            px=px,
            py=py,
            tileset_name=obj.get_string("tileset_name"),
            image_name=obj.get_string("tileset_name"),
            sprite_name=obj.get_string("sprite_name"),
            graphic_state=GraphicState[
                obj.get_string("graphic_state", "closed").upper()
            ],
            facing_direction=Direction[
                obj.get_string("facing_direction", "south").upper()
            ],
            color=GateColor[obj.get_string("color", "red").upper()],
            tilemap=tilemap,
            dyn_id=obj.object_id,
            name=obj.name,
        )

        return [gate]
