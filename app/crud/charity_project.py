from sqlalchemy import select
from sqlalchemy.sql import extract
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        select_stmt = select(CharityProject).where(
            CharityProject.fully_invested == True # noqa
        ).order_by((extract(
            'year', CharityProject.close_date)) - (
                extract('year', CharityProject.create_date))
        ).order_by((extract(
            'month', CharityProject.close_date)) - (
                extract('month', CharityProject.create_date))
        ).order_by((extract(
            'day', CharityProject.close_date)) - (
                extract('day', CharityProject.create_date))
        ).order_by((extract(
            'hour', CharityProject.close_date)) - (
                extract('hour', CharityProject.create_date))
        ).order_by((extract(
            'minute', CharityProject.close_date)) - (
                extract('minute', CharityProject.create_date))
        ).order_by((extract(
            'second', CharityProject.close_date)) - (
                extract('second', CharityProject.create_date))
        ).order_by((extract(
            'microseconds', CharityProject.close_date)) - (
                extract('microseconds', CharityProject.create_date))
        )
        projects_by_comp_rate = await session.execute(select_stmt)
        projects_by_comp_rate = projects_by_comp_rate.scalars().all()
        return projects_by_comp_rate


charityproject_crud = CRUDCharityProject(CharityProject)
