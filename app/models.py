from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class SpyCat(SQLModel, table=True):
    __tablename__: str = "spy_cats" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    years_of_experience: int
    breed: str
    salary: float

    missions: List["Mission"] = Relationship(back_populates="cat")


class Mission(SQLModel, table=True):
    __tablename__ = "missions" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    cat_id: Optional[int] = Field(default=None, foreign_key="spy_cats.id")
    is_complete: bool = Field(default=False)

    cat: Optional[SpyCat] = Relationship(back_populates="missions")
    targets: List["Target"] = Relationship(
        back_populates="mission",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Target(SQLModel, table=True):
    __tablename__ = "targets" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    mission_id: Optional[int] = Field(default=None, foreign_key="missions.id")
    name: str
    country: str
    notes: Optional[str] = Field(default=None)
    is_complete: bool = Field(default=False)

    mission: Optional[Mission] = Relationship(back_populates="targets")
