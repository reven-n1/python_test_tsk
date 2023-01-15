from .db_models import Statistic
from ..database import Database
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.sql import func
from .schemas import IncomingStats
from .utils import check_field_for_existence, Cache
from fastapi import Depends
from json import loads
from .exceptions import NoContentFound
from typing import List


async def get_statistics(start_date: str, end_date: str, column: str = Depends(check_field_for_existence)) -> List[dict]:
    """ returns statistics for a period with optional order by column """

    async with await Database.get_class_session() as session:
        # i'd prefer to order_by using sql cause it's faster but i have no idea how to sort json elements by the specified field
        events = (await session.execute(select(
            func.json_object(
                'date', Statistic.date,
                'cost', func.SUM(Statistic.cost),
                'views', func.SUM(Statistic.views),
                'clicks', func.SUM(Statistic.clicks),
                'cpm', func.SUM(Statistic.clicks) / func.SUM(Statistic.clicks) * 1000,
                'cpc', func.SUM(Statistic.cost) / func.SUM(Statistic.clicks)
            ))
                                        .where(Statistic.date.between(start_date, end_date))
                                        .group_by(Statistic.date))
                  ).scalars().all()

        if not events: raise NoContentFound

        events = [loads(event) for event in events]
        if column:
            events.sort(key=lambda item: item.get(column))

    return events


async def reset_statistics() -> None:
    """ truncate table """
    async with await Database.get_class_session() as session:
        await session.execute(text(f"TRUNCATE TABLE {Statistic.__table__}"))

    Cache().reset_cache()


async def save_statistics(data: IncomingStats) -> None:
    """ save statistic to db """
    stats = Statistic(**data.dict())
    await stats.save()

    Cache().reset_cache()
