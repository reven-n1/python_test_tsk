from typing import List

from starlette.status import HTTP_204_NO_CONTENT
from fastapi import APIRouter, Query, Depends
from fastapi.responses import Response

from .service import get_statistics, reset_statistics, save_statistics
from .schemas import IncomingStats, OutcomingStatistics
from .utils import cache, check_field_for_existence
from .constants import date_regex_format
from .exceptions import NoContentFound

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
    responses={404: {"description": "Not found"}}
)


@router.post("/stats", summary="Summary of the Endpoint")
async def save_stats(stats_data: IncomingStats):
    await save_statistics(stats_data)
    return Response(status_code=201)


@router.get("/stats", response_model=List[OutcomingStatistics], summary="Summary of the Endpoint")
@cache
async def get_stats(start_date: str = Query(regex=date_regex_format),
                    end_date: str = Query(regex=date_regex_format),
                    order_by: str | None = Depends(check_field_for_existence)):

    """ returns statistics for the specified period """

    # it was possible to specify the datetime type but the format in task was slightly different

    try:
        data = await get_statistics(start_date=start_date, end_date=end_date, column=order_by)
    except NoContentFound:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return data


@router.delete("/stats", summary="Summary of the Endpoint")
async def reset_stats():
    await reset_statistics()
    return Response(status_code=200)
