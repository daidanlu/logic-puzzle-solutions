from __future__ import annotations

import random
from typing import Iterable, List, Tuple, Dict

State = Tuple[int, ...]


def normalize(piles: Iterable[int]) -> State:
    """Return a canonical state: positive pile sizes sorted in descending order."""
    return tuple(sorted((p for p in piles if p > 0), reverse=True))


def triangular_number(k: int) -> int:
    """Return 1 + 2 + ... + k."""
    return k * (k + 1) // 2


def staircase(k: int) -> State:
    """Return the staircase fixed point {k, k-1, ..., 1}."""
    return tuple(range(k, 0, -1))


def step(state: State) -> State:
    """
    Perform one Bulgarian Solitaire move.

    If the current state has m piles, remove one card from each pile,
    discard empty piles, and add one new pile of size m.
    """
    m = len(state)
    old_piles_after_removal = [p - 1 for p in state if p - 1 > 0]
    return normalize(old_piles_after_removal + [m])


def find_cycle(initial_state: State) -> Tuple[List[State], List[State]]:
    """
    Starting from initial_state, return (preperiod, cycle).

    Since the number of states is finite and the transition rule is deterministic,
    some state must eventually repeat.
    """
    seen: Dict[State, int] = {}
    orbit: List[State] = []
    state = normalize(initial_state)

    while state not in seen:
        seen[state] = len(orbit)
        orbit.append(state)
        state = step(state)

    cycle_start = seen[state]
    return orbit[:cycle_start], orbit[cycle_start:]


def random_partition(n: int) -> State:
    """Generate a random partition of n as a normalized state."""
    piles = []
    remaining = n

    while remaining > 0:
        size = random.randint(1, remaining)
        piles.append(size)
        remaining -= size

    return normalize(piles)


def ghost_capacity(max_pile_count: int) -> int:
    """
    Capacity of the largest possible staircase with max_pile_count piles:

        m + (m - 1) + ... + 1 = m(m + 1)/2
    """
    return triangular_number(max_pile_count)


def explain_cycle(cycle: List[State], k: int) -> None:
    """Print the key quantities used in the proof for a detected cycle."""
    max_pile_count = max(len(state) for state in cycle)
    n = triangular_number(k)

    print("Detected cycle:")
    for state in cycle:
        print(f"  {state}")

    print()
    print(f"Total cards N:                     {n}")
    print(f"Triangular index k:                {k}")
    print(f"Maximum pile count in the cycle m: {max_pile_count}")
    print(f"Ghost staircase capacity T_m:      {ghost_capacity(max_pile_count)}")
    print(f"Staircase fixed point:             {staircase(k)}")

    assert max_pile_count == k
    assert cycle == [staircase(k)]


def simulate_one_example() -> None:
    """Run the example N = 10."""
    k = 4
    initial_state = normalize([5, 4, 1])

    print("Example simulation")
    print("==================")
    print(f"Initial state: {initial_state}")

    state = initial_state
    for t in range(1, 20):
        state = step(state)
        print(f"t={t:2d}: {state}")

        if state == staircase(k):
            print("Reached the staircase fixed point.")
            break

    print()
    preperiod, cycle = find_cycle(initial_state)
    print(f"Preperiod length: {len(preperiod)}")
    print(f"Cycle length:     {len(cycle)}")
    explain_cycle(cycle, k)


def test_many_random_states(k: int, trials: int = 1000) -> None:
    """
    Test many random initial states for N = k(k+1)/2.

    This does not replace the proof, but it computationally illustrates
    that every tested initial state reaches the same staircase fixed point.
    """
    n = triangular_number(k)
    target = staircase(k)

    for _ in range(trials):
        initial_state = random_partition(n)
        _preperiod, cycle = find_cycle(initial_state)
        assert cycle == [target], (initial_state, cycle, target)

    print(f"Random test passed for k={k}, N={n}, trials={trials}.")


def main() -> None:
    simulate_one_example()

    print()
    print("Randomized verification")
    print("=======================")

    for k in range(1, 11):
        test_many_random_states(k, trials=500)


if __name__ == "__main__":
    main()
