from __future__ import annotations

import contextlib
import typing
import uuid


class Marker:
    def __init__(
        self,
        type: typing.Literal["arrow", "arrowclosed"],
        *,
        color: str | None = None,
        stroke_width: int | None = None,
    ):
        self.id = uuid.uuid4()
        self.type = type
        self.color = color
        self.stroke_width = stroke_width

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": str(self.id),
            "type": self.type,
            "color": self.color,
            "strokeWidth": self.stroke_width,
        }

        return output_dict

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            type=input_dict.get("type", "arrow"),
            color=input_dict.get("color"),
            stroke_width=input_dict.get("strokeWidth"),
        )

        if "id" in input_dict:
            instance.id = uuid.UUID(input_dict["id"])

        return instance

    def update_from_dict(self, input_dict: dict[str, typing.Any]):
        with contextlib.suppress(KeyError):
            self.type = input_dict["type"]
        with contextlib.suppress(KeyError):
            self.color = input_dict["color"]
        with contextlib.suppress(KeyError):
            self.stroke_width = input_dict["strokeWidth"]

    def __repr__(self):
        return f"StreamlitFlowMarker({self.type}, {self.color}, {self.stroke_width})"
