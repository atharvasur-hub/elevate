from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RuralDevScheme(Base):
    __tablename__ = "rural_dev_scheme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    beneficiary_id: Mapped[int] = mapped_column(Integer, ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    beneficiary_code: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    days_worked: Mapped[int] = mapped_column(Integer, nullable=False)
    wages_paid_inr: Mapped[float] = mapped_column(Float, nullable=False)
    project_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    beneficiary: Mapped["Beneficiary"] = relationship("Beneficiary")
    location: Mapped["Location"] = relationship("Location")
