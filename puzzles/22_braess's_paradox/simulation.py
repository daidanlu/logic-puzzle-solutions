TOTAL_DRIVERS = 4000
EPS = 1e-9


ROUTES_BEFORE = {
    "P1": ("SA", "AD"),  # S -> A -> D
    "P2": ("SB", "BD"),  # S -> B -> D
}

ROUTES_AFTER = {
    "P1": ("SA", "AD"),  # S -> A -> D
    "P2": ("SB", "BD"),  # S -> B -> D
    "P3": ("SA", "AB", "BD"),  # S -> A -> B -> D
}


def edge_cost(edge, load):
    """Return the travel time of an edge with the current number of drivers."""
    if edge == "SA":
        return load / 100
    if edge == "BD":
        return load / 100
    if edge == "AD":
        return 45
    if edge == "SB":
        return 45
    if edge == "AB":
        return 0

    raise ValueError(f"Unknown edge: {edge}")


def edge_loads(route_counts, routes):
    """Count how many drivers are using each edge."""
    loads = {}

    for route in routes.values():
        for edge in route:
            loads[edge] = 0

    for route_name, count in route_counts.items():
        for edge in routes[route_name]:
            loads[edge] += count

    return loads


def route_cost(route_name, route_counts, routes):
    """Compute the total travel time of one route."""
    loads = edge_loads(route_counts, routes)
    total = 0

    for edge in routes[route_name]:
        total += edge_cost(edge, loads[edge])

    return total


def all_route_costs(route_counts, routes):
    """Compute the travel time of every available route."""
    return {
        route_name: route_cost(route_name, route_counts, routes)
        for route_name in routes
    }


def cost_after_one_driver_switch(from_route, to_route, route_counts, routes):
    """
    Compute the cost for one driver if they switch routes.

    The driver's own switch changes the edge loads by one, so we create
    a temporary copy of the route counts before measuring the new cost.
    """
    if route_counts[from_route] <= 0:
        return float("inf")

    new_counts = route_counts.copy()
    new_counts[from_route] -= 1
    new_counts[to_route] += 1

    return route_cost(to_route, new_counts, routes)


def has_better_response(route_counts, routes):
    """Check whether some driver can improve by switching to another route."""
    for current_route in routes:
        if route_counts[current_route] == 0:
            continue

        current_cost = route_cost(current_route, route_counts, routes)

        for new_route in routes:
            if new_route == current_route:
                continue

            new_cost = cost_after_one_driver_switch(
                current_route,
                new_route,
                route_counts,
                routes,
            )

            if new_cost < current_cost - EPS:
                return True

    return False


def best_response_simulation(initial_counts, routes, max_steps=100000):
    """
    Run a simple selfish-routing simulation.

    In each step, one driver checks whether another route is better.
    If switching helps, that driver moves to the best available route.
    The simulation stops when no single driver can improve.
    """
    route_counts = initial_counts.copy()

    for step in range(max_steps):
        moved = False

        for current_route in routes:
            if route_counts[current_route] == 0:
                continue

            current_cost = route_cost(current_route, route_counts, routes)
            best_route = current_route
            best_cost = current_cost

            for new_route in routes:
                if new_route == current_route:
                    continue

                new_cost = cost_after_one_driver_switch(
                    current_route,
                    new_route,
                    route_counts,
                    routes,
                )

                if new_cost < best_cost - EPS:
                    best_cost = new_cost
                    best_route = new_route

            if best_route != current_route:
                route_counts[current_route] -= 1
                route_counts[best_route] += 1
                moved = True
                break

        if not moved:
            return route_counts, step

    return route_counts, max_steps


def print_state(title, route_counts, routes):
    """Print the route distribution, edge loads, route costs, and stability."""
    print(title)
    print("-" * len(title))

    print("Route counts:")
    for route_name in routes:
        print(f"  {route_name}: {route_counts[route_name]}")

    print("Edge loads:")
    loads = edge_loads(route_counts, routes)
    for edge in sorted(loads):
        print(f"  {edge}: {loads[edge]}")

    print("Route costs:")
    costs = all_route_costs(route_counts, routes)
    for route_name in routes:
        print(f"  {route_name}: {costs[route_name]:.2f} minutes")

    print(f"Nash equilibrium? {not has_better_response(route_counts, routes)}")
    print()


def main():
    # Before the new edge exists, traffic should split evenly.
    before_counts = {
        "P1": 2000,
        "P2": 2000,
    }

    print_state(
        "Before adding A -> B",
        before_counts,
        ROUTES_BEFORE,
    )

    # After the new edge exists, everyone is drawn to P3.
    after_counts = {
        "P1": 0,
        "P2": 0,
        "P3": 4000,
    }

    print_state(
        "After adding A -> B",
        after_counts,
        ROUTES_AFTER,
    )

    # Start from the old equilibrium and let drivers selfishly switch routes.
    start_counts = {
        "P1": 2000,
        "P2": 2000,
        "P3": 0,
    }

    final_counts, steps = best_response_simulation(
        start_counts,
        ROUTES_AFTER,
    )

    print(f"Best-response simulation stopped after {steps} switches.")
    print_state(
        "Final state of the simulation",
        final_counts,
        ROUTES_AFTER,
    )

    before_time = route_cost("P1", before_counts, ROUTES_BEFORE)
    after_time = route_cost("P3", after_counts, ROUTES_AFTER)

    print("Summary")
    print("-------")
    print(f"Travel time before adding A -> B: {before_time:.2f} minutes")
    print(f"Travel time after adding A -> B:  {after_time:.2f} minutes")
    print(f"Increase caused by selfish routing: {after_time - before_time:.2f} minutes")


if __name__ == "__main__":
    main()
