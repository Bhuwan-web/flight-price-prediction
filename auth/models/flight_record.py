from beanie import Document, PydanticObjectId
from datetime import datetime

from pydantic import BaseModel, Field

from bson import ObjectId


class FlightRecordIn(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    transit_count: int

    @classmethod
    def validate_origin(cls, value):
        if not Source.find_one(Source.source == value):
            raise ValueError(f"Origin {value} is not a valid source")

    @classmethod
    def validate_destination(cls, value):
        if not Destination.find_one(Destination.destination == value):
            raise ValueError(f"Destination {value} is not a valid destination")

    @classmethod
    def validate_airline(cls, value):
        if not Airline.find_one(Airline.airline == value):
            raise ValueError(f"Airline {value} is not a valid airline")

    class Config:
        json_schema_extra = {
            "example": {
                "origin": "Chennai",
                "destination": "Cochin",
                "departure_time": "2022-01-01T10:00:00",
                "arrival_time": "2022-01-01T12:00:00",
                "transit_count": 1,
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


class Source(Document):
    """Destinations Document."""

    source: str
    array: list[int]

    class Settings:
        name = "sources"


class Airline(Document):
    """Destinations Document."""

    airline: str
    array: list[int]

    class Settings:
        name = "airlines"

    class Config:
        json_encoders = {ObjectId: str}


class Destination(Document):
    """Destinations Document."""

    destination: str
    array: list[int]

    class Settings:
        name = "destinations"
