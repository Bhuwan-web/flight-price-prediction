"""User router."""

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.models.flight_record import (
    FlightRecordDB,
    FlightRecordIn,
    FlightRecordOut,
)
from auth.models.user import User
from auth.service.predict_price import predict_price
from auth.util.current_user import current_user

router = APIRouter(prefix="/flight", tags=["Flight"])


@router.post("/predict")
async def predict_flight_price(flight_record: FlightRecordIn, user: User = Depends(current_user)):
    predicted_prices = await predict_price(flight_record)
    flight_logs = [{"user_id": user.id, **predicted_price, **flight_record.model_dump()} for predicted_price in predicted_prices]

    flight_logs_db = [FlightRecordDB(**flight_log) for flight_log in flight_logs]
    db_data = await FlightRecordDB.insert_many(flight_logs_db)

    return JSONResponse(
        content={
            "success": True,
            "data": [
                {
                    **jsonable_encoder(FlightRecordOut.model_validate({**flight_log,"_id": str(db_data.inserted_ids[index])}).model_dump())
                } for index,flight_log in enumerate(flight_logs)
            ]
        },
        status_code=200
    )


@router.post("/logs")
async def flight_logs(user: User = Depends(current_user)) -> list:  # type: ignore[no-untyped-def]
    """Update allowed user fields."""
    flight_records = await FlightRecordDB.find(
        FlightRecordDB.user_id == user.id,FlightRecordDB.cancelled == False  # noqa: E712
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



