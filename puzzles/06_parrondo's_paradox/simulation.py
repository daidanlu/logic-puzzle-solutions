"""
Monte Carlo Markov Chain Simulator for Parrondo's Paradox.
"""

import random
import matplotlib.pyplot as plt

# --- System Parameters from Theoretical Proof ---
EPSILON = 0.005
P_A = 0.5 - EPSILON  # 0.495
P_B_BAD = 0.1 - EPSILON  # 0.095 (State 0: C mod 3 == 0)
P_B_GOOD = 0.75 - EPSILON  # 0.745 (State 1, 2: C mod 3 != 0)


# --- Game Definitions ---
def play_game_a(capital: int) -> int:
    """Game A: A simple biased coin toss."""
    return capital + 1 if random.random() < P_A else capital - 1


def play_game_b(capital: int) -> int:
    """Game B: A state-dependent Markov chain game."""
    if capital % 3 == 0:
        return capital + 1 if random.random() < P_B_BAD else capital - 1
    else:
        return capital + 1 if random.random() < P_B_GOOD else capital - 1


def play_game_c(capital: int) -> int:
    """Game C: Randomly alternate between Game A and Game B (50% chance each)."""
    if random.random() < 0.5:
        return play_game_a(capital)
    else:
        return play_game_b(capital)


# --- Monte Carlo Simulation Engine ---
def run_monte_carlo(game_func, num_trials: int, num_steps: int) -> list:
    """
    Runs the specified game multiple times to calculate the expected capital trajectory.
    """
    # Initialize an array to store the sum of capital at each step across all trials
    capital_sums = [0.0] * (num_steps + 1)

    for _ in range(num_trials):
        capital = 0
        for step in range(1, num_steps + 1):
            capital = game_func(capital)
            capital_sums[step] += capital

    # Calculate the average capital at each step to find the expected value (E[C])
    return [total / num_trials for total in capital_sums]


def main():
    trials = 5000
    steps = 1000

    print("=== Parrondo's Paradox MCMC Simulator ===")
    print(f"Running {trials} parallel universes, each playing {steps} rounds...")

    print("\nSimulating Game A (Simple biased coin)...")
    trajectory_a = run_monte_carlo(play_game_a, trials, steps)

    print("Simulating Game B (State-dependent Markov chain)...")
    trajectory_b = run_monte_carlo(play_game_b, trials, steps)

    print("Simulating Game C (50/50 Random Mixture)...")
    trajectory_c = run_monte_carlo(play_game_c, trials, steps)

    # --- Terminal Output ---
    print("\n[Final Expected Capital after 1000 rounds]")
    print(f"Game A (Expected to lose): {trajectory_a[-1]:.2f}")
    print(f"Game B (Expected to lose): {trajectory_b[-1]:.2f}")
    print(f"Game C (The Paradox - WIN): {trajectory_c[-1]:.2f}")

    # --- Visualization ---
    print("\nGenerating trajectory plot...")
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_a, label="Game A (Losing)", color="red", alpha=0.8)
    plt.plot(trajectory_b, label="Game B (Losing)", color="blue", alpha=0.8)
    plt.plot(
        trajectory_c,
        label="Game C (Winning - The Paradox)",
        color="green",
        linewidth=2.5,
    )

    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.title(
        "Parrondo's Paradox: Monte Carlo Simulation", fontsize=14, fontweight="bold"
    )
    plt.xlabel("Number of Rounds", fontsize=12)
    plt.ylabel("Expected Capital (E[C])", fontsize=12)
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)

    # Save the plot to the directory
    plt.savefig("parrondo_trajectories.png", dpi=300)
    print(
        "Plot saved as 'parrondo_trajectories.png'."
    )


if __name__ == "__main__":
    main()
