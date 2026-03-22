"""
Comparing the naive random strategy vs. the optimal cycle-following strategy.
"""

import random


def simulate_random_strategy(
    boxes: list[int], num_prisoners: int, max_attempts: int
) -> bool:
    """
    Naive strategy: Each prisoner picks max_attempts boxes completely at random.
    """
    for prisoner in range(num_prisoners):
        # Prisoner randomly selects 50 distinct boxes
        chosen_boxes = random.sample(range(num_prisoners), max_attempts)

        found = False
        for box_index in chosen_boxes:
            if boxes[box_index] == prisoner:
                found = True
                break

        # If any single prisoner fails, everyone is executed
        if not found:
            return False

    return True


def simulate_cycle_strategy(
    boxes: list[int], num_prisoners: int, max_attempts: int
) -> bool:
    """
    Optimal strategy (Cycle-following):
    Prisoner i opens box i. If it's not their number j, they open box j next.
    """
    for prisoner in range(num_prisoners):
        current_box = prisoner
        found = False

        for _ in range(max_attempts):
            ticket = boxes[current_box]
            if ticket == prisoner:
                found = True
                break
            # Pointer chasing: the ticket dictates the next box to open
            current_box = ticket

        # If a prisoner is caught in a cycle longer than max_attempts, they fail
        if not found:
            return False

    return True


def run_simulation(iterations: int = 100_000):
    num_prisoners = 100
    max_attempts = 50

    random_successes = 0
    cycle_successes = 0

    print(f"=== Starting Simulation ===")
    print(f"Prisoners: {num_prisoners}, Attempts allowed: {max_attempts}")
    print(f"Running {iterations:,} iterations...\n")

    for _ in range(iterations):
        # Generate a random permutation of tickets 0 to 99
        boxes = list(range(num_prisoners))
        random.shuffle(boxes)

        # Test Naive Strategy
        if simulate_random_strategy(boxes, num_prisoners, max_attempts):
            random_successes += 1

        # Test Cycle-following Strategy
        if simulate_cycle_strategy(boxes, num_prisoners, max_attempts):
            cycle_successes += 1

    # Calculate and display empirical probabilities
    random_prob = (random_successes / iterations) * 100
    cycle_prob = (cycle_successes / iterations) * 100

    print("=== Simulation Results ===")
    print(
        f"1. Naive Random Strategy Success Rate: {random_prob:.6f}% ({random_successes}/{iterations})"
    )
    print(
        f"2. Cycle-following Strategy Success Rate: {cycle_prob:.4f}% ({cycle_successes}/{iterations})"
    )
    print(f"\nTheoretical Limit for Cycle Strategy: ~31.183%")


if __name__ == "__main__":
    run_simulation(iterations=100_000)
