from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..session import get_session
from ..models import SpyCat, Mission, Target
from ..schemas import MissionCreate, MissionRead, TargetUpdate, TargetRead

router = APIRouter(tags=["Missions"])


def check_cat_availability(session: Session, cat_id: int):
    statement = select(Mission).where(
        Mission.cat_id == cat_id, Mission.is_complete == False
    )
    active_mission = session.exec(statement).first()
    if active_mission:
        raise HTTPException(
            status_code=400,
            detail=f"Cat {cat_id} is already assigned to active mission {active_mission.id}.",
        )


@router.get("/missions/", response_model=List[MissionRead])
def list_missions(session: Session = Depends(get_session)):
    return session.exec(select(Mission)).all()


@router.get("/missions/{mission_id}", response_model=MissionRead)
def get_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.post("/missions/", response_model=MissionRead, status_code=201)
def create_mission(mission_in: MissionCreate, session: Session = Depends(get_session)):
    if not (1 <= len(mission_in.targets) <= 3):
        raise HTTPException(status_code=400, detail="Mission must have 1-3 targets.")

    if mission_in.cat_id:
        cat = session.get(SpyCat, mission_in.cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        check_cat_availability(session, mission_in.cat_id)

    db_mission = Mission(cat_id=mission_in.cat_id)
    session.add(db_mission)
    session.flush()

    for target_data in mission_in.targets:
        db_target = Target.model_validate(target_data)
        db_target.mission_id = db_mission.id
        session.add(db_target)

    session.commit()
    session.refresh(db_mission)
    return db_mission


@router.post("/missions/{mission_id}/assign", response_model=MissionRead)
def assign_cat_to_mission(
    mission_id: int, cat_id: int, session: Session = Depends(get_session)
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = session.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    check_cat_availability(session, cat_id)

    mission.cat_id = cat_id
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@router.delete("/missions/{mission_id}", status_code=204)
def delete_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.cat_id:
        raise HTTPException(
            status_code=400, detail="Cannot delete mission assigned to a cat."
        )

    session.delete(mission)
    session.commit()


@router.patch("/targets/{target_id}", response_model=TargetRead)
def update_target(
    target_id: int, target_in: TargetUpdate, session: Session = Depends(get_session)
):
    target = session.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = session.get(Mission, target.mission_id)

    if not mission:
        raise HTTPException(
            status_code=404, detail="Mission associated with this target not found"
        )

    if target_in.notes is not None:
        if target.is_complete or mission.is_complete:
            raise HTTPException(
                status_code=400,
                detail="Cannot update notes: Target or Mission is completed.",
            )
        target.notes = target_in.notes

    if target_in.is_complete is not None:
        target.is_complete = target_in.is_complete

    session.add(target)
    session.commit()
    session.refresh(target)

    all_targets = session.exec(
        select(Target).where(Target.mission_id == mission.id)
    ).all()
    if all(t.is_complete for t in all_targets):
        mission.is_complete = True
        session.add(mission)
        session.commit()

    return target
