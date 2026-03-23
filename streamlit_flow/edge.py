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
        source_marker: Marker | None = None,  # TODO
        target_marker: Marker | None = None,  # TODO
        hidden: bool = False,
        animated: bool = False,
        deletable: bool = True,
        focusable: bool = True,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
        label_style: dict[str, typing.Any] = {},
    ) -> None:

        self.id = uuid.uuid4()
        self.source_node = source_node
        self.source_handle = source_handle
        self.target_node = target_node
        self.target_handle = target_handle
        self.label = label
        self.type = type
        self.source_marker = source_marker
        self.target_marker = target_marker
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
            "id": str(self.id),
            "source": str(self.source_node.id),
            "sourceHandle": str(self.source_handle.id),
            "target": str(self.target_node.id),
            "targetHandle": str(self.target_handle.id),
            "label": self.label,
            "type": self.type,
            "markerStart": self.source_marker.as_dict() if self.source_marker is not None else {},
            "markerEnd": self.target_marker.as_dict() if self.target_marker is not None else {},
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
            source_node=input_dict["source"],
            source_handle=input_dict["sourceHandle"],
            target_node=input_dict["target"],
            target_handle=input_dict["targetHandle"],
            label=input_dict.get("label", ""),
            type=input_dict.get("type", "default"),
            source_marker=input_dict.get("markerStartId"),
            target_marker=input_dict.get("markerEndId"),
            hidden=input_dict.get("hidden", False),
            animated=input_dict.get("animated", False),
            deletable=input_dict.get("deletable", True),
            focusable=input_dict.get("focusable", True),
            z_index=input_dict.get("zIndex", 0),
            style=input_dict.get("style", {}),
            label_style=input_dict.get("labelStyle", {}),
        )

        if "id" in input_dict:
            instance.id = uuid.UUID(input_dict["id"])

        return instance

    def __repr__(self):
        return f"StreamlitFlowEdge({self.id}, {self.source_node.id}:{self.source_handle.id}->{self.target_node.id}:{self.target_handle.id}, '{self.label}')"
