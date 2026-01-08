from typing import List, Optional
from sqlmodel import SQLModel
from pydantic import field_validator
import requests


class SpyCatBase(SQLModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class SpyCatCreate(SpyCatBase):
    @field_validator("breed")
    @classmethod
    def validate_breed(cls, v: str) -> str:
        try:
            response = requests.get("https://api.thecatapi.com/v1/breeds")
            if response.status_code == 200:
                breeds_data = response.json()
                valid_breeds = [b["name"] for b in breeds_data]

                if v not in valid_breeds:
                    raise ValueError(
                        f"Breed '{v}' is invalid. Check TheCatAPI for valid breeds."
                    )
        except requests.RequestException:
            pass

        return v


class SpyCatUpdate(SQLModel):
    salary: float


class SpyCatRead(SpyCatBase):
    id: int


class TargetBase(SQLModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_complete: bool = False


class TargetCreate(SQLModel):
    name: str
    country: str
    notes: Optional[str] = None


class TargetUpdate(SQLModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None


class TargetRead(TargetBase):
    id: int
    mission_id: Optional[int]


class MissionBase(SQLModel):
    is_complete: bool = False
    cat_id: Optional[int] = None


class MissionCreate(SQLModel):
    cat_id: Optional[int] = None
    targets: List[TargetCreate]


class MissionRead(MissionBase):
    id: int
    targets: List[TargetRead]
