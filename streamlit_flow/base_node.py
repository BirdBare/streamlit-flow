from __future__ import annotations

import contextlib
import typing
import uuid

from .handle import Handle


class BaseNode:
    subclass_registry: dict[str, type[typing.Self]] = {}

    def __init_subclass__(cls) -> None:
        BaseNode.subclass_registry[cls.__name__] = cls

    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        *,
        handles: set[Handle] = set(),
        hidden: bool = False,
        draggable: bool = False,
        selectable: bool = False,
        deletable: bool = False,
        focusable: bool = False,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
    ):

        self.id = uuid.uuid4()
        self.pos_x = pos_x
        self.pos_y = pos_y

        if handles == set():
            self.handles = typing.cast("set[Handle]", set())
        else:
            self.handles = handles

        self.hidden = hidden
        self.draggable = draggable
        self.selectable = selectable
        self.deletable = deletable
        self.focusable = focusable
        self.z_index = z_index

        if style == {}:
            self.style = {}
        else:
            self.style = style

        if "width" not in self.style:
            self.style["width"] = "auto"
        if "height" not in self.style:
            self.style["height"] = "auto"

        if type(self) is typing.Self:
            raise NotImplementedError("Cannot instantiate 'StreamlitFlowNode'. Base class.")

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": str(self.id),
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

    def update_from_dict(self, input_dict: dict[str, typing.Any]):
        with contextlib.suppress(KeyError):
            self.pos_x = input_dict["position"]["x"]
        with contextlib.suppress(KeyError):
            self.pos_y = input_dict["position"]["y"]
        with contextlib.suppress(KeyError):
            self.handles = typing.cast("set[Handle]", input_dict["data"]["handles"])
        with contextlib.suppress(KeyError):
            self.hidden = input_dict["hidden"]
        with contextlib.suppress(KeyError):
            self.draggable = input_dict["draggable"]
        with contextlib.suppress(KeyError):
            self.selectable = input_dict["selectable"]
        with contextlib.suppress(KeyError):
            self.deletable = input_dict["deletable"]
        with contextlib.suppress(KeyError):
            self.z_index = input_dict["zIndex"]
        with contextlib.suppress(KeyError):
            self.focusable = input_dict["focusable"]
        with contextlib.suppress(KeyError):
            self.style = input_dict["style"]

    def __repr__(self):
        return f"StreamlitFlowNode({self.id}, ({round(self.pos_x, 2)}, {round(self.pos_y, 2)}))"
