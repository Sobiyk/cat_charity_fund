from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.services.investments import check_for_projects_to_invest
from app.schemas.donation import (
    DonationCreate, DonationDBAdmin, DonationDBUser
)

router = APIRouter()


@router.get(
    '/my',
    response_model=list[DonationDBUser],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """ Эндпоинт для вывода всех пожертвований текущего пользователя """
    donations = await donation_crud.get_multi(session=session, user=user)
    return donations


@router.get(
    '/',
    response_model=list[DonationDBAdmin],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDBUser,
    response_model_exclude_none=True
)
async def create_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """ Эндпоинт для отправки пожертвования """
    donation = await donation_crud.create(obj_in, session, user)
    donation = await check_for_projects_to_invest(
        obj=donation, session=session
    )
    return donation
