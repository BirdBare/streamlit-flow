from __future__ import annotations

import contextlib
import typing
import uuid

from .base_node import BaseNode


class MarkdownNode(BaseNode):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        content: typing.Any,
        *,
        handle_ids: set[uuid.UUID] = set(),
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
            handle_ids=handle_ids,
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
            pos_x=input_dict.get("position", {}).get("x", 0),
            pos_y=input_dict.get("position", {}).get("y", 0),
            content=input_dict.get("data", {}).get("content", ""),
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
        super().update_from_dict(input_dict)
        with contextlib.suppress(KeyError):
            self.content = input_dict["data"]["content"]

    def __repr__(self):
        return (
            f"StreamlitFlowMarkdownNode({self.id}, ({round(self.pos_x, 2)}, {round(self.pos_y, 2)}), '{self.content}')"
        )
