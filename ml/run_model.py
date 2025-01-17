import pickle
import numpy as np
from auth.models.flight_record import Airline
import asyncio
from concurrent.futures import ThreadPoolExecutor
# Make predictions using the loaded model

# %% predict Price
stop = [1]
journey_date = [12, 5]
departure = [18, 5]
arrival = [23, 30]
duration = [5, 25]
airlines = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
source = [0, 0, 1, 0]
destination = [0, 0, 0, 0, 1]

sample_input = np.array(
    [
        np.concatenate(
            (
                stop,
                journey_date,
                departure,
                arrival,
                duration,
                airlines,
                source,
                destination,
            )
        )
    ]
)


async def get_predicted_price(
    transit_count: int,
    journey_date: list,
    departure: list,
    arrival: list,
    source: list,
    destination: list,
    duration: list,
):
    with open("ml/flight_price_rf.pkl", "rb") as file:
        forest = pickle.load(file)

    airlines: list[Airline] = await Airline.find().to_list()

    def predict(airline: Airline):
        sample_input = [
            np.concatenate(
                (
                    transit_count,
                    journey_date,
                    departure,
                    arrival,
                    duration,
                    airline.array,
                    source,
                    destination,
                )
            )
        ]
        predicted_price = round(forest.predict(sample_input)[0], 2)
        return {"predicted_price": predicted_price, "airline": airline.airline}

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(executor, predict, airline) for airline in airlines
        ]
        predicted_prices = await asyncio.gather(*tasks)

    return predicted_prices
