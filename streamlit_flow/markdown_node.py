from __future__ import annotations

import contextlib
import typing

from .base_node import BaseNode
from .handle import Handle


class MarkdownNode(BaseNode):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        markdown: typing.Any,
        *,
        handles: set[Handle] = set(),
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
        self.markdown = markdown

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = super().as_dict()

        output_dict["data"]["markdown"] = self.markdown

        return output_dict

    def update_from_dict(self, input_dict: dict[str, typing.Any]):
        super().update_from_dict(input_dict)
        with contextlib.suppress(KeyError):
            self.markdown = input_dict["data"]["markdown"]

    def __repr__(self):
        return (
            f"StreamlitFlowMarkdownNode({self.id}, ({round(self.pos_x, 2)}, {round(self.pos_y, 2)}), '{self.markdown}')"
        )
