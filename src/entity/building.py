from dataclasses import dataclass


@dataclass(slots=True)
class BuildingEntity:
    id: int
    address: str
    latitude: float
    longitude: float
