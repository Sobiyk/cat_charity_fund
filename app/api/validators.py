from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicates(name: str, session: AsyncSession) -> None:
    """ Корутина для проверки имени проекта на предмет уникальности """
    stmt = select(CharityProject).where(CharityProject.name == name)
    query = await session.execute(stmt)
    if query.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists_by_id(
    id: int, session: AsyncSession
) -> CharityProject:
    """ Корутина для проерки существования проекта по id """
    project = await charityproject_crud.get(id, session)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект с таким id не существует.'
        )
    return project


async def validate_update_project(
    db_obj: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession
) -> None:
    """ Корутина для валидации при обновлении проекта """
    if db_obj.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if obj_in.name is not None:
        await check_name_duplicates(obj_in.name, session)
    if obj_in.full_amount and obj_in.full_amount < db_obj.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Полная сумма проекта не может быть меньше уже собранной!'
        )
