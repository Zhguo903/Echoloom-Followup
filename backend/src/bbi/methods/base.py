from dataclasses import dataclass


@dataclass(frozen=True)
class MethodSpec:
    calls: str
    visible_context: str
