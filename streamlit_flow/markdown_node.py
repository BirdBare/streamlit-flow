from __future__ import annotations

import typing

from .base_node import BaseNode
from .handle import Handle


class MarkdownNode(BaseNode):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        content: typing.Any,
        *,
        handles: list[Handle] = [],
        hidden: bool = False,
        draggable: bool = True,
        selectable: bool = False,
        deletable: bool = False,
        focusable: bool = True,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
    ):
        super().__init__(
            pos_x=pos_x,
            pos_y=pos_y,
            handles=handles,
            hidden=hidden,
            draggable=draggable,
            selectable=selectable,
            deletable=deletable,
            focusable=focusable,
            z_index=z_index,
            style=style,
        )
        self.content = content

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = super().as_dict()

        output_dict["data"]["content"] = self.content

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:
        instance = cls(
            pos_x=input_dict["position"]["x"],
            pos_y=input_dict["position"]["y"],
            content=input_dict["data"]["content"],
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
        return (
            f"StreamlitFlowMarkdownNode({self.id}, ({round(self.pos_x, 2)}, {round(self.pos_y, 2)}), '{self.content}')"
        )
