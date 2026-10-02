from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    state: str
    district: str
    sub_district: Optional[str] = None
    pincode: Optional[str] = None
    area_type: str = "Rural"


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    sub_district: Optional[str] = None
    pincode: Optional[str] = None
    area_type: Optional[str] = None


class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
