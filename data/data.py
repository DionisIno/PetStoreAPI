from dataclasses import dataclass


@dataclass
class Pet:
    id_number: int = None
    name: str = None
    photoUrls: str = None
    status: str = None
    breed: str = None
