"""
Algorithmic Solver for the Impossible Puzzle (Freudenthal's Puzzle).
Uses set filtering to simulate the epistemic logic deduction of S and P.
"""

from collections import defaultdict


def get_initial_space() -> list[tuple[int, int]]:
    """
    Generate the initial sample space: 1 < x < y and x + y <= 100.
    """
    pairs = []
    for x in range(2, 100):
        for y in range(x + 1, 100):
            if x + y <= 100:
                pairs.append((x, y))
    return pairs


def filter_1_p_does_not_know(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Step 1: P says "I don't know".
    Eliminate pairs whose product P has only one valid factorization.
    """
    product_map = defaultdict(list)
    for x, y in pairs:
        product_map[x * y].append((x, y))

    # Keep only pairs where the product maps to more than 1 possible pair
    return [pair for pair in pairs if len(product_map[pair[0] * pair[1]]) > 1]


def filter_2_s_already_knew(
    initial_pairs: list[tuple[int, int]], step1_pairs: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """
    Step 2: S says "I already knew that you didn't know".
    S's sum must be one where every possible partition (x, y) results in a non-unique product.
    Eliminate all pairs where x + y is not in this candidate S set.
    """
    step1_set = set(step1_pairs)
    sum_map = defaultdict(list)

    # Map all initial pairs by their sum
    for x, y in initial_pairs:
        sum_map[x + y].append((x, y))

    candidate_s_set = set()
    for current_sum, pairs_with_this_sum in sum_map.items():
        # S is only certain if all pairs summing to current_sum survived Step 1
        if all(p in step1_set for p in pairs_with_this_sum):
            candidate_s_set.add(current_sum)

    # Keep pairs from the initial space whose sum is in the candidate set
    return [(x, y) for (x, y) in initial_pairs if (x + y) in candidate_s_set]


def filter_3_p_now_knows(step2_pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Step 3: P says "Now I know".
    Eliminate all products P that have multiple sum possibilities in the candidate S set.
    """
    product_map = defaultdict(list)
    for x, y in step2_pairs:
        product_map[x * y].append((x, y))

    # Keep only pairs where the product maps to exactly 1 surviving pair
    return [pair for pair in step2_pairs if len(product_map[pair[0] * pair[1]]) == 1]


def filter_4_s_now_knows(step3_pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Step 4: S says "Now I know too".
    Find the S that possesses a uniquely surviving additive partition.
    """
    sum_map = defaultdict(list)
    for x, y in step3_pairs:
        sum_map[x + y].append((x, y))

    # Keep only pairs where the sum maps to exactly 1 surviving pair
    return [pair for pair in step3_pairs if len(sum_map[pair[0] + pair[1]]) == 1]


if __name__ == "__main__":
    print("=== Starting the Impossible Puzzle Solver ===\n")

    # We define the initial sample space as all pairs of numbers (x, y) that satisfy 1 < x < y and x + y <= 100.
    initial_space = get_initial_space()
    print(f"Initial sample space size: {len(initial_space)} pairs")

    # 1. P says "I don't know"
    survivors_1 = filter_1_p_does_not_know(initial_space)
    print(f"After P's 1st statement: {len(survivors_1)} pairs remain")

    # 2. S says "I already knew that you didn't know"
    survivors_2 = filter_2_s_already_knew(initial_space, survivors_1)
    print(f"After S's 1st statement: {len(survivors_2)} pairs remain")

    # 3. P says "Now I know"
    survivors_3 = filter_3_p_now_knows(survivors_2)
    print(f"After P's 2nd statement: {len(survivors_3)} pairs remain")

    # 4. S says "Now I know too"
    final_survivors = filter_4_s_now_knows(survivors_3)
    print(f"After S's 2nd statement: {len(final_survivors)} pairs remain")

    print("\n=== Conclusion ===")
    if len(final_survivors) == 1:
        x, y = final_survivors[0]
        print(f"The unique pair is: x = {x}, y = {y}")
        print(f"At this point, S = {x + y}, P = {x * y}")
    else:
        print("Failed to converge to a unique solution.")
