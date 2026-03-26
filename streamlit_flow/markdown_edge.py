from __future__ import annotations

import typing
import uuid

from .base_edge import BaseEdge
from .base_node import BaseNode
from .handle import Handle
from .marker import Marker


class MarkdownEdge(BaseEdge):
    def __init__(
        self,
        source_node: BaseNode,
        source_handle: Handle,
        target_node: BaseNode,
        target_handle: Handle,
        markdown: typing.Any = "",
        *,
        line_type: typing.Literal["straight", "smoothstep", "simplebezier", "bezier"] = "simplebezier",
        source_marker: Marker | None = None,  # TODO
        target_marker: Marker | None = None,  # TODO
        hidden: bool = False,
        animated: bool = False,
        deletable: bool = True,
        focusable: bool = True,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
        markdown_style: dict[str, typing.Any] = {},
    ) -> None:

        super().__init__(
            source_node=source_node,
            source_handle=source_handle,
            target_node=target_node,
            target_handle=target_handle,
            line_type=line_type,
            source_marker=source_marker,
            target_marker=target_marker,
            hidden=hidden,
            animated=animated,
            deletable=deletable,
            focusable=focusable,
            z_index=z_index,
            style=style,
        )

        self.markdown = markdown

        if markdown_style == {}:
            self.markdown_style = {}
        else:
            self.markdown_style = markdown_style

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = super().as_dict()

        output_dict["data"]["markdown"] = self.markdown
        output_dict["data"]["markdownStyle"] = self.markdown_style

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:
        instance = cls(
            source_node=input_dict["source"],
            source_handle=input_dict["sourceHandle"],
            target_node=input_dict["target"],
            target_handle=input_dict["targetHandle"],
            markdown=input_dict.get("data", {}).get("markdown", ""),
            line_type=input_dict.get("data", {}).get("lineType", "simplebezier"),
            source_marker=input_dict.get("markerStartId"),
            target_marker=input_dict.get("markerEndId"),
            hidden=input_dict.get("hidden", False),
            animated=input_dict.get("animated", False),
            deletable=input_dict.get("deletable", True),
            focusable=input_dict.get("focusable", True),
            z_index=input_dict.get("zIndex", 0),
            style=input_dict.get("style", {}),
            markdown_style=input_dict.get("data", {}).get("markdownStyle", {}),
        )

        if "id" in input_dict:
            instance.id = uuid.UUID(input_dict["id"])

        return instance

    def __repr__(self):
        return f"StreamlitFlowEdge({self.id}, {self.source_node.id}:{self.source_handle.id}->{self.target_node.id}:{self.target_handle.id})"
