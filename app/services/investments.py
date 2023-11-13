from datetime import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def check_for_available_investments(
    obj: CharityProject, session: AsyncSession
) -> CharityProject:
    available_donations = await session.execute(select(Donation).where(
        Donation.fully_invested == False # noqa
    ))
    available_donations = available_donations.scalars().all()
    if not available_donations:
        return obj
    for donation in available_donations:
        if (obj.invested_amount + donation.available) >= obj.full_amount:
            donation.invested_amount += obj.needed_amount
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = dt.utcnow()
            obj.invested_amount = obj.full_amount
            obj.fully_invested = True
            obj.close_date = dt.utcnow()
            session.add(donation)
            break
        else:
            obj.invested_amount += donation.available
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = dt.utcnow()
            session.add(donation)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def check_for_projects_to_invest(
    obj: Donation, session: AsyncSession
) -> Donation:
    available_projects = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == False # noqa
    ))
    available_projects = available_projects.scalars().all()
    for project in available_projects:
        await check_for_available_investments(obj=project, session=session)
    await session.refresh(obj)
    return obj
