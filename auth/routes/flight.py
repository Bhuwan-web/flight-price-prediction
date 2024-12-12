"""User router."""

import random
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response

from auth.models.flight_record import (
    FlightRecordDB,
    FlightRecordIn,
    FlightRecordOut,
)
from auth.models.user import User
from auth.util.current_user import current_user

router = APIRouter(prefix="/flight", tags=["Flight"])


@router.post("/predict")
async def get_user(flight_record: FlightRecordIn, user: User = Depends(current_user)):
    flight_prediction = random.randint(1000, 7000)
    flight_record_with_amt = {
        **flight_record.model_dump(),
        "predicted_price": flight_prediction,
    }
    flight_log = {"user_id": user.id, **flight_record_with_amt}
    flight_db_record = await FlightRecordDB(**flight_log).create()
    flight_db_record.id = str(flight_db_record.id)

    return FlightRecordOut(**flight_db_record.model_dump())


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
