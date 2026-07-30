from sqlalchemy.orm import Session 
from sqlalchemy import select
from datetime import datetime

from app.models.reading import ReadingModel

class SQLiteReadingRepository:
    def __init__(self, db: Session):
        self.db = db 

    def add(self, sensor_id: str, value: str, unit: str) -> ReadingModel:
        db_reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading 

    def list_for_sensor(self, sensor_id:str, limit:int, offset:int, from_date: datetime | None, to_date: datetime | None) -> list[ReadingModel]:
        query = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

        if from_date:
            query = query.where(ReadingModel.created_at >= from_date)
        if to_date:
            query = query.where(ReadingModel.crated_at <= to_date)

        query = query.offset(offset).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, reading_id:int) -> ReadingModel | None:
        return self.db.get(ReadingModel, reading_id)

    def delate (self, reading_id: int) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading:
            self.db.delate(reading)
            self.db.commit()
