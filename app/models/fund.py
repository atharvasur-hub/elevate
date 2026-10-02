from datetime import date, datetime
from typing import Optional
from sqlalchemy import Date, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Fund(Base):
    __tablename__ = "funds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scheme_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    location_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    financial_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    allocated_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    disbursed_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    utilized_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
