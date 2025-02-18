
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from auth.models.flight_record import (
    Destination,
    Source,
)
from auth.models.user import User
from auth.util.current_user import current_user
from auth.models.flight_record import Airline

router = APIRouter(prefix="/flight", tags=["Flight"])

@router.get("/sources")
async def source_keys() -> list:
    """Fetch all source keys"""
    sources = await Source.find().to_list()
    if not sources:
        raise HTTPException(404, "No sources found")
    return [source.source for source in sources]


@router.get("/destinations")
async def destination_keys() -> list:
    """Fetch all destination keys"""
    destinations = await Destination.find().to_list()
    if destinations is None:
        raise HTTPException(404, "No destinations found")
    return JSONResponse(content={"data":[destination.destination for destination in destinations],"success":True},status_code=200)


@router.get("/airlines")
async def airline_keys() -> list:
    """Fetch all airline keys"""
    airlines = await Airline.find().to_list()
    if airlines is None:
        raise HTTPException(404, "No airlines found")
    return JSONResponse(content={"data":[airline.airline for airline in airlines],"success":True},status_code=200)


@router.post("/source")
async def add_sources(sources: list[Source],user: User = Depends(current_user)) -> Response:
    """Add source keys in bulk"""
    await Source.insert_many(sources)
    return JSONResponse(
        content={"success": True, "message": "Sources added"}, status_code=201
    )


@router.post("/destination")
async def add_destination(destinations: list[Destination],user: User = Depends(current_user)) -> Response:
    """Add source keys in bulk"""
    await Destination.insert_many(destinations)
    return JSONResponse(
        content={"success": True, "message": "Destinations added"}, status_code=201
    )


@router.post("/airline",)
async def add_airlines(airlines: list[Airline],user: User = Depends(current_user)) -> Response:
    """Add source keys in bulk"""
    await Airline.insert_many(airlines)
    return JSONResponse(
        content={"success": True, "message": "Airlines added"}, status_code=201
    )
