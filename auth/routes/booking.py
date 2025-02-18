
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.models.flight_record import (
    FlightBooking,
    FlightRecordDB,
    FlightRecordOut,
)
from auth.models.user import User
from auth.service.get_booking_details import get_booking_details
from auth.util.current_user import current_user
from auth.util.mail import send_booking_email, send_cancellation_email

router = APIRouter(prefix="/flight", tags=["Booking"])

@router.post("/book")
async def book_flight(flight_booking: FlightBooking,user: User = Depends(current_user)) -> Response:
    """Book a flight"""
    flight_record = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, FlightRecordDB.id == ObjectId(flight_booking.flight_id)
    )
    if flight_record is None:
        raise HTTPException(404, "No flight info found")
    if flight_record.booked:
        raise HTTPException(400, "Flight already booked")
    if not flight_record.user_id:
        flight_record.user_id = user.id
    flight_record_db = await FlightBooking.create(flight_booking)
    flight_record.booked = True
    await flight_record.save()
    booking_details = await get_booking_details(user.id,flight_booking.flight_id,flight_booking)  
    await send_booking_email(booking_details)
    return JSONResponse(
        content={"success": True, "message": "Flight booked", "data": jsonable_encoder(flight_record_db.model_dump())}, status_code=201
    )


@router.get("/info/{flight_id}")
async def get_flight_info(flight_id: str, user: User = Depends(current_user)):
    """Get flight info from logs based on flight_id"""
    flight_record_db = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, FlightRecordDB.id ==ObjectId(flight_id)
    )
    if flight_record_db is None:
        raise HTTPException(404, "No flight info found")
    return JSONResponse(content={"success": True, "data": jsonable_encoder(FlightRecordOut.model_validate(flight_record_db.model_dump()))},status_code=200)

@router.post("/cancel/{flight_id}")
async def cancel_flight_booking(flight_id: str, user: User = Depends(current_user)) -> Response:
    """Cancel a flight booking"""
    flight_record = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, FlightRecordDB.id == ObjectId(flight_id)
    )
    if flight_record is None:
        raise HTTPException(404, "No flight info found")
    booking=await FlightBooking.find_one(FlightBooking.flight_id==flight_id)
    if not booking:
        raise HTTPException(404, "No booking found")
    if booking.cancelled:
        raise HTTPException(400, "Flight already cancelled")
    booking.cancelled = True
    await booking.save()
    flight_booking = await FlightBooking.find_one(FlightBooking.flight_id==flight_id)
    booking_details = await get_booking_details(user.id,flight_id,flight_booking)
    if not booking_details:
        raise HTTPException(404, "No booking details found")
    await send_cancellation_email(booking_details)
    return JSONResponse(
        content={"success": True, "message": "Flight booking cancelled"}, status_code=200
    )

@router.get("/booked/logs")
async def get_booked_flights_logs(user: User = Depends(current_user)) -> list:
    """Get booked flights logs"""
    flight_records = await FlightRecordDB.find(  # noqa: F821
        FlightRecordDB.user_id == user.id, FlightRecordDB.booked == True  # noqa: E712
    ).to_list()
    return JSONResponse(content={"success": True, "data": jsonable_encoder(flight_records)},status_code=200)
