from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    max_threshold: Mapped[float | None] = mapped_column(nullable=True)

    readings = Mapped[list]
