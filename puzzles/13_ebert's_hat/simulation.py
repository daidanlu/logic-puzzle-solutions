import itertools


def is_death_set(state):
    """
    Determines if the current state belongs to the 'Death Set' W (i.e., a Hamming Code codeword).
    Using 0-based indexing: P1=0, P2=1, P3=2, P4=3, P5=4, P6=5, P7=6
    """
    # Ring A: {1, 2, 3, 5} -> Indices {0, 1, 2, 4}
    ring_A_even = (state[0] + state[1] + state[2] + state[4]) % 2 == 0

    # Ring B: {1, 2, 4, 6} -> Indices {0, 1, 3, 5}
    ring_B_even = (state[0] + state[1] + state[3] + state[5]) % 2 == 0

    # Ring C: {1, 3, 4, 7} -> Indices {0, 2, 3, 6}
    ring_C_even = (state[0] + state[2] + state[3] + state[6]) % 2 == 0

    # A state is a Codeword (Death Set) ONLY if all three parity checks are even
    return ring_A_even and ring_B_even and ring_C_even


def prisoner_action(prisoner_index, true_state):
    """
    Action Axiom: The prisoner deduces their action based on the hats of the other 6.
    Returns: 0 (Guess Black), 1 (Guess White), -1 (Pass)
    """
    # Hypothesis 1: Assume my own hat is Black (0)
    state_if_0 = list(true_state)
    state_if_0[prisoner_index] = 0

    # Hypothesis 2: Assume my own hat is White (1)
    state_if_1 = list(true_state)
    state_if_1[prisoner_index] = 1

    # Deduction Rules
    if is_death_set(state_if_0):
        # If assuming Black constructs the Death Set, I firmly believe I must be White.
        return 1
    elif is_death_set(state_if_1):
        # If assuming White constructs the Death Set, I firmly believe I must be Black.
        return 0
    else:
        # Neither assumption constructs the Death Set. I lack geometric deduction criteria.
        return -1


def run_simulation():
    total_states = 128
    wins = 0
    losses = 0

    print("=== Ebert's Hat Problem: (7,4,3) Hamming Code Simulation ===\n")

    # Generate all 128 possible hat combinations (0: Black, 1: White)
    all_possible_states = list(itertools.product([0, 1], repeat=7))

    for state in all_possible_states:
        guesses = []

        for i in range(7):
            guesses.append(prisoner_action(i, state))

        correct_guesses = 0
        wrong_guesses = 0

        for i in range(7):
            if guesses[i] == -1:
                continue  # Prisoner passed
            elif guesses[i] == state[i]:
                correct_guesses += 1
            else:
                wrong_guesses += 1

        # Evaluate ultimate survival conditions
        # Win condition: At least 1 correct guess and exactly 0 wrong guesses
        if wrong_guesses == 0 and correct_guesses > 0:
            wins += 1
        else:
            losses += 1
            if is_death_set(state):
                print(
                    f"[Death Set Triggered] True State: {state} | Guesses: {guesses} (All 7 guessed WRONG)"
                )

    print("-" * 60)
    print("=== Simulation Results ===")
    print(f"Total Configurations : {total_states}")
    print(f"Winning Scenarios    : {wins}")
    print(f"Losing Scenarios     : {losses} (Exactly matches the 16 Codewords)")
    print(f"Calculated Win Rate  : {wins / total_states * 100:.2f}%")

    assert wins == 112, "Physics broken: Wins should be exactly 112."
    assert losses == 16, "Physics broken: Losses should be exactly 16."


if __name__ == "__main__":
    run_simulation()
