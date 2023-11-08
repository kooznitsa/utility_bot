from dataclasses import dataclass, asdict


@dataclass
class UserCreate:
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

    def as_dict(self):
        return asdict(self)


@dataclass
class DistrictCreate:
    district: str

    def as_dict(self):
        return asdict(self)
