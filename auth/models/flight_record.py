from beanie import Document, PydanticObjectId
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

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
    user_id: PydanticObjectId # type: ignore
    airline: str
    booked: bool=False

    class Settings:
        name = "flight_records"

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class FlightRecordOut(FlightRecordDB):
    id: ObjectId|str = Field(..., alias="_id")

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


class FlightBooking(Document):
    """Bookings Document."""

    flight_id: PydanticObjectId
    user_id: PydanticObjectId|None=None
    user_name: str
    email:str|None=None
    phone_number: str
    quantity: int = 1
    created_at: datetime = datetime.now()
    cancelled: bool = False

    class Settings:
        name = "bookings"
    @field_validator('phone_number')
    def phone_number_must_be_10_digits(cls, value):
        if len(value) != 10:
            raise ValueError('Phone number must be 10 digits')
        return value
    
    @field_validator('user_name')
    def name_must_be_at_least_2_characters(cls, value):
        if len(value) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return value

class FlightBookingDetails(BaseModel):
    booking_id: str
    user_name: str
    email: str
    phone_number: str
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    transit_count: int
    predicted_price: float
    quantity: int = 1

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "John Doe",
                "phone_number": "1234567890",
                "flight_id": "1234567890",
                "airline": "Indigo",
                "origin": "Chennai",
                "destination": "Cochin",
                "departure_time": "2022-01-01T10:00:00",
                "arrival_time": "2022-01-01T12:00:00",
                "transit_count": 1,
                "predicted_price": 1000,
                "quantity": 1,
            }
        }