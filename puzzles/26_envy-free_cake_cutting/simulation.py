"""
1. The cake is represented as the interval [0, 1].
2. Each participant has a private piecewise-constant valuation function.
3. Alice cuts the cake into three equal-value pieces according to Alice.
4. Bob trims his unique favorite piece down to the value of his second favorite.
5. Charlie, Bob, and Alice choose main pieces according to the protocol.
6. If trimming occurred, the trimmed-off remainder is divided by the non-taker,
   then chosen in the order Taker -> Alice -> Non-Taker.
7. The final allocation is checked for envy-freeness from each participant's
   own valuation function.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Interval = Tuple[float, float]
Allocation = Dict[str, List[Interval]]


PARTICIPANTS = ["Alice", "Bob", "Charlie"]
EPS = 1e-9


@dataclass
class ValuationProfile:
    """Piecewise-constant private valuations on the cake interval [0, 1]."""

    cell_values: Dict[str, List[float]]

    @property
    def cells(self) -> int:
        return len(next(iter(self.cell_values.values())))

    @property
    def cell_width(self) -> float:
        return 1.0 / self.cells

    def value_interval(self, person: str, interval: Interval) -> float:
        """Return V_person([a, b]) for a possibly fractional interval."""
        a, b = interval
        if b <= a:
            return 0.0

        n = self.cells
        width = self.cell_width
        values = self.cell_values[person]

        # Clamp tiny floating-point drift.
        a = max(0.0, min(1.0, a))
        b = max(0.0, min(1.0, b))

        start_cell = max(0, min(n - 1, int(math.floor(a / width))))
        end_cell = max(0, min(n - 1, int(math.floor((b - EPS) / width))))

        total = 0.0
        for k in range(start_cell, end_cell + 1):
            cell_a = k * width
            cell_b = (k + 1) * width
            overlap = max(0.0, min(b, cell_b) - max(a, cell_a))
            if overlap > 0:
                total += values[k] * (overlap / width)
        return total

    def value_piece(self, person: str, intervals: Iterable[Interval]) -> float:
        """Return the value of a finite union of intervals."""
        return sum(self.value_interval(person, interval) for interval in intervals)

    def cut_from_left(
        self, person: str, interval: Interval, target_value: float
    ) -> float:
        """
        Find x in [a, b] such that V_person([a, x]) ~= target_value.

        Binary search works because valuations are nonnegative, so the value
        accumulated from left to right is monotone.
        """
        a, b = interval
        whole = self.value_interval(person, interval)

        if target_value <= 0:
            return a
        if target_value >= whole:
            return b

        lo, hi = a, b
        for _ in range(80):
            mid = (lo + hi) / 2.0
            current = self.value_interval(person, (a, mid))
            if current < target_value:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2.0


@dataclass
class ProtocolResult:
    allocation: Allocation
    stage_one_allocation: Allocation
    trimmed_piece_owner: Optional[str]
    non_taker: Optional[str]
    trimmed_remainder: Optional[Interval]
    alice_cuts: Tuple[float, float]
    bob_trimmed: bool
    log: List[str]


def generate_random_profile(seed: int, cells: int) -> ValuationProfile:
    """
    Generate independent private valuations.

    Each person gets positive random cell weights, then the weights are
    normalized so each person's value for the whole cake is exactly 1.
    """
    rng = random.Random(seed)
    cell_values: Dict[str, List[float]] = {}

    for person in PARTICIPANTS:
        raw = [rng.expovariate(1.0) + 0.05 for _ in range(cells)]
        total = sum(raw)
        cell_values[person] = [x / total for x in raw]

    return ValuationProfile(cell_values=cell_values)


def format_interval(interval: Interval) -> str:
    return f"[{interval[0]:.4f}, {interval[1]:.4f}]"


def format_intervals(intervals: Sequence[Interval]) -> str:
    return " + ".join(format_interval(x) for x in intervals) if intervals else "∅"


def choose_favorite(
    profile: ValuationProfile,
    person: str,
    candidates: Sequence[int],
    pieces: Sequence[Interval],
) -> int:
    """Choose the candidate piece index with maximum value for the given person."""
    return max(candidates, key=lambda idx: profile.value_interval(person, pieces[idx]))


def selfridge_conway(profile: ValuationProfile) -> ProtocolResult:
    """Execute the Selfridge-Conway protocol on one valuation profile."""
    log: List[str] = []

    # Stage 1. Alice cuts [0, 1] into three equal-value pieces according to Alice.
    x1 = profile.cut_from_left("Alice", (0.0, 1.0), 1.0 / 3.0)
    x2 = profile.cut_from_left("Alice", (x1, 1.0), 1.0 / 3.0)
    original_pieces: List[Interval] = [(0.0, x1), (x1, x2), (x2, 1.0)]

    log.append("Stage 1: Alice cuts the cake into three pieces she values equally.")
    for idx, piece in enumerate(original_pieces):
        log.append(
            f"  P{idx + 1} = {format_interval(piece)}, "
            f"Alice value = {profile.value_interval('Alice', piece):.6f}"
        )

    # Bob evaluates and possibly trims his unique favorite piece.
    bob_values = [profile.value_interval("Bob", piece) for piece in original_pieces]
    sorted_indices = sorted(range(3), key=lambda i: bob_values[i], reverse=True)
    largest_idx = sorted_indices[0]
    second_idx = sorted_indices[1]
    largest_value = bob_values[largest_idx]
    second_value = bob_values[second_idx]

    main_pieces = list(original_pieces)
    trimmed_remainder: Optional[Interval] = None
    trimmed_piece_idx: Optional[int] = None
    bob_trimmed = False

    log.append("\nBob evaluates Alice's three pieces:")
    for idx, value in enumerate(bob_values):
        log.append(f"  Bob value for P{idx + 1}: {value:.6f}")

    if largest_value > second_value + EPS:
        bob_trimmed = True
        trimmed_piece_idx = largest_idx
        a, b = original_pieces[largest_idx]
        trim_point = profile.cut_from_left("Bob", (a, b), second_value)
        main_pieces[largest_idx] = (a, trim_point)
        trimmed_remainder = (trim_point, b)

        log.append(f"\nBob has a unique favorite P{largest_idx + 1}, so he trims it.")
        log.append(
            f"  Trimmed main piece: {format_interval(main_pieces[largest_idx])}, "
            f"Bob value = {profile.value_interval('Bob', main_pieces[largest_idx]):.6f}"
        )
        log.append(
            f"  Trimmed-off remainder: {format_interval(trimmed_remainder)}, "
            f"Bob value = {profile.value_interval('Bob', trimmed_remainder):.6f}"
        )
    else:
        log.append("\nBob has no unique favorite piece, so no trimming is needed.")

    # Charlie chooses first among the main pieces.
    remaining = [0, 1, 2]
    allocation_main: Allocation = {person: [] for person in PARTICIPANTS}

    charlie_choice = choose_favorite(profile, "Charlie", remaining, main_pieces)
    allocation_main["Charlie"] = [main_pieces[charlie_choice]]
    remaining.remove(charlie_choice)
    log.append(f"\nCharlie chooses P{charlie_choice + 1}.")

    # Bob chooses second. If Charlie did not take the trimmed piece, Bob must take it.
    if (
        bob_trimmed
        and trimmed_piece_idx is not None
        and charlie_choice != trimmed_piece_idx
    ):
        bob_choice = trimmed_piece_idx
        log.append(
            f"Bob is required to take the trimmed piece P{bob_choice + 1}, "
            "because Charlie did not take it."
        )
    else:
        bob_choice = choose_favorite(profile, "Bob", remaining, main_pieces)
        log.append(f"Bob chooses P{bob_choice + 1} from the remaining pieces.")

    allocation_main["Bob"] = [main_pieces[bob_choice]]
    remaining.remove(bob_choice)

    # Alice takes the final main piece.
    alice_choice = remaining[0]
    allocation_main["Alice"] = [main_pieces[alice_choice]]
    log.append(f"Alice receives the remaining P{alice_choice + 1}.")

    allocation_final: Allocation = {
        person: list(intervals) for person, intervals in allocation_main.items()
    }

    trimmed_piece_owner: Optional[str] = None
    non_taker: Optional[str] = None

    # Stage 2. Allocate the trimmed-off remainder, if it exists.
    if bob_trimmed and trimmed_remainder is not None and trimmed_piece_idx is not None:
        if charlie_choice == trimmed_piece_idx:
            trimmed_piece_owner = "Charlie"
            non_taker = "Bob"
        else:
            trimmed_piece_owner = "Bob"
            non_taker = "Charlie"

        log.append("\nStage 2: allocate the trimmed-off remainder.")
        log.append(f"  Taker T = {trimmed_piece_owner}")
        log.append(f"  Non-taker NT = {non_taker}")

        r_a, r_b = trimmed_remainder
        total_r_value_for_nt = profile.value_interval(non_taker, trimmed_remainder)
        r1 = profile.cut_from_left(
            non_taker, trimmed_remainder, total_r_value_for_nt / 3.0
        )
        r2 = profile.cut_from_left(non_taker, (r1, r_b), total_r_value_for_nt / 3.0)

        remainder_pieces: List[Interval] = [(r_a, r1), (r1, r2), (r2, r_b)]

        log.append(f"{non_taker} cuts the remainder into three equal-value parts:")
        for idx, piece in enumerate(remainder_pieces):
            log.append(
                f"  R{idx + 1} = {format_interval(piece)}, "
                f"{non_taker} value = {profile.value_interval(non_taker, piece):.6f}"
            )

        rem_remaining = [0, 1, 2]

        taker_choice = choose_favorite(
            profile, trimmed_piece_owner, rem_remaining, remainder_pieces
        )
        allocation_final[trimmed_piece_owner].append(remainder_pieces[taker_choice])
        rem_remaining.remove(taker_choice)
        log.append(f"{trimmed_piece_owner} chooses R{taker_choice + 1} first.")

        alice_rem_choice = choose_favorite(
            profile, "Alice", rem_remaining, remainder_pieces
        )
        allocation_final["Alice"].append(remainder_pieces[alice_rem_choice])
        rem_remaining.remove(alice_rem_choice)
        log.append(f"Alice chooses R{alice_rem_choice + 1} second.")

        nt_choice = rem_remaining[0]
        allocation_final[non_taker].append(remainder_pieces[nt_choice])
        log.append(f"{non_taker} receives R{nt_choice + 1} last.")
    else:
        log.append(
            "\nNo trimmed-off remainder exists, so the protocol ends after Stage 1."
        )

    return ProtocolResult(
        allocation=allocation_final,
        stage_one_allocation=allocation_main,
        trimmed_piece_owner=trimmed_piece_owner,
        non_taker=non_taker,
        trimmed_remainder=trimmed_remainder,
        alice_cuts=(x1, x2),
        bob_trimmed=bob_trimmed,
        log=log,
    )


def envy_matrix(
    profile: ValuationProfile, allocation: Allocation
) -> Dict[str, Dict[str, float]]:
    """Return matrix M[i][j] = V_i(final share of j)."""
    matrix: Dict[str, Dict[str, float]] = {}
    for evaluator in PARTICIPANTS:
        matrix[evaluator] = {}
        for owner in PARTICIPANTS:
            matrix[evaluator][owner] = profile.value_piece(evaluator, allocation[owner])
    return matrix


def is_envy_free(
    profile: ValuationProfile,
    allocation: Allocation,
    tolerance: float = 1e-7,
) -> Tuple[bool, List[str]]:
    """Check V_i(X_i) >= V_i(X_j) for all i, j."""
    matrix = envy_matrix(profile, allocation)
    violations: List[str] = []

    for evaluator in PARTICIPANTS:
        own_value = matrix[evaluator][evaluator]
        for other in PARTICIPANTS:
            other_value = matrix[evaluator][other]
            if other_value > own_value + tolerance:
                violations.append(
                    f"{evaluator} envies {other}: "
                    f"own={own_value:.9f}, other={other_value:.9f}"
                )

    return len(violations) == 0, violations


def find_profile_with_trimming(
    seed: int, cells: int, max_attempts: int = 100
) -> Tuple[int, ValuationProfile]:
    """
    Try nearby seeds until Bob trims.

    Trimming is the more interesting case because it exercises both stages.
    The fallback still returns a valid profile if no trimming case is found.
    """
    fallback_profile = generate_random_profile(seed, cells)
    for offset in range(max_attempts):
        current_seed = seed + offset
        profile = generate_random_profile(current_seed, cells)
        original_x1 = profile.cut_from_left("Alice", (0.0, 1.0), 1.0 / 3.0)
        original_x2 = profile.cut_from_left("Alice", (original_x1, 1.0), 1.0 / 3.0)
        pieces = [(0.0, original_x1), (original_x1, original_x2), (original_x2, 1.0)]
        bob_values = [profile.value_interval("Bob", piece) for piece in pieces]
        values_desc = sorted(bob_values, reverse=True)
        if values_desc[0] > values_desc[1] + EPS:
            return current_seed, profile
    return seed, fallback_profile


def print_result(seed: int, profile: ValuationProfile, result: ProtocolResult) -> None:
    """Pretty-print protocol trace and envy-free verification."""
    print("=" * 72)
    print("Selfridge-Conway 3-Person Envy-Free Cake-Cutting Simulation")
    print("=" * 72)
    print(f"Seed: {seed}")
    print(
        f"Valuation model: piecewise-constant private values over {profile.cells} cells"
    )
    print()

    for line in result.log:
        print(line)

    print("\nFinal allocation:")
    for person in PARTICIPANTS:
        print(f"  {person}: {format_intervals(result.allocation[person])}")

    matrix = envy_matrix(profile, result.allocation)
    print("\nValue matrix: evaluator's value for each person's final share")
    header = "Evaluator".ljust(12) + "".join(owner.rjust(12) for owner in PARTICIPANTS)
    print(header)
    print("-" * len(header))
    for evaluator in PARTICIPANTS:
        row = evaluator.ljust(12)
        for owner in PARTICIPANTS:
            row += f"{matrix[evaluator][owner]:12.6f}"
        print(row)

    ok, violations = is_envy_free(profile, result.allocation)
    print("\nEnvy-free check:")
    if ok:
        print(
            "  PASS: no participant values another person's final share more than their own."
        )
    else:
        print("  FAIL: envy detected.")
        for item in violations:
            print(f"  - {item}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate the Selfridge-Conway envy-free cake-cutting protocol."
    )
    parser.add_argument("--seed", type=int, default=11, help="random seed")
    parser.add_argument("--cells", type=int, default=80, help="number of value cells")
    parser.add_argument(
        "--allow-no-trim",
        action="store_true",
        help="use the exact seed even if Bob does not need to trim",
    )
    args = parser.parse_args()

    if args.cells < 10:
        raise ValueError("Please use at least 10 cells for a meaningful simulation.")

    if args.allow_no_trim:
        seed = args.seed
        profile = generate_random_profile(args.seed, args.cells)
    else:
        seed, profile = find_profile_with_trimming(args.seed, args.cells)

    result = selfridge_conway(profile)
    print_result(seed, profile, result)


if __name__ == "__main__":
    main()
