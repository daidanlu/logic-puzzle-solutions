import numpy as np

def generate_random_club(N):
    """
    Generate a random club represented as a binary vector of length N.
    1 means the citizen is in the club, 0 means they are not.
    """
    return np.random.randint(0, 2, N)

def run_oddtown_simulation(N=10, max_attempts=50000):
    print("=== Oddtown Theorem Simulation ===\n")
    print(f"Total Population (N) : {N}")
    print(f"Max Random Attempts  : {max_attempts}\n")

    valid_clubs = []

    for attempt in range(max_attempts):
        candidate = generate_random_club(N)

        # Rule 1: Oddtown Self-Rule (Club size must be odd)
        if np.sum(candidate) % 2 != 1:
            continue

        # Rule 2: Even Intersection Rule (Dot product with all existing clubs must be even)
        is_valid = True
        for existing_club in valid_clubs:
            intersection_size = np.dot(candidate, existing_club)
            if intersection_size % 2 != 0:
                is_valid = False
                break

        if is_valid:
            valid_clubs.append(candidate)
            print(f"[Club Approved #{len(valid_clubs)}] Members: {candidate}")

            # Once we hit N, the theoretical ceiling is reached.
            if len(valid_clubs) == N:
                print(f"\n[System Alert] Theoretical ceiling reached (M = N = {N}).")
                print("Burning remaining attempts to prove no more clubs can exist...")

    print("\n" + "-" * 50)
    print("=== Simulation Results ===")
    
    M = len(valid_clubs)
    print(f"Total Attempts Evaluated : {max_attempts}")
    print(f"Final Number of Clubs (M): {M}")

    if M > 0:
        # Construct the Incidence Matrix A (M rows, N columns)
        A = np.array(valid_clubs)
        print("\n=== Incidence Matrix A (M x N) ===")
        print(A)

        # Execute the core algebraic proof: A * A^T (mod 2)
        A_AT = np.dot(A, A.T) % 2
        print(f"\n=== Verification of A * A^T (mod 2) ===")
        print(A_AT)

        # Check if the result is a perfect Identity Matrix
        is_identity = np.array_equal(A_AT, np.eye(M))
        print(f"\nIs A * A^T (mod 2) a perfect Identity Matrix? -> {is_identity}")

    # The ultimate mathematical assertion
    assert M <= N, "Physics broken: M exceeded N!"
    print("\nMathematical Theorem Verified: M can never exceed N.")

if __name__ == "__main__":
    # Let's test with a small town of 10 people and 50,000 random club proposals
    run_oddtown_simulation(N=10, max_attempts=50000)