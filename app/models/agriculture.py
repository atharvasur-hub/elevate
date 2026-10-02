from datetime import date, datetime
from typing import Optional
from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AgricultureScheme(Base):
    __tablename__ = "agriculture_scheme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    beneficiary_id: Mapped[int] = mapped_column(Integer, ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    beneficiary_code: Mapped[str] = mapped_column(String(50), nullable=False)
    land_holding_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    subsidy_disbursed_inr: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    disbursal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    beneficiary: Mapped["Beneficiary"] = relationship("Beneficiary")
    location: Mapped["Location"] = relationship("Location")
