from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlertModel(Base):
    __tablename__ = "alerts"

    alert_id: Mapped[str] = mapped_column(String, primary_key=True)
    sensor_id: Mapped[str] = mapped_column(String, index=True)
    reading_value: Mapped[float] = mapped_column(Float)
    threshold: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
