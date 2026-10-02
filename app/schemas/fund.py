from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.scheme import SchemeResponse
from app.schemas.location import LocationResponse


class FundBase(BaseModel):
    scheme_id: int
    location_id: int
    financial_year: str
    allocated_amount: float
    disbursed_amount: float = 0.0
    utilized_amount: float = 0.0
    status: str = "Allocated"
    sanction_date: Optional[date] = None


class FundCreate(FundBase):
    pass


class FundUpdate(BaseModel):
    financial_year: Optional[str] = None
    allocated_amount: Optional[float] = None
    disbursed_amount: Optional[float] = None
    utilized_amount: Optional[float] = None
    status: Optional[str] = None
    sanction_date: Optional[date] = None


class FundResponse(FundBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FundDetailResponse(FundResponse):
    scheme: Optional[SchemeResponse] = None
    location: Optional[LocationResponse] = None
