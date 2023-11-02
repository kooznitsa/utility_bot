from dataclasses import dataclass


@dataclass
class UserCreate:
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


@dataclass
class DistrictCreate:
    district: str
