"""User router."""

import random
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from auth.models.flight_record import (
    Destination,
    FlightRecordDB,
    FlightRecordIn,
    FlightRecordOut,
    Source,
)
from auth.models.user import User
from auth.service.predict_price import predict_price
from auth.util.current_user import current_user
from auth.models.flight_record import Airline

router = APIRouter(prefix="/flight", tags=["Flight"])


@router.post("/predict")
async def predict_flight_price(flight_record: FlightRecordIn):
    # async def get_user(flight_record: FlightRecordIn, user: User = Depends(current_user)):
    predicted_price = await predict_price(flight_record)
    # flight_log = {"user_id": user.id, **flight_record_with_amt}
    # flight_db_record = await FlightRecordDB(**flight_log).create()
    # flight_db_record.id = str(flight_db_record.id)

    # return FlightRecordOut(**flight_db_record.model_dump())
    return JSONResponse(
        content={"success": True, "data": predicted_price}, status_code=200
    )  # predicted_price


@router.post("/logs")
async def flight_logs(user: User = Depends(current_user)) -> list:  # type: ignore[no-untyped-def]
    """Update allowed user fields."""
    flight_records = await FlightRecordDB.find(
        FlightRecordDB.user_id == user.id
    ).to_list()
    return flight_records


@router.delete("/delete/{id}")
async def delete_record(
    id: str,
    user: User = Depends(current_user),
) -> Response:
    """Delete current user."""
    record = await FlightRecordDB.find_one(
        FlightRecordDB.user_id == user.id, id=ObjectId(id)
    )
    if record is None:
        raise HTTPException(404, "No record found")
    await record.delete()
    return Response(status_code=204)


@router.get("/sources")
async def source_keys() -> list:
    """Fetch all source keys"""
    sources = await Source.find({}).to_list()
    if not sources:
        raise HTTPException(404, "No sources found")
    return [source.source for source in sources]


@router.get("/destinations")
async def destination_keys() -> list:
    """Fetch all destination keys"""
    destinations = await Destination.find().to_list()
    if destinations is None:
        raise HTTPException(404, "No destinations found")
    return [destination.destination for destination in destinations]


@router.get("/airlines")
async def airline_keys() -> list:
    """Fetch all airline keys"""
    airlines = await Airline.find().to_list()
    if airlines is None:
        raise HTTPException(404, "No airlines found")
    return [airline.airline for airline in airlines]


@router.post("/source")
async def add_source(source: Source) -> Response:
    """Add source keys"""
    added_source = await source.create()
    return Response(added_source, status_code=201)
