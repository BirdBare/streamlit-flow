from __future__ import annotations

import contextlib
import typing
import uuid


class BaseNode:
    subclass_registry: dict[str, type[typing.Self]] = {}

    def __init_subclass__(cls) -> None:
        BaseNode.subclass_registry[cls.__name__] = cls

    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        *,
        handle_ids: set[uuid.UUID] = set(),
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

        if handle_ids == set():
            self.handle_ids = set()
        else:
            self.handle_ids = handle_ids

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
        output_dict["data"]["handleIds"] = [str(handle_id) for handle_id in self.handle_ids]
        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            pos_x=input_dict.get("position", {}).get("x", 0),
            pos_y=input_dict.get("position", {}).get("y", 0),
            handle_ids={uuid.UUID(handle_id) for handle_id in input_dict.get("data", {}).get("handleIds", [])},
            hidden=input_dict.get("hidden", False),
            draggable=input_dict.get("draggable", False),
            selectable=input_dict.get("selectable", False),
            deletable=input_dict.get("deletable", False),
            z_index=input_dict.get("zIndex", False),
            focusable=input_dict.get("focusable", False),
            style=input_dict.get("style", {}),
        )

        if "id" in input_dict:
            instance.id = uuid.UUID(input_dict["id"])

        return instance

    def update_from_dict(self, input_dict: dict[str, typing.Any]):
        with contextlib.suppress(KeyError):
            self.pos_x = input_dict["position"]["x"]
        with contextlib.suppress(KeyError):
            self.pos_y = input_dict["position"]["y"]
        with contextlib.suppress(KeyError):
            self.handle_ids = {uuid.UUID(handle_id) for handle_id in input_dict["data"]["handleIds"]}
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
