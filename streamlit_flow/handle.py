from __future__ import annotations

import typing
import uuid


class Handle:
    def __init__(
        self,
        position: typing.Literal["top", "bottom", "left", "right"],
        *,
        is_source: bool = True,
        is_target: bool = True,
        style: dict[str, typing.Any] = {},
    ):
        self.id = str(uuid.uuid4())
        self.position = position
        self.is_source = is_source
        self.is_target = is_target
        self.valid_targets: set[typing.Self] = set()

        if style == {}:
            self.style = {}
        else:
            self.style = style

    def __eq__(self, value) -> bool:
        return self.id == value.id

    @typing.overload
    def add_valid_targets(self, *targets: typing.Self): ...

    @typing.overload
    def add_valid_targets(self, *targets: None): ...

    def add_valid_targets(self, *targets: typing.Self | None):
        if None in targets:
            self.valid_targets = set()

        else:
            for target in targets:
                if target is None:
                    continue

                self.valid_targets.add(target)

                if self not in target.valid_targets:
                    target.add_valid_targets(self)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": self.id,
            "position": self.position,
            "isConnectableStart": self.is_source,
            "isConnectableEnd": self.is_target,
            "validTargetIds": [handle.id for handle in self.valid_targets],
            "style": self.style,
        }

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            position=input_dict["position"],
            is_source=input_dict["isConnectableStart"],
            is_target=input_dict["isConnectableEnd"],
            style=input_dict["style"],
        )

        if "id" in input_dict:
            instance.id = input_dict["id"]

        return instance

    def __repr__(self):
        return f"StreamlitFlowHandle({self.id}, {self.position}, {self.is_source}, {self.is_target})"
