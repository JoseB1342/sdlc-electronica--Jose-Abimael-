from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel


class SQLiteReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        db_reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def list_for_sensor(self, sensor_id: str, limit: int, offset: int, from_date: datetime | None, to_date: datetime | None) -> list[ReadingModel]:
        query = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

        if from_date:
            query = query.where(ReadingModel.created_at >= from_date)
        if to_date:
            query = query.where(ReadingModel.created_at <= to_date)

        query = query.order_by(ReadingModel.created_at.desc()).offset(offset).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self.db.get(ReadingModel, reading_id)

    def delete(self, reading_id: int) -> None:
        db_reading = self.get_by_id(reading_id)
        if db_reading:
            self.db.delete(db_reading)
            self.db.commit()

    def get_statistics(self, sensor_id: str, from_date: datetime | None = None, to_date: datetime | None = None) -> dict:
        query = select(
            func.min(ReadingModel.value).label("min_value"),
            func.max(ReadingModel.value).label("max_value"),
            func.avg(ReadingModel.value).label("avg_value")
        ).where(ReadingModel.sensor_id == sensor_id)

        if from_date:
            query = query.where(ReadingModel.created_at >= from_date)
        if to_date:
            query = query.where(ReadingModel.created_at <= to_date)

        result = self.db.execute(query).first()

    
        if result and result.min_value is not None:
            return {
                "min": round(result.min_value, 2),
                "max": round(result.max_value, 2),
                "avg": round(result.avg_value, 2)
            }
        
        return {"min": 0.0, "max": 0.0, "avg": 0.0}


# ----------------------------------------------


class SQLiteSensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, sensor_id: str, sensor_type: str, location: str, max_threshold: float | None = None) -> SensorModel:
        db_sensor = SensorModel(
            id=sensor_id, 
            type=sensor_type, 
            location=location,
            max_threshold=max_threshold
        )
        self.db.add(db_sensor)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor

    def get_by_id(self, sensor_id: str) -> SensorModel | None:
        return self.db.get(SensorModel, sensor_id)

    def list_all(self, limit: int, offset: int) -> list[SensorModel]:
        query = select(SensorModel).where(SensorModel.is_active).offset(offset).limit(limit)
        return list(self.db.scalars(query).all())

    def delete(self, sensor_id: str) -> None:
        sensor = self.get_by_id(sensor_id)
        if sensor:
            sensor.is_active = False
            self.db.commit()

    def deactivate(self, sensor_id: str) -> Any:
        sensor = self.get_by_id(sensor_id)
        
        if not sensor:
            return None
            
        sensor.is_active = False
        self.db.commit()
        self.db.refresh(sensor)
        
        return sensor