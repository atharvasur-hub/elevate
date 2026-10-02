from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SchemeBase(BaseModel):
    name: str
    code: str
    ministry: str
    sector: str
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    budget_allocated: float = 0.0
    is_active: bool = True
    launch_date: Optional[date] = None


class SchemeCreate(SchemeBase):
    pass


class SchemeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    ministry: Optional[str] = None
    sector: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    budget_allocated: Optional[float] = None
    is_active: Optional[bool] = None
    launch_date: Optional[date] = None


class SchemeResponse(SchemeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
