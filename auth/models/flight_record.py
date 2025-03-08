from beanie import Document, PydanticObjectId
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator, root_validator, validator

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


class FlightBookingInput(BaseModel):
    """Bookings Document."""

    flight_id: PydanticObjectId
    user_id: PydanticObjectId|None=None
    user_name: str
    email:str|None=None
    phone_number: str
    quantity: int = 1
    created_at: datetime = datetime.now()
    cancelled: bool = False
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

class FlightBookingRecord(FlightBookingInput,Document):
    total_price: float=0

    
    @model_validator(mode='after')
    def total_price_must_not_be_zero(cls, values):
        if 'total_price' in values and values['total_price'] == 0:
            flight_record:FlightRecordDB = FlightRecordDB.find_one(FlightRecordDB.id == values['flight_id']).run_sync()
            if not flight_record:
                raise ValueError("Flight record not found")
            predicted_price = flight_record.predicted_price
            values['total_price'] = values['quantity'] *predicted_price
        return values
    
    
    
    class Settings:
        name = "bookings"
    
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
    total_price: float

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