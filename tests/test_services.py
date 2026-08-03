from datetime import UTC, datetime

import pytest

from app.models.reading import ReadingModel
from app.services.reading_service import ReadingService


class FakeReadingRepository:
    def __init__(self):
        self._storage: list[ReadingModel] = []
        self._id_counter = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        fake_reading = ReadingModel(
            id=self._id_counter,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
            created_at=datetime.now(UTC),
        )
        self._storage.append(fake_reading)
        self._id_counter += 1
        return fake_reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self._storage if r.sensor_id == sensor_id]


def test_record_successful():
    fake_repo = FakeReadingRepository()
    service = ReadingService(repo=fake_repo)

    result = service.record(sensor_id="TEMP-01", value=25.0, unit="C")

    assert result.sensor_id == "TEMP-01"
    assert result.value == 25.0
    assert len(fake_repo._storage) == 1


def test_record_below_absolute_zero():
    # 1. Preparar (Arrange)
    fake_repo = FakeReadingRepository()
    service = ReadingService(repo=fake_repo)

    with pytest.raises(ValueError, match="Temperatura por debajo del cero absoluto"):
        service.record(sensor_id="TEMP-01", value=-300.0, unit="C")

    assert len(fake_repo._storage) == 0
