"""
Simulation for the classic Gossip Problem.

Problem:
    There are N >= 4 nodes.
    Initially, node i knows only secret s_i.
    A call between nodes u and v updates both knowledge sets to their union.
    The goal is for every node to know all N secrets.

This script simulates:
    1. The optimal four-core construction using exactly 2N - 4 calls.
    2. A three-core comparison construction using 2N - 3 calls.
    3. Step-by-step knowledge propagation and correctness verification.

Run:
    python simulation.py
    python simulation.py --n 8
    python simulation.py --n 8 --quiet
    python simulation.py --n 8 --three-core
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Node = int
Secret = str
Call = Tuple[Node, Node]


@dataclass(frozen=True)
class SimulationResult:
    n: int
    calls: List[Call]
    knowledge: Dict[Node, Set[Secret]]

    @property
    def call_count(self) -> int:
        return len(self.calls)

    @property
    def all_secrets(self) -> Set[Secret]:
        return {f"s{i}" for i in range(self.n)}

    def is_complete(self) -> bool:
        return all(self.knowledge[i] == self.all_secrets for i in range(self.n))


def initial_knowledge(n: int) -> Dict[Node, Set[Secret]]:
    """Create the initial knowledge state: node i knows only s_i."""
    if n < 1:
        raise ValueError("n must be positive.")
    return {i: {f"s{i}"} for i in range(n)}


def make_call(knowledge: Dict[Node, Set[Secret]], u: Node, v: Node) -> None:
    """
    Perform one bidirectional call.

    After the call:
        K_u' = K_v' = K_u union K_v
    """
    merged = knowledge[u] | knowledge[v]
    knowledge[u] = set(merged)
    knowledge[v] = set(merged)


def format_node(i: Node) -> str:
    """Human-readable node label."""
    if 0 <= i < 26:
        return chr(ord("A") + i)
    return f"Node{i}"


def format_secret_set(secrets: Iterable[Secret]) -> str:
    """Stable compact printing for a set of secrets."""
    def key(secret: str) -> int:
        return int(secret[1:])
    return "{" + ", ".join(sorted(secrets, key=key)) + "}"


def print_state(knowledge: Dict[Node, Set[Secret]]) -> None:
    """Print all nodes' current knowledge."""
    for i in sorted(knowledge):
        print(f"  {format_node(i)}: {format_secret_set(knowledge[i])}")


def four_core_schedule(n: int) -> List[Call]:
    """
    Build the optimal 2N - 4 call schedule.

    Core nodes:
        A, B, C, D  ->  0, 1, 2, 3

    Phase 1:
        Each peripheral node calls one core node once.
    Phase 2:
        Four core synchronization calls:
            (A,B), (C,D), (A,C), (B,D)
    Phase 3:
        Each peripheral node calls the same core node again to receive all secrets.
    """
    if n < 4:
        raise ValueError("The four-core construction requires n >= 4.")

    core = [0, 1, 2, 3]
    peripherals = list(range(4, n))

    # Assign each peripheral to a core node in round-robin order.
    assignment: Dict[Node, Node] = {
        p: core[index % 4]
        for index, p in enumerate(peripherals)
    }

    upload_calls = [(p, assignment[p]) for p in peripherals]

    core_calls = [
        (0, 1),  # A-B
        (2, 3),  # C-D
        (0, 2),  # A-C
        (1, 3),  # B-D
    ]

    download_calls = [(p, assignment[p]) for p in peripherals]

    return upload_calls + core_calls + download_calls


def three_core_schedule(n: int) -> List[Call]:
    """
    Build a three-core comparison schedule.

    This construction is correct but not optimal for N >= 4.
    It uses:
        (N - 3) upload calls
        3 core calls
        (N - 3) download calls
    Total:
        2N - 3 calls

    Core nodes:
        A, B, C  ->  0, 1, 2
    """
    if n < 3:
        raise ValueError("The three-core construction requires n >= 3.")

    core = [0, 1, 2]
    peripherals = list(range(3, n))

    assignment: Dict[Node, Node] = {
        p: core[index % 3]
        for index, p in enumerate(peripherals)
    }

    upload_calls = [(p, assignment[p]) for p in peripherals]

    core_calls = [
        (0, 1),  # A-B
        (1, 2),  # B-C
        (2, 0),  # C-A
    ]

    download_calls = [(p, assignment[p]) for p in peripherals]

    return upload_calls + core_calls + download_calls


def simulate(
    n: int,
    calls: Sequence[Call],
    *,
    verbose: bool = True,
    title: str = "Simulation",
) -> SimulationResult:
    """Simulate a given call schedule and optionally print each step."""
    knowledge = initial_knowledge(n)

    if verbose:
        print("=" * 72)
        print(title)
        print("=" * 72)
        print(f"N = {n}")
        print("Initial state:")
        print_state(knowledge)
        print()

    for step, (u, v) in enumerate(calls, start=1):
        before_u = set(knowledge[u])
        before_v = set(knowledge[v])
        make_call(knowledge, u, v)

        if verbose:
            print(
                f"Call {step:02d}: "
                f"{format_node(u)} <-> {format_node(v)}"
            )
            print(
                f"  before: {format_node(u)}={format_secret_set(before_u)}, "
                f"{format_node(v)}={format_secret_set(before_v)}"
            )
            print(
                f"  after : {format_node(u)}={format_secret_set(knowledge[u])}, "
                f"{format_node(v)}={format_secret_set(knowledge[v])}"
            )
            print()

    result = SimulationResult(
        n=n,
        calls=list(calls),
        knowledge=knowledge,
    )

    if verbose:
        print("Final state:")
        print_state(knowledge)
        print()
        print(f"Total calls: {result.call_count}")
        print(f"All nodes fully informed: {result.is_complete()}")
        print("=" * 72)
        print()

    return result


def verify_optimal_formula(n: int, result: SimulationResult) -> None:
    """Verify that the four-core construction uses exactly 2N - 4 calls."""
    expected = 2 * n - 4
    if result.call_count != expected:
        raise AssertionError(
            f"Expected {expected} calls, but got {result.call_count}."
        )
    if not result.is_complete():
        raise AssertionError("The final state is not fully synchronized.")


def verify_three_core_formula(n: int, result: SimulationResult) -> None:
    """Verify that the three-core construction uses exactly 2N - 3 calls."""
    expected = 2 * n - 3
    if result.call_count != expected:
        raise AssertionError(
            f"Expected {expected} calls, but got {result.call_count}."
        )
    if not result.is_complete():
        raise AssertionError("The final state is not fully synchronized.")


def print_schedule(calls: Sequence[Call]) -> None:
    """Print a compact list of calls."""
    for index, (u, v) in enumerate(calls, start=1):
        print(f"{index:02d}. {format_node(u)} <-> {format_node(v)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate the Gossip Problem / Telephone Problem."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=8,
        help="Number of nodes. Must be at least 4 for the optimal construction.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the summary, not every call.",
    )
    parser.add_argument(
        "--three-core",
        action="store_true",
        help="Also run the non-optimal three-core comparison construction.",
    )
    parser.add_argument(
        "--schedule-only",
        action="store_true",
        help="Only print the optimal call schedule.",
    )
    args = parser.parse_args()

    n = args.n
    if n < 4:
        raise ValueError("Please use n >= 4.")

    optimal_calls = four_core_schedule(n)

    if args.schedule_only:
        print(f"Optimal four-core schedule for N = {n}:")
        print_schedule(optimal_calls)
        print(f"Total calls: {len(optimal_calls)}")
        print(f"Expected 2N - 4: {2 * n - 4}")
        return

    optimal_result = simulate(
        n,
        optimal_calls,
        verbose=not args.quiet,
        title="Four-Core Optimal Construction",
    )
    verify_optimal_formula(n, optimal_result)

    print("Summary:")
    print(f"  N = {n}")
    print(f"  Four-core call count = {optimal_result.call_count}")
    print(f"  Formula 2N - 4 = {2 * n - 4}")
    print(f"  Complete synchronization verified = {optimal_result.is_complete()}")

    if args.three_core:
        print()
        three_calls = three_core_schedule(n)
        three_result = simulate(
            n,
            three_calls,
            verbose=not args.quiet,
            title="Three-Core Comparison Construction",
        )
        verify_three_core_formula(n, three_result)

        print("Three-core comparison:")
        print(f"  Three-core call count = {three_result.call_count}")
        print(f"  Formula 2N - 3 = {2 * n - 3}")
        print(f"  Complete synchronization verified = {three_result.is_complete()}")
        print(f"  Extra call compared with optimal = {three_result.call_count - optimal_result.call_count}")


if __name__ == "__main__":
    main()
