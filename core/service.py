import pandas as pd
from core.maps import geocode_address, build_distance_matrix
from core.routing import solve_vrp
from core.config import COMPANY_LOCATION, BUS_CAPACITY

def compute_optimized_routes(addresses: list[str]) -> list[dict]:
    """
    Main service function that:
    1) Geocodes addresses
    2) Builds travel time matrix
    3) Solves VRP with OR-Tools
    """

    rows = []

    # ALWAYS add company (depot) first
    rows.append({"name": "Company", "lat": COMPANY_LOCATION[0], "lon": COMPANY_LOCATION[1]})

    # Geocode all employee addresses
    for addr in addresses:
        loc = geocode_address(addr)
        if loc:
            rows.append({"name": addr, "lat": loc[0], "lon": loc[1]})

    # No valid locations?
    if len(rows) <= 1:
        return pd.DataFrame()

    # Build locations list for matrix
    locations = [(r["lat"], r["lon"]) for r in rows]
    matrix = build_distance_matrix(locations)

    # Estimate number of buses
    num_buses = max(1, len(rows) // BUS_CAPACITY)

    # Solve routing
    raw_routes = solve_vrp(matrix, num_buses)

    # Convert OR-Tools index routes into human-readable lists
    optimized = []
    for i, route in enumerate(raw_routes):
        optimized.append({"bus_id": i, "route_indices": route})

    return optimized
