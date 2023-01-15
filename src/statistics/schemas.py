from fastapi import Query
from pydantic import BaseModel, validator

from .constants import date_regex_format


class IncomingStats(BaseModel):
    date: str = Query(regex=date_regex_format)
    views: int | None
    clicks: int | None
    cost: float | None

    @validator('views', 'clicks', 'cost', always=False)
    def value_validator(cls, value, field):
        if not value >= 0:
            raise ValueError(f"{field.name} value must be >= 0, current {value}")
        return value

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-01-14",
                "views": 10,
                "clicks": 5,
                "cost": 15.10,
            }
        }


class SubOutcomeItem(BaseModel):
    date: str
    views: int
    clicks: int
    cost: float

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-01-14",
                "views": 10,
                "clicks": 5,
                "cost": 15.10,
            }
        }


class OutcomingStatistics(BaseModel):
    date: str
    views: int
    clicks: int
    cost: float
    cpc: float
    cpm: float

    class Config:
        schema_extra = {
            "date": "2023-01-15",
            "views": 100.0,
            "clicks": "10",
            "cost": "10.0",
            "cpc": 1.0,
            "cpm": 0.1
        }
