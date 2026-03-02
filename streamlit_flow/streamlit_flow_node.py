from __future__ import annotations

import typing
import uuid

from .streamlit_flow_handle import StreamlitFlowHandle


class StreamlitFlowNode:
    subclass_registry: dict[str, type[StreamlitFlowNode]] = {}

    def __init_subclass__(cls) -> None:
        StreamlitFlowNode.subclass_registry[cls.__name__] = cls

    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        *,
        handles: list[StreamlitFlowHandle] = [],
        hidden: bool = False,
        draggable: bool = False,
        selectable: bool = False,
        deletable: bool = False,
        focusable: bool = False,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
    ):

        self.id = str(uuid.uuid4())
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.handles = handles
        self.hidden = hidden
        self.draggable = draggable
        self.selectable = selectable
        self.deletable = deletable
        self.focusable = focusable
        self.z_index = z_index
        self.style = style

        if "width" not in self.style:
            self.style["width"] = "auto"
        if "height" not in self.style:
            self.style["height"] = "auto"

        if type(self) is typing.Self:
            raise NotImplementedError("Cannot instantiate 'StreamlitFlowNode'. Base class.")

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": self.id,
            "position": {"x": self.pos_x, "y": self.pos_y},
            "hidden": self.hidden,
            "draggable": self.draggable,
            "selectable": self.selectable,
            "deletable": self.deletable,
            "focusable": self.focusable,
            "zIndex": self.z_index,
            "style": self.style,
        }

        output_dict["type"] = type(self).__name__

        output_dict["data"] = {}
        output_dict["data"]["handles"] = [handle.as_dict() for handle in self.handles]
        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            pos_x=input_dict["position"]["x"],
            pos_y=input_dict["position"]["y"],
            handles=input_dict["data"]["handles"],
            hidden=input_dict["hidden"],
            draggable=input_dict["draggable"],
            selectable=input_dict["selectable"],
            deletable=input_dict["deletable"],
            z_index=input_dict["zIndex"],
            focusable=input_dict["focusable"],
            style=input_dict["style"],
        )

        if "id" in input_dict:
            instance.id = input_dict["id"]

        return instance

    def __repr__(self):
        return f"StreamlitFlowNode({self.id}, ({round(self.pos_x, 2)}, {round(self.pos_y, 2)}))"
