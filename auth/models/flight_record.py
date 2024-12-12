from beanie import Document, PydanticObjectId
from datetime import datetime

from pydantic import BaseModel, Field

from bson import ObjectId


class FlightRecordIn(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    airline: str
    transit_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "origin": "JFK",
                "destination": "LHR",
                "departure_time": "2022-01-01T10:00:00",
                "arrival_time": "2022-01-01T12:00:00",
                "airline": "United",
                "transit_count": 1,
                "predicted_price": 100.0,
            }
        }


class FlightRecord(FlightRecordIn):
    predicted_price: float
    created_at: datetime = datetime.now()


class FlightRecordDB(FlightRecord, Document):
    user_id: PydanticObjectId

    class Settings:
        name = "flight_records"

    class Config:
        json_encoders = {ObjectId: str}


class FlightRecordOut(FlightRecordDB):
    id: str = Field(..., alias="_id")

    class Config:
        extra = "allow"
