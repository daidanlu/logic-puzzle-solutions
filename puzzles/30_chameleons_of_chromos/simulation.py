"""
This script models the three-color chameleon state machine:
    RG -> BB: (R, G, B) -> (R-1, G-1, B+2)
    RB -> GG: (R, G, B) -> (R-1, G+2, B-1)
    GB -> RR: (R, G, B) -> (R+2, G-1, B-1)

It demonstrates two points from the proof:
1. The original state (13, 15, 17) cannot reach any monochromatic state.
2. After adding one red chameleon, (14, 15, 17) can reach the all-green state
   through the explicit path:
       one GB -> RR collision, then sixteen RB -> GG collisions.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True, order=True)
class State:
    """A state is the number of red, green, and blue chameleons."""

    red: int
    green: int
    blue: int

    @property
    def total(self) -> int:
        return self.red + self.green + self.blue

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def is_monochromatic(self) -> bool:
        """Return True iff exactly one color has all chameleons."""
        return sum(x > 0 for x in self.as_tuple()) == 1

    def invariant_mod3(self) -> Tuple[int, int, int]:
        """
        Return the modulo-3 invariant:
            (R-G mod 3, G-B mod 3, B-R mod 3).
        """
        r, g, b = self.as_tuple()
        return ((r - g) % 3, (g - b) % 3, (b - r) % 3)

    def possible_monochromatic_targets_by_congruence(self) -> List[Tuple[str, "State"]]:
        """
        Necessary congruence test for each monochromatic target.
        To reach:
        - all red:   G == B (mod 3)
        - all green: R == B (mod 3)
        - all blue:  R == G (mod 3)
        """
        n = self.total
        targets: List[Tuple[str, State]] = []

        if self.green % 3 == self.blue % 3:
            targets.append(("all red", State(n, 0, 0)))

        if self.red % 3 == self.blue % 3:
            targets.append(("all green", State(0, n, 0)))

        if self.red % 3 == self.green % 3:
            targets.append(("all blue", State(0, 0, n)))

        return targets


def legal_next_states(state: State) -> Iterable[Tuple[str, State]]:
    """
    Generate all effective legal transitions from a state.
    Same-color meetings are ignored because they do not change the state.
    """
    r, g, b = state.as_tuple()

    if r > 0 and g > 0:
        yield "RG -> BB", State(r - 1, g - 1, b + 2)

    if r > 0 and b > 0:
        yield "RB -> GG", State(r - 1, g + 2, b - 1)

    if g > 0 and b > 0:
        yield "GB -> RR", State(r + 2, g - 1, b - 1)


def apply_collision(state: State, collision: str) -> State:
    """Apply one named collision: RG, RB, or GB."""
    collision = collision.upper()
    r, g, b = state.as_tuple()

    if collision == "RG":
        if r <= 0 or g <= 0:
            raise ValueError(f"Illegal RG collision from state {state}")
        return State(r - 1, g - 1, b + 2)

    if collision == "RB":
        if r <= 0 or b <= 0:
            raise ValueError(f"Illegal RB collision from state {state}")
        return State(r - 1, g + 2, b - 1)

    if collision == "GB":
        if g <= 0 or b <= 0:
            raise ValueError(f"Illegal GB collision from state {state}")
        return State(r + 2, g - 1, b - 1)

    raise ValueError("collision must be one of: RG, RB, GB")


def monochromatic_targets(total: int) -> List[State]:
    return [State(total, 0, 0), State(0, total, 0), State(0, 0, total)]


def bfs_path_to_any_target(
    start: State,
    targets: Iterable[State],
) -> Tuple[Optional[List[Tuple[str, State]]], int]:
    """
    Breadth-first search over the finite state space.
    Returns:
        (path, visited_count)
    path is a list of (action, new_state), or None if no target is reachable.
    """
    target_set = set(targets)
    queue = deque([start])
    parent: Dict[State, Tuple[Optional[State], Optional[str]]] = {start: (None, None)}

    while queue:
        current = queue.popleft()

        if current in target_set:
            path: List[Tuple[str, State]] = []
            while parent[current][0] is not None:
                previous, action = parent[current]
                assert previous is not None and action is not None
                path.append((action, current))
                current = previous
            path.reverse()
            return path, len(parent)

        for action, next_state in legal_next_states(current):
            if next_state not in parent:
                parent[next_state] = (current, action)
                queue.append(next_state)

    return None, len(parent)


def verify_invariant_along_path(start: State, path: List[Tuple[str, State]]) -> None:
    """Assert that the modulo-3 invariant is unchanged along a path."""
    expected = start.invariant_mod3()
    for _, state in path:
        assert (
            state.invariant_mod3() == expected
        ), f"Invariant changed: expected {expected}, got {state.invariant_mod3()}"


def constructed_readme_path() -> List[Tuple[str, State]]:
    """
    The explicit path described in the README:
    (14, 15, 17)
      --GB--> (16, 14, 16)
      --RB repeated 16 times--> (0, 46, 0)
    """
    state = State(14, 15, 17)
    path: List[Tuple[str, State]] = []

    state = apply_collision(state, "GB")
    path.append(("GB -> RR", state))

    for _ in range(16):
        state = apply_collision(state, "RB")
        path.append(("RB -> GG", state))

    return path


def print_state_report(state: State) -> None:
    print(f"State: {state.as_tuple()}, total = {state.total}")
    print(f"Modulo-3 invariant (R-G, G-B, B-R): {state.invariant_mod3()}")

    targets = state.possible_monochromatic_targets_by_congruence()
    if targets:
        print("Targets allowed by the necessary congruence test:")
        for name, target in targets:
            print(f"  - {name}: {target.as_tuple()}")
    else:
        print("Targets allowed by the necessary congruence test: none")


def print_path(path: List[Tuple[str, State]], max_lines: int = 8) -> None:
    """
    Print a path compactly.

    If the path is long, show the first few and last few steps.
    """
    print(f"Path length: {len(path)} collision(s)")

    if len(path) <= max_lines:
        for i, (action, state) in enumerate(path, start=1):
            print(f"  {i:02d}. {action:8s} -> {state.as_tuple()}")
        return

    head = max_lines // 2
    tail = max_lines - head

    for i, (action, state) in enumerate(path[:head], start=1):
        print(f"  {i:02d}. {action:8s} -> {state.as_tuple()}")

    print("  ...")

    start_index = len(path) - tail + 1
    for i, (action, state) in enumerate(path[-tail:], start=start_index):
        print(f"  {i:02d}. {action:8s} -> {state.as_tuple()}")


def demo_original_state() -> None:
    print("=" * 72)
    print("Demo 1: original state (13, 15, 17)")
    print("=" * 72)

    start = State(13, 15, 17)
    print_state_report(start)

    path, visited_count = bfs_path_to_any_target(
        start,
        monochromatic_targets(start.total),
    )

    print(f"BFS visited {visited_count} reachable state(s).")
    if path is None:
        print("Result: no monochromatic state is reachable.")
    else:
        print("Result: a monochromatic state is reachable.")
        print_path(path)

    print()


def demo_perturbed_state() -> None:
    print("=" * 72)
    print("Demo 2: perturbed state (14, 15, 17)")
    print("=" * 72)

    start = State(14, 15, 17)
    print_state_report(start)

    print("\nExplicit README construction:")
    path = constructed_readme_path()
    verify_invariant_along_path(start, path)
    print_path(path)
    print(f"Final state: {path[-1][1].as_tuple()}")

    print("\nBFS confirmation:")
    bfs_path, visited_count = bfs_path_to_any_target(
        start,
        monochromatic_targets(start.total),
    )

    print(f"BFS visited {visited_count} reachable state(s).")
    if bfs_path is None:
        print("Result: no monochromatic state is reachable.")
    else:
        verify_invariant_along_path(start, bfs_path)
        print("Result: a monochromatic state is reachable.")
        print_path(bfs_path)
        print(f"Final state: {bfs_path[-1][1].as_tuple()}")

    print()


def main() -> None:
    demo_original_state()
    demo_perturbed_state()


if __name__ == "__main__":
    main()
