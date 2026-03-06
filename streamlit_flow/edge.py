from __future__ import annotations

import typing
import uuid

from .base_node import BaseNode
from .handle import Handle
from .marker import Marker


class Edge:
    def __init__(
        self,
        source_node: BaseNode,
        source_handle: Handle,
        target_node: BaseNode,
        target_handle: Handle,
        label: str = "",
        *,
        type: typing.Literal["default", "straight", "step", "smoothstep", "simplebezier"] = "default",
        marker_start: Marker | None = None,  # TODO
        marker_end: Marker | None = None,  # TODO
        hidden: bool = False,
        animated: bool = False,
        deletable: bool = True,
        focusable: bool = True,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
        label_style: dict[str, typing.Any] = {},
    ) -> None:

        assert source_handle in source_node.handles, "source_handle is not a valid handle for source_node"
        assert target_handle in target_node.handles, "source_handle is not a valid handle for source_node"

        self.id = str(uuid.uuid4())
        self.source_node = source_node
        self.source_handle = source_handle
        self.target_node = target_node
        self.target_handle = target_handle
        self.label = label
        self.type = type
        self.marker_start = marker_start
        self.marker_end = marker_end
        self.hidden = hidden
        self.animated = animated
        self.deletable = deletable
        self.focusable = focusable
        self.z_index = z_index

        if style == {}:
            self.style = {}
        else:
            self.style = style

        if label_style == {}:
            self.label_style = {}
        else:
            self.label_style = label_style

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": self.id,
            "source": self.source_node.id,
            "sourceHandle": self.source_handle.id,
            "target": self.target_node.id,
            "targetHandle": self.target_handle.id,
            "label": self.label,
            "type": self.type,
            "markerStart": {} if self.marker_start is None else self.marker_start.as_dict(),
            "markerEnd": {} if self.marker_end is None else self.marker_end.as_dict(),
            "hidden": self.hidden,
            "animated": self.animated,
            "deletable": self.deletable,
            "focusable": self.focusable,
            "zIndex": self.z_index,
            "style": self.style,
            "labelStyle": self.label_style,
        }

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:
        instance = cls(
            source_node=input_dict["source_node"],
            source_handle=input_dict["source_handle"],
            target_node=input_dict["target_node"],
            target_handle=input_dict["target_handle"],
            label=input_dict["label"],
            type=input_dict["type"],
            marker_start=input_dict["marker_start"],
            marker_end=input_dict["marker_end"],
            hidden=input_dict["hidden"],
            animated=input_dict["animated"],
            deletable=input_dict["deletable"],
            focusable=input_dict["focusable"],
            z_index=input_dict["zIndex"],
            style=input_dict["style"],
            label_style=input_dict["labelStyle"],
        )

        if "id" in input_dict:
            instance.id = input_dict["id"]

        return instance

    def __repr__(self):
        return f"StreamlitFlowEdge({self.id}, {self.source_node}:{self.source_handle}->{self.target_node}:{self.target_handle}, '{self.label}')"
