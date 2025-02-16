from bson import ObjectId
from fastapi import HTTPException
from auth.models.flight_record import FlightBooking, FlightBookingDetails, FlightRecordDB
from auth.models.user import User

async def get_booking_details(user_id:str,flight_id:str,booking_details:FlightBooking):
    """Get booking details."""
    flight_record = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user_id, FlightRecordDB.id == ObjectId(flight_id)
    )
    email=booking_details.email
    if not email:
        email=(await User.find_one(User.id==user_id)).email

    if flight_record is None:
        raise HTTPException(404, "Flight record not found")
    data={"user_id":flight_record.user_id,"email":email,"user_name":booking_details.user_name,"phone_number":booking_details.phone_number,"flight_id":str(flight_record.id),"airline":flight_record.airline,"origin":flight_record.origin,"destination":flight_record.destination,"departure_time":flight_record.departure_time,"arrival_time":flight_record.arrival_time,"transit_count":flight_record.transit_count,"predicted_price":flight_record.predicted_price,}
    return FlightBookingDetails(**data)
    