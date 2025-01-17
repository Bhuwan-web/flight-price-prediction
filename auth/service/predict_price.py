from auth.models.flight_record import Destination, FlightRecordIn, Source
import datetime

from ml.run_model import get_predicted_price


async def predict_price(user_record: FlightRecordIn):
    normalized_user_record = await get_normalized_user_record(user_record)
    return await get_predicted_price(**normalized_user_record)


async def get_normalized_user_record(user_record: FlightRecordIn):
    origin = user_record.origin
    destination = user_record.destination
    departure_time = user_record.departure_time
    arrival_time = user_record.arrival_time
    duration = user_record.arrival_time - user_record.departure_time
    transit_count = [user_record.transit_count]
    source_array = (await Source.find_one(Source.source == origin)).array
    destination_array = (
        await Destination.find_one(Destination.destination == destination)
    ).array

    normalized_departure_time = time_to_array(departure_time)
    normalized_arrival_time = time_to_array(arrival_time)
    normalized_duration = timedelta_to_array(duration)

    journey_date = datetime_to_array(departure_time)

    return {
        "transit_count": transit_count,
        "journey_date": journey_date,
        "departure": normalized_departure_time,
        "arrival": normalized_arrival_time,
        "source": source_array,
        "destination": destination_array,
        "duration": normalized_duration,
    }


def datetime_to_array(dt: datetime.datetime):
    """Convert datetime object to list of day,month"""
    return [dt.day, dt.month]


def time_to_array(time: datetime) -> list:
    return [time.hour, time.minute]


def timedelta_to_array(td: datetime.timedelta) -> list:
    """Convert timedelta object to list of hour,minute"""
    seconds = td.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return [hours, minutes]
