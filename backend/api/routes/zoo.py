from fastapi import APIRouter, HTTPException

from api.deps import CurrentUser, SessionDep
from db.permissions import has_permission
from db.zoo import get_zoo, get_zoo_by_id, get_zoo_by_name
from models import Zoo
from schemas import ZooIn

router = APIRouter(prefix="/zoo", tags=["Zoo"])


@router.get("/")
async def read_all_zoo(session: SessionDep) -> list[Zoo]:
    return await get_zoo(session)


@router.get("/{zoo_id}")
async def read_zoo(zoo_id: int, session: SessionDep) -> Zoo:
    zoo = await get_zoo_by_id(zoo_id, session)
    if not zoo:
        raise HTTPException(status_code=404, detail="Zoo not found")
    return zoo


@router.get("/name/{zoo_name}")
async def read_zoo_by_name(zoo_name: str, session: SessionDep):
    zoo = await get_zoo_by_name(zoo_name, session)
    if not zoo:
        raise HTTPException(status_code=404, detail="Zoo not found")
    return zoo


@router.post("/")
async def create_zoo(
    body: ZooIn, session: SessionDep, current_user: CurrentUser
) -> Zoo:
    if not has_permission(current_user.role.permissions, "create_zoo"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    zoo = Zoo(**body.model_dump())  # type: ignore
    session.add(zoo)
    await session.commit()
    await session.refresh(zoo)
    return zoo


@router.put("/{zoo_id}")
async def update_zoo(
    zoo_id: int, zoo_updated: ZooIn, session: SessionDep, current_user: CurrentUser
) -> Zoo:
    if not has_permission(current_user.role.permissions, "update_zoo"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    zoo = await get_zoo_by_id(zoo_id, session)
    if not zoo:
        raise HTTPException(status_code=404, detail="Zoo not found")

    zoo.name = zoo_updated.name
    zoo.location = zoo_updated.location
    zoo.information = zoo_updated.information

    await session.commit()
    await session.refresh(zoo)
    return zoo


@router.delete("/{zoo_id}")
async def delete_zoo(zoo_id: int, session: SessionDep, current_user: CurrentUser):
    if not has_permission(current_user.role.permissions, "delete_zoo"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    zoo = await get_zoo_by_id(zoo_id, session)
    if not zoo:
        raise HTTPException(status_code=404, detail="Zoo not found")

    await session.delete(zoo)
    await session.commit()
    return {"message": "Zoo deleted"}
