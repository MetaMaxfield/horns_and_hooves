from dataclasses import dataclass


@dataclass(slots=True)
class ActivityEntity:
    id: int
    name: str
