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
        valid_targets: set[Handle] = set(),
        style: dict[str, typing.Any] = {},
    ):
        self.id = uuid.uuid4()
        self.position = position
        self.is_source = is_source
        self.is_target = is_target

        if valid_targets == set():
            self.valid_targets = set()
        else:
            self.valid_targets = valid_targets

        if style == {}:
            self.style = {}
        else:
            self.style = style

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    @typing.overload
    def add_valid_targets(self, *targets: Handle): ...

    @typing.overload
    def add_valid_targets(self, *targets: None): ...

    def add_valid_targets(self, *targets: Handle | None):
        if None in targets:
            self.valid_targets = set()

        else:
            for target in targets:
                if target is None:
                    continue

                self.valid_targets.add(target)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": str(self.id),
            "position": self.position,
            "isConnectableStart": self.is_source,
            "isConnectableEnd": self.is_target,
            "validTargetIds": [str(valid_target.id) for valid_target in self.valid_targets],
            "style": self.style,
        }

        return output_dict

    def __repr__(self):
        return f"StreamlitFlowHandle({self.id}, {self.position}, {self.is_source}, {self.is_target})"
