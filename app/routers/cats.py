from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..session import get_session
from ..models import SpyCat
from ..schemas import SpyCatCreate, SpyCatRead, SpyCatUpdate

router = APIRouter(prefix="/cats", tags=["Spy Cats"])


@router.get("/", response_model=List[SpyCatRead])
def list_spy_cats(session: Session = Depends(get_session)):
    return session.exec(select(SpyCat)).all()


@router.get("/{cat_id}", response_model=SpyCatRead)
def get_spy_cat(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.post("/", response_model=SpyCatRead, status_code=201)
def create_spy_cat(cat: SpyCatCreate, session: Session = Depends(get_session)):
    db_cat = SpyCat.model_validate(cat)
    session.add(db_cat)
    session.commit()
    session.refresh(db_cat)
    return db_cat


@router.delete("/{cat_id}", status_code=204)
def delete_spy_cat(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    session.delete(cat)
    session.commit()


@router.patch("/{cat_id}", response_model=SpyCatRead)
def update_spy_cat_salary(
    cat_id: int, cat_update: SpyCatUpdate, session: Session = Depends(get_session)
):
    cat = session.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = cat_update.salary
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat
