from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class SensorCreate(BaseModel):
    id: str
    type: str
    location: str


class SensorOut(SensorCreate):
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class ReadingCreate(BaseModel):
    value: float
    unit: str

    @model_validator(mode="after")
    def check_physical_ranges(self):
        unit_upper = self.unit.upper()

        if unit_upper in ["C", "CELSIUS"]:
            if self.value < -273.15:
                raise ValueError("Física inválida: Temperatura menor al cero absoluto")

        elif unit_upper in ["%", "HUMEDAD"]:
            if not (0 <= self.value <= 100):
                raise ValueError("Física inválida: la humedad relativa debe de estar en 0% y 100%")

        elif unit_upper in ["HPA", "PA", "ATM"]:
            if self.value <= 0:
                raise ValueError("Física inválida: La presion atmosferica debe ser mayor a 0")

        else:
            raise ValueError(f"Física inválida. Unidad de medida {self.unit} no  reconocida por el sistema")

        return self


class SensorReadingOut(ReadingCreate):
    id: int
    sensor_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
