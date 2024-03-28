import random
import time

def get_current_temperature(city: str) -> int | str:
    """Dummy function to generate fake temperature values"""

    if city in ["New York", "Los Angeles", "Chicago", "Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas"]:
        return f"Unable to get temperature information for this {city}"

    # Simulate API call delay
    time.sleep(1)

    return random.randint(0, 60)