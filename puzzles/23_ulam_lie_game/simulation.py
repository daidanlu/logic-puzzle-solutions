import math
import numpy as np


def choose_balanced_question(conflicts, remaining_questions):
    """
    Choose a subset A so that the yes-branch and no-branch
    have nearly equal Berlekamp weight.

    conflicts[x] = 0 means candidate x is in the whitelist.
    conflicts[x] = 1 means candidate x is in the graylist.
    conflicts[x] = 2 means candidate x is eliminated.

    remaining_questions is the number of questions before asking
    the current question.
    """
    k = remaining_questions

    whites = np.flatnonzero(conflicts == 0)
    grays = np.flatnonzero(conflicts == 1)

    w = len(whites)
    g = len(grays)

    total_weight = (k + 1) * w + g
    target = total_weight / 2.0

    # If A is empty, then after a "yes" answer:
    # every white candidate outside A becomes gray.
    # So the base yes-weight is w.
    base_yes_weight = w

    possible_white_counts = set()

    if k > 1:
        approx = int(round((target - base_yes_weight) / (k - 1)))

        for value in [
            0,
            w,
            approx - 3,
            approx - 2,
            approx - 1,
            approx,
            approx + 1,
            approx + 2,
            approx + 3,
        ]:
            if 0 <= value <= w:
                possible_white_counts.add(value)
    else:
        possible_white_counts.add(0)

    best_choice = None

    for white_count in possible_white_counts:
        current_yes_weight = base_yes_weight + (k - 1) * white_count
        remaining_needed = target - current_yes_weight

        gray_candidates = [
            0,
            g,
            math.floor(remaining_needed),
            round(remaining_needed),
            math.ceil(remaining_needed),
        ]

        for gray_count in gray_candidates:
            gray_count = int(max(0, min(g, gray_count)))

            yes_weight = base_yes_weight + (k - 1) * white_count + gray_count

            difference = abs(yes_weight - target)

            if best_choice is None or difference < best_choice[0]:
                best_choice = (
                    difference,
                    white_count,
                    gray_count,
                    yes_weight,
                )

    _, white_count, gray_count, yes_weight = best_choice

    in_A = np.zeros_like(conflicts, dtype=bool)

    if white_count > 0:
        in_A[whites[:white_count]] = True

    if gray_count > 0:
        in_A[grays[:gray_count]] = True

    return in_A, total_weight, yes_weight


def simulate_ulam_game(
    N=1_000_000,
    total_questions=25,
    secret=123456,
    lie_turn=7,
    verbose=True,
):
    """
    Simulate Ulam's Game with at most one lie.

    N:
        The search range is 1, 2, ..., N.

    total_questions:
        Number of yes/no questions allowed.

    secret:
        The true number chosen by the oracle.

    lie_turn:
        The turn on which the oracle lies.
        Use None if the oracle never lies.

    verbose:
        Whether to print the search process.
    """

    conflicts = np.zeros(N + 1, dtype=np.int8)

    # Ignore index 0, since candidates are 1 to N.
    conflicts[0] = 2

    for turn in range(1, total_questions + 1):
        remaining_questions = total_questions - turn + 1

        A, total_weight, yes_weight = choose_balanced_question(
            conflicts,
            remaining_questions,
        )

        truthful_answer = bool(A[secret])

        if lie_turn == turn:
            observed_answer = not truthful_answer
            lied = True
        else:
            observed_answer = truthful_answer
            lied = False

        live_candidates = conflicts <= 1

        if observed_answer:
            # Oracle says: secret is in A.
            # Candidates outside A become less credible.
            inconsistent = (~A) & live_candidates
        else:
            # Oracle says: secret is not in A.
            # Candidates inside A become less credible.
            inconsistent = A & live_candidates

        conflicts[inconsistent] += 1
        conflicts[conflicts > 1] = 2

        white_count = int(np.sum(conflicts == 0))
        gray_count = int(np.sum(conflicts == 1))

        # After asking this question, one fewer question remains.
        new_weight = remaining_questions * white_count + gray_count

        if verbose:
            print(f"Turn {turn}")
            print("-" * 40)
            print(f"Remaining questions before asking: {remaining_questions}")
            print(f"Total weight before question: {total_weight}")
            print(f"Yes-branch weight: {yes_weight}")
            print(f"No-branch weight: {total_weight - yes_weight}")
            print(f"Oracle answer: {'YES' if observed_answer else 'NO'}")
            print(f"Truthful answer: {'YES' if truthful_answer else 'NO'}")
            print(f"Lied this turn? {lied}")
            print(f"White candidates: {white_count}")
            print(f"Gray candidates: {gray_count}")
            print(f"Weight after question: {new_weight}")
            print()

    candidates = np.flatnonzero((conflicts <= 1) & (np.arange(N + 1) > 0))

    print("=" * 40)
    print("Final result")
    print("=" * 40)
    print(f"Secret number: {secret}")
    print(f"Surviving candidates: {candidates}")
    print(f"Number of survivors: {len(candidates)}")

    if len(candidates) == 1 and candidates[0] == secret:
        print("Success: the true number was uniquely identified.")
    else:
        print("Failure: the strategy did not isolate the true number.")


if __name__ == "__main__":
    simulate_ulam_game(
        N=1_000_000,
        total_questions=25,
        secret=123456,
        lie_turn=7,
        verbose=True,
    )
