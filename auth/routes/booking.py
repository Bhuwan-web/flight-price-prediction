
import json
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.models.flight_record import (
    FlightBookingInput,
    FlightBookingRecord,
    FlightRecordDB,
    FlightRecordOut,
)
from auth.models.user import User
from auth.service.get_booking_details import get_booking_details
from auth.util.current_user import current_user
from auth.util.mail import send_booking_email, send_cancellation_email

router = APIRouter(prefix="/flight", tags=["Booking"])

@router.post("/book")
async def book_flight(flight_booking: FlightBookingInput,user: User = Depends(current_user)) -> Response:
    """Book a flight"""
    flight_record = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, FlightRecordDB.id == ObjectId(flight_booking.flight_id)
    )
    if flight_record is None:
        raise HTTPException(404, "No flight info found")
    if flight_record.booked:
        raise HTTPException(400, "Flight already booked")
    if not flight_booking.user_id:
        flight_booking.user_id = user.id
    flight_record.booked = True
    if not flight_booking.email:
        flight_booking.email=user.email
    total_price = flight_record.predicted_price * flight_booking.quantity
    booking_record_db = FlightBookingRecord(**flight_booking.model_dump(), total_price=total_price)
    await booking_record_db.save()
    booking_details = await get_booking_details(user.id,flight_booking.flight_id,booking_record_db)  
    await send_booking_email(booking_details)
    return JSONResponse(
        content={"success": True, "message": "Flight booked", "data": json.loads(booking_record_db.model_dump_json())}, status_code=201
    )


@router.post("/info/{flight_id}")
async def get_flight_info(flight_id: str, user: User = Depends(current_user)):
    """Get flight info from logs based on flight_id"""
    flight_record_db = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, FlightRecordDB.id ==ObjectId(flight_id)
    )
    if flight_record_db is None:
        raise HTTPException(404, "No flight info found")
    return JSONResponse(content={"success": True, "data": jsonable_encoder(FlightRecordOut.model_validate(flight_record_db.model_dump()))},status_code=200)

@router.post("/cancel")
async def cancel_flight_booking(booking_id: str, user: User = Depends(current_user)) -> Response:
    """Cancel a flight booking"""

    booking=await FlightBookingRecord.find_one(FlightBookingRecord.user_id == ObjectId(user.id),FlightBookingRecord.id==ObjectId(booking_id))
    if not booking:
        raise HTTPException(404, "No booking found")
    if booking.cancelled:
        raise HTTPException(400, "Flight already cancelled")
    booking.cancelled = True
    await booking.save()
    booking_details = await get_booking_details(user.id,booking.flight_id,booking)
    if not booking_details:
        raise HTTPException(404, "No booking details found")
    await send_cancellation_email(booking_details)
    return JSONResponse(
        content={"success": True, "message": "Flight booking cancelled"}, status_code=200
    )

@router.post("/booked/logs")
async def get_booked_flights_logs(user: User = Depends(current_user)) -> list:
    """Get booked flights logs"""
    flight_records = await FlightBookingRecord.find(  # noqa: F821
        FlightBookingRecord.user_id == user.id  # noqa: E712
    ).to_list()
    result = []
    for record in flight_records:
        flight_details = await FlightRecordDB.find_one(FlightRecordDB.id == ObjectId(record.flight_id))
        if record.total_price == 0:
            # old records may not contain total price record in db
            record.total_price = record.quantity * flight_details.predicted_price
            record.save()
        result.append({
            "_id": str(record.id),
            "user_id": str(record.user_id),
            "flight_id": str(record.flight_id),
            "cancelled": record.cancelled,
            "quantity": record.quantity,
            "total_price": record.total_price,
            "flight_details": flight_details
        })
    return JSONResponse(content={"success": True, "data":jsonable_encoder(result)},status_code=200)
