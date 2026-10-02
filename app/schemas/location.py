from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    state: str
    district: str
    sub_district: str
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    sub_district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationResponse(LocationBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
