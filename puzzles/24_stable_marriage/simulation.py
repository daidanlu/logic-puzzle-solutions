"""
Stable Marriage Problem Simulation
Gale-Shapley Algorithm

The code simulates the proof idea:
1. Convergence: each proposer proposes to each receiver at most once.
2. Perfect matching: nobody remains unmatched at termination.
3. Stability: the final matching contains no blocking pair.
"""

from collections import deque
from typing import Dict, List, Tuple, Optional

Person = str
Preferences = Dict[Person, List[Person]]
Matching = Dict[Person, Person]


def build_rank_map(
    receiver_preferences: Preferences,
) -> Dict[Person, Dict[Person, int]]:
    """
    Convert each receiver's preference list into a ranking table.
    Smaller rank means more preferred.

    This makes each comparison O(1), so the whole algorithm is O(N^2).
    """
    rank = {}
    for receiver, preference_list in receiver_preferences.items():
        rank[receiver] = {proposer: i for i, proposer in enumerate(preference_list)}
    return rank


def gale_shapley(
    proposer_preferences: Preferences,
    receiver_preferences: Preferences,
    verbose: bool = True,
) -> Tuple[Matching, int]:
    """
    Run the Gale-Shapley algorithm with proposers as the active side.

    Returns:
        proposer_to_receiver: final matching from proposers to receivers
        proposal_count: total number of proposals made
    """
    proposers = list(proposer_preferences.keys())
    n = len(proposers)

    receiver_rank = build_rank_map(receiver_preferences)

    next_choice_index: Dict[Person, int] = {a: 0 for a in proposers}

    proposer_to_receiver: Dict[Person, Optional[Person]] = {a: None for a in proposers}
    receiver_to_proposer: Dict[Person, Optional[Person]] = {
        b: None for b in receiver_preferences
    }

    free_proposers = deque(proposers)
    proposal_count = 0

    if verbose:
        print("Initial state: everyone is free.\n")

    while free_proposers:
        a = free_proposers.popleft()

        if next_choice_index[a] >= n:
            continue

        b = proposer_preferences[a][next_choice_index[a]]
        next_choice_index[a] += 1
        proposal_count += 1

        current = receiver_to_proposer[b]

        if verbose:
            print(f"Proposal {proposal_count}: {a} proposes to {b}.")

        if current is None:
            proposer_to_receiver[a] = b
            receiver_to_proposer[b] = a
            if verbose:
                print(f"  {b} is free, so {b} accepts {a}.\n")
        else:
            if receiver_rank[b][a] < receiver_rank[b][current]:
                proposer_to_receiver[current] = None
                free_proposers.append(current)

                proposer_to_receiver[a] = b
                receiver_to_proposer[b] = a

                if verbose:
                    print(f"  {b} prefers {a} over {current}.")
                    print(
                        f"  {current} becomes free, and {b} is now matched with {a}.\n"
                    )
            else:
                if next_choice_index[a] < n:
                    free_proposers.append(a)
                if verbose:
                    print(
                        f"  {b} prefers current partner {current}, so {b} rejects {a}.\n"
                    )

    final_matching: Matching = {
        a: b for a, b in proposer_to_receiver.items() if b is not None
    }
    return final_matching, proposal_count


def is_perfect_matching(matching: Matching, n: int) -> bool:
    """
    Check whether the matching contains exactly N proposer-receiver pairs
    and every receiver appears exactly once.
    """
    return len(matching) == n and len(set(matching.values())) == n


def find_blocking_pairs(
    matching: Matching,
    proposer_preferences: Preferences,
    receiver_preferences: Preferences,
) -> List[Tuple[Person, Person]]:
    """
    Find all blocking pairs in the final matching.

    A pair (a, b) is blocking if:
    1. a is not matched with b;
    2. a prefers b over his current partner;
    3. b prefers a over her current partner.
    """
    receiver_rank = build_rank_map(receiver_preferences)

    receiver_to_proposer = {b: a for a, b in matching.items()}
    blocking_pairs = []

    for a, current_b in matching.items():
        for b in proposer_preferences[a]:
            if b == current_b:
                break

            current_a = receiver_to_proposer[b]

            if receiver_rank[b][a] < receiver_rank[b][current_a]:
                blocking_pairs.append((a, b))

    return blocking_pairs


def print_matching(matching: Matching) -> None:
    print("Final matching:")
    for a in sorted(matching):
        print(f"  {a} -> {matching[a]}")
    print()


def run_example() -> None:
    proposer_preferences = {
        "A1": ["B1", "B2", "B3", "B4"],
        "A2": ["B1", "B3", "B2", "B4"],
        "A3": ["B2", "B1", "B3", "B4"],
        "A4": ["B2", "B3", "B4", "B1"],
    }

    receiver_preferences = {
        "B1": ["A3", "A1", "A2", "A4"],
        "B2": ["A2", "A4", "A1", "A3"],
        "B3": ["A1", "A2", "A3", "A4"],
        "B4": ["A4", "A3", "A2", "A1"],
    }

    n = len(proposer_preferences)

    print("Before running Gale-Shapley")
    print("-----------------------------")
    print(f"N = {n}")
    print(f"Maximum possible proposals: N^2 = {n * n}\n")

    matching, proposal_count = gale_shapley(
        proposer_preferences,
        receiver_preferences,
        verbose=True,
    )

    print("After running Gale-Shapley")
    print("----------------------------")
    print_matching(matching)

    print("Proof checks")
    print("------------")
    print(f"Total proposals: {proposal_count}")
    print(f"Proposal bound N^2: {n * n}")
    print(f"Convergence check: {proposal_count <= n * n}")

    perfect = is_perfect_matching(matching, n)
    print(f"Perfect matching check: {perfect}")

    blocking_pairs = find_blocking_pairs(
        matching,
        proposer_preferences,
        receiver_preferences,
    )
    print(f"Blocking pairs: {blocking_pairs}")
    print(f"Stability check: {len(blocking_pairs) == 0}")


if __name__ == "__main__":
    run_example()
