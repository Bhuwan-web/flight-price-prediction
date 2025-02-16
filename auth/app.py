"""Server app config."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from auth.config import CONFIG
from auth.models.user import User
from auth.models.flight_record import FlightBooking, FlightRecordDB, Source, Destination, Airline

from auth.routes.auth import router as AuthRouter
from auth.routes.mail import router as MailRouter
from auth.routes.register import router as RegisterRouter
from auth.routes.user import router as UserRouter
from auth.routes.flight import router as FlightRouter
from auth.routes.booking import router as BookingRouter


DESCRIPTION = """
This API powers whatever I want to make

It supports:

- Account sign-up and management
- Something really cool that will blow your socks off
"""


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """Initialize application services."""
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).flight_price_predictor  # type: ignore[attr-defined]
    await init_beanie(
        app.db, document_models=[User, FlightRecordDB, Source, Destination, Airline,FlightBooking]
    )  # type: ignore[arg-type,attr-defined]
    print("Startup complete")
    yield
    print("Shutdown complete")


app = FastAPI(
    title="My Server",
    description=DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(AuthRouter)
app.include_router(MailRouter)
app.include_router(RegisterRouter)
app.include_router(UserRouter)
app.include_router(FlightRouter)
app.include_router(BookingRouter)


@app.get("/")
async def root():
    """Return a friendly hello world message."""
    return {
        "success": "Server Up and Running",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
    }
