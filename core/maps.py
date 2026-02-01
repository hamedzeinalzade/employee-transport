import requests
from core.config import GOOGLE_API_KEY

def geocode_address(address: str) -> tuple[float, float] | None:
    """
    Convert a textual address into geographic coordinates.

    Args:
        address (str): Human-readable address.

    Returns:
        tuple[float, float] | None:
            Latitude and longitude if successful, otherwise None.
    """

    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={address}&key={GOOGLE_API_KEY}"
    )
    r = requests.get(url).json()

    if r.get("status") != "OK":
        return None

    loc = r["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

def travel_time_min(origin: tuple[float, float], destination: tuple[float, float]) -> int | None:
    """
    Calculate travel time between two coordinates using live traffic data.

    Args:
        origin (tuple[float, float]): Origin latitude and longitude.
        destination (tuple[float, float]): Destination latitude and longitude.

    Returns:
        int | None:
            Travel time in minutes if available, otherwise None.
    """

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin[0]},{origin[1]}"
        f"&destinations={destination[0]},{destination[1]}"
        f"&departure_time=now&traffic_model=best_guess"
        f"&key={GOOGLE_API_KEY}"
    )
    r = requests.get(url).json()

    if r.get("status") != "OK":
        return None

    el = r["rows"][0]["elements"][0]
    if el.get("status") != "OK":
        return None

    # Return travel time in minutes
    return el["duration_in_traffic"]["value"] // 60

def build_distance_matrix(locations: list[tuple[float, float]]) -> list[list[int]]:
    """
    Build a full travel-time matrix between all locations.

    This matrix is required by OR-Tools to solve
    the Vehicle Routing Problem.

    Args:
        locations (list[tuple[float, float]]):
            List of (latitude, longitude) coordinates.

    Returns:
        list[list[int]]:
            2D matrix where each cell represents travel time in minutes.
            Unreachable paths are assigned a large penalty value.
    """
    matrix = []
    for origin in locations:
        row = []
        for dest in locations:
            t = travel_time_min(origin, dest)
            # If distance cannot be computed, set a large fallback
            row.append(t if t else 9999)
        matrix.append(row)
    return matrix
