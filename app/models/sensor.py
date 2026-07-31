from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db import Base
from typing import List

class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)

    readings = Mapped[List]