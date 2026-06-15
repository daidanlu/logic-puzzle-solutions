"""
Josephus Problem, step size 2.
This simulation verifies the proof that if N = 2^m + L,  0 <= L < 2^m,
then the final survivor is W(N) = 2L + 1.
Equivalently, W(N) is obtained by moving the leading binary 1 of N
to the lowest bit position.
"""

from random import randint


def josephus_simulation(n: int, trace: bool = False) -> int:
    """
    Direct circular simulation.
    Agents are numbered from 1 to n.
    Starting from agent 1, each active agent eliminates the next alive agent.
    The process continues until only one agent remains.
    Time complexity: O(n^2) here because list.pop(index) may shift elements.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    circle = list(range(1, n + 1))
    current = 0

    if trace:
        print(f"Initial circle: {circle}")

    while len(circle) > 1:
        victim = (current + 1) % len(circle)

        if trace:
            print(f"{circle[current]} eliminates {circle[victim]}")

        circle.pop(victim)

        # After removing the victim, the next active agent is now at
        # the victim's old index modulo the new circle length.
        current = victim % len(circle)

        if trace:
            print(f"Remaining: {circle}")

    return circle[0]


def josephus_formula(n: int) -> int:
    """
    Closed-form solution.
    Let 2^m be the largest power of 2 not exceeding n.
    Then n = 2^m + L, and the survivor is 2L + 1.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    highest_power_of_two = 1 << (n.bit_length() - 1)
    L = n - highest_power_of_two
    return 2 * L + 1


def josephus_binary_rotation(n: int) -> int:
    """
    Binary rotation interpretation.
    Move the leading binary 1 of n to the end.
    Example:
        41 = 101001_2
        rotate left over effective width:
        010011_2 = 19
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    binary = bin(n)[2:]

    if len(binary) == 1:
        rotated = binary
    else:
        rotated = binary[1:] + binary[0]

    return int(rotated, 2)


def demo(n: int) -> None:
    print("=" * 72)
    print(f"Demo: N = {n}")
    print("=" * 72)

    simulated = josephus_simulation(n, trace=(n <= 20))
    formula = josephus_formula(n)
    rotated = josephus_binary_rotation(n)

    highest_power_of_two = 1 << (n.bit_length() - 1)
    L = n - highest_power_of_two

    print()
    print(f"Largest power of 2 <= N: {highest_power_of_two}")
    print(f"Decomposition: N = {highest_power_of_two} + {L}")
    print(f"Formula: W(N) = 2L + 1 = {2 * L + 1}")

    print()
    print(f"Binary N:        {bin(n)[2:]}")
    print(f"Binary survivor: {bin(rotated)[2:]}")
    print()

    print(f"Simulation result:      {simulated}")
    print(f"Closed-form result:     {formula}")
    print(f"Binary rotation result: {rotated}")
    print(f"All match:              {simulated == formula == rotated}")


def verify_exhaustive(limit: int = 500) -> None:
    """
    Exhaustively compare direct simulation and formula for small N.
    """
    for n in range(1, limit + 1):
        simulated = josephus_simulation(n)
        formula = josephus_formula(n)
        rotated = josephus_binary_rotation(n)

        if not (simulated == formula == rotated):
            raise AssertionError(
                f"Mismatch at N={n}: "
                f"simulation={simulated}, formula={formula}, rotation={rotated}"
            )

    print(f"Exhaustive verification passed for N = 1 to {limit}.")


def verify_random(samples: int = 10_000, max_n: int = 10**9) -> None:
    """
    Randomly verify formula and binary rotation.
    Direct list simulation is not used here because it is too slow for large N.
    """
    for _ in range(samples):
        n = randint(1, max_n)

        formula = josephus_formula(n)
        rotated = josephus_binary_rotation(n)

        if formula != rotated:
            raise AssertionError(
                f"Mismatch at N={n}: formula={formula}, rotation={rotated}"
            )

    print(f"Random verification passed for {samples} samples up to N = {max_n}.")


if __name__ == "__main__":
    demo(41)

    print()
    verify_exhaustive(limit=500)

    print()
    verify_random(samples=10_000, max_n=10**9)
