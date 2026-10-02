from typing import Optional
from pydantic import BaseModel


class DatabaseStatus(BaseModel):
    status: str
    database: str
    version: Optional[str] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    status: str
    database: DatabaseStatus
