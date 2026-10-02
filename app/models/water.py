from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WaterScheme(Base):
    __tablename__ = "water_scheme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    beneficiary_id: Mapped[int] = mapped_column(Integer, ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    beneficiary_code: Mapped[str] = mapped_column(String(50), nullable=False)
    tap_connection_status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    cost_incurred: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    beneficiary: Mapped["Beneficiary"] = relationship("Beneficiary")
    location: Mapped["Location"] = relationship("Location")
