"""
Multi-Agent Simulation for the El Farol Bar Problem (Minority Game).
"""

import random


class Agent:
    def __init__(self, memory_length: int, num_strategies: int):
        self.memory_length = memory_length
        self.strategies = []

        # Initialize strategy pool: A strategy is a lookup table mapping a history of past weeks represented as a tuple of booleans
        # True = predict overcrowded (>M)
        # False = predict comfortable (<=M)
        num_possible_histories = (
            1 << memory_length
        )  # num_possible_histories = 2^memory_length
        for _ in range(num_strategies):
            strategy = {}
            for i in range(num_possible_histories):
                # Convert integer to a tuple of booleans representing past states, e.g. 6 is reversed 110 (False, True, True)
                history_tuple = tuple(bool((i >> j) & 1) for j in range(memory_length))
                strategy[history_tuple] = random.choice([True, False])
            self.strategies.append(strategy)

        # Track the performance of each strategy
        self.strategy_scores = [0] * num_strategies

    def predict_and_decide(self, current_history: tuple) -> bool:
        """
        Agent picks their highest-scoring strategy to predict tonight's crowd.
        Returns True if they decide to go, False if they stay home.
        """
        best_score = max(self.strategy_scores)
        # Handle ties randomly to prevent herd behavior
        best_indices = [
            i for i, score in enumerate(self.strategy_scores) if score == best_score
        ]
        active_strategy_idx = random.choice(best_indices)

        # Predict the outcome using the best strategy
        predicted_overcrowded = self.strategies[active_strategy_idx][current_history]

        # Decision logic: Go if predicting comfortable, stay if predicting overcrowded
        return not predicted_overcrowded

    def update_strategy_scores(self, current_history: tuple, actual_overcrowded: bool):
        """
        Reward strategies that correctly predicted the actual outcome.
        """
        for i, strategy in enumerate(self.strategies):
            prediction = strategy[current_history]
            if prediction == actual_overcrowded:
                self.strategy_scores[i] += 1
            else:
                self.strategy_scores[i] -= 1


def run_minority_game(
    total_agents=100, threshold=60, weeks=500, memory_length=3, strategies_per_agent=5
):
    print("=== El Farol Bar Problem Simulation (Minority Game) ===")
    print(f"N = {total_agents}, M = {threshold}")
    print(
        f"Memory Length = {memory_length} weeks, Strategies per Agent = {strategies_per_agent}\n"
    )

    # Initialize agents
    agents = [Agent(memory_length, strategies_per_agent) for _ in range(total_agents)]

    # Generate an initial random history
    history = [random.choice([True, False]) for _ in range(memory_length)]
    attendance_record = []

    for week in range(1, weeks + 1):
        # The history tuple agents look at to make their current decision
        current_history_tuple = tuple(history[-memory_length:])

        # 1. All agents independently decide whether to go
        attendance = sum(
            agent.predict_and_decide(current_history_tuple) for agent in agents
        )
        attendance_record.append(attendance)

        # 2. System determines the actual macroscopic outcome
        actual_overcrowded = attendance > threshold
        history.append(actual_overcrowded)

        # 3. Agents reflect and update their strategy scores
        for agent in agents:
            agent.update_strategy_scores(current_history_tuple, actual_overcrowded)

    print(f"Simulation completed for {weeks} weeks.")
    recent_attendance = attendance_record[-100:]
    avg_attendance = sum(recent_attendance) / len(recent_attendance)

    print(f"\n[Results]")
    print(f"Average attendance over the last 100 weeks: {avg_attendance:.2f}")
    print(f"Expected theoretical mean (Nash Equilibrium): {threshold}")

    # Print the last 10 weeks
    print(f"Attendance in the final 10 weeks: {attendance_record[-10:]}")

    if abs(avg_attendance - threshold) <= 5:
        print(
            "\nConclusion: The system successfully self-organized into a dynamic equilibrium near the threshold, proving the power of inductive reasoning!"
        )


if __name__ == "__main__":
    run_minority_game()
