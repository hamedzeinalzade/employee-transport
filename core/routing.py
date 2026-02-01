from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrp(distance_matrix: list[list[int]], num_vehicles: int, depot: int = 0) -> list[list[int]]:
    """
    Solve the Vehicle Routing Problem (VRP).

    Args:
        distance_matrix (list[list[int]]):
            Square matrix of travel times between locations.
        num_vehicles (int): Number of available vehicles.
        depot (int): Index of the depot (default is 0).

    Returns:
        list[list[int]]:
            A list of routes, each represented as a list of node indices.
            Each route starts and ends at the depot.
    """

    # Manager translates node index to OR-Tools index
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix), num_vehicles, depot=0
    )

    # Routing model
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index: int, to_index: int) -> int:
        """
        Callback used by OR-Tools to retrieve travel cost.

        Args:
            from_index (int): Origin index.
            to_index (int): Destination index.

        Returns:
            int: Travel cost between nodes.
        """
        return distance_matrix[
            manager.IndexToNode(from_index)
        ][
            manager.IndexToNode(to_index)
        ]

    transit_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_index)

    # Strategy: start with cheapest path and improve
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_params)

    routes = []
    if solution:
        for v in range(num_vehicles):
            index = routing.Start(v)
            route = []
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))  # End at depot
            routes.append(route)

    return routes
