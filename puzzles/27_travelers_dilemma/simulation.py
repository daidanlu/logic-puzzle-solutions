"""
Traveler's Dilemma Simulation

1. The payoff mechanism of the Traveler's Dilemma.
2. The Pareto-optimal cooperative outcome (100, 100).
3. The iterated elimination path from 100 down to 2.
4. The unique Nash equilibrium (2, 2).

The default game uses integer claims from 2 to 100 and a reward/penalty value of 2.
"""

from typing import List, Tuple, Dict

Strategy = int
Payoff = Tuple[int, int]
Profile = Tuple[int, int]


def payoff(a: Strategy, b: Strategy, bonus: int = 2) -> Payoff:
    """
    Compute the payoff for player A and player B.

    If both players choose the same number X, both receive X.
    If the choices differ, the lower claimant receives S + bonus,
    and the higher claimant receives S - bonus.
    """
    if a == b:
        return a, b

    smaller = min(a, b)

    if a < b:
        return smaller + bonus, smaller - bonus
    else:
        return smaller - bonus, smaller + bonus


def best_responses_to_opponent(
    opponent_choice: Strategy,
    strategies: List[Strategy],
    player: str,
    bonus: int = 2,
) -> List[Strategy]:
    """
    Return all best responses to a fixed opponent choice.

    player = "A" means we compute A's best responses to B's choice.
    player = "B" means we compute B's best responses to A's choice.
    """
    values: Dict[Strategy, int] = {}

    for s in strategies:
        if player == "A":
            values[s] = payoff(s, opponent_choice, bonus)[0]
        elif player == "B":
            values[s] = payoff(opponent_choice, s, bonus)[1]
        else:
            raise ValueError("player must be either 'A' or 'B'")

    max_value = max(values.values())
    return [s for s, value in values.items() if value == max_value]


def find_nash_equilibria(
    low: int = 2,
    high: int = 100,
    bonus: int = 2,
) -> List[Profile]:
    """
    Find all pure-strategy Nash equilibria by brute force.

    A profile (a, b) is a Nash equilibrium if:
    - a is a best response to b;
    - b is a best response to a.
    """
    strategies = list(range(low, high + 1))
    equilibria: List[Profile] = []

    for a in strategies:
        for b in strategies:
            a_best = best_responses_to_opponent(b, strategies, "A", bonus)
            b_best = best_responses_to_opponent(a, strategies, "B", bonus)

            if a in a_best and b in b_best:
                equilibria.append((a, b))

    return equilibria


def weakly_dominates_against_restricted_space(
    dominating: Strategy,
    dominated: Strategy,
    opponent_strategies: List[Strategy],
    bonus: int = 2,
) -> bool:
    """
    Check whether one strategy weakly dominates another strategy
    for player A against a restricted opponent strategy space.

    Because the game is symmetric, checking player A is enough
    for the same dominance relation to hold for player B.
    """
    payoff_dominating = []
    payoff_dominated = []

    for opponent in opponent_strategies:
        payoff_dominating.append(payoff(dominating, opponent, bonus)[0])
        payoff_dominated.append(payoff(dominated, opponent, bonus)[0])

    at_least_as_good = all(x >= y for x, y in zip(payoff_dominating, payoff_dominated))
    strictly_better_somewhere = any(
        x > y for x, y in zip(payoff_dominating, payoff_dominated)
    )

    return at_least_as_good and strictly_better_somewhere


def iterated_elimination_trace(
    low: int = 2,
    high: int = 100,
    bonus: int = 2,
) -> List[Tuple[int, int, bool]]:
    """
    Simulate the iterated elimination logic.

    At each step, when the current maximum remaining strategy is U,
    strategy U - 1 weakly dominates strategy U over the restricted
    strategy space {low, ..., U}.

    The returned rows are:
    (eliminated_strategy, dominating_strategy, dominance_verified)
    """
    trace: List[Tuple[int, int, bool]] = []

    current_high = high
    while current_high > low:
        dominated = current_high
        dominating = current_high - 1
        restricted_space = list(range(low, current_high + 1))

        verified = weakly_dominates_against_restricted_space(
            dominating=dominating,
            dominated=dominated,
            opponent_strategies=restricted_space,
            bonus=bonus,
        )

        trace.append((dominated, dominating, verified))
        current_high -= 1

    return trace


def pareto_optimal_profiles(
    low: int = 2,
    high: int = 100,
    bonus: int = 2,
) -> List[Tuple[Profile, Payoff]]:
    """
    Find Pareto-optimal pure profiles by brute force.

    A profile is Pareto-optimal if no other profile makes one player
    strictly better off without making the other player worse off.
    """
    strategies = list(range(low, high + 1))
    profiles = [((a, b), payoff(a, b, bonus)) for a in strategies for b in strategies]

    pareto_profiles: List[Tuple[Profile, Payoff]] = []

    for profile, p in profiles:
        dominated_by_another = False

        for other_profile, q in profiles:
            if q[0] >= p[0] and q[1] >= p[1] and (q[0] > p[0] or q[1] > p[1]):
                dominated_by_another = True
                break

        if not dominated_by_another:
            pareto_profiles.append((profile, p))

    return pareto_profiles


def print_sample_payoffs() -> None:
    """Print a few payoff examples."""
    examples = [(100, 100), (99, 100), (98, 99), (2, 2), (3, 2)]

    print("Sample payoff checks")
    print("-" * 60)

    for a, b in examples:
        print(f"A chooses {a:>3}, B chooses {b:>3} -> payoff = {payoff(a, b)}")

    print()


def print_elimination_summary(trace: List[Tuple[int, int, bool]]) -> None:
    """Print a readable summary of the elimination process."""
    print("Iterated elimination of weakly dominated strategies")
    print("-" * 60)

    print("First 10 elimination steps:")
    for eliminated, dominating, verified in trace[:10]:
        print(
            f"Eliminate {eliminated:>3}: "
            f"{dominating:>3} weakly dominates {eliminated:>3} "
            f"-> verified = {verified}"
        )

    print("...")

    print("Last 5 elimination steps:")
    for eliminated, dominating, verified in trace[-5:]:
        print(
            f"Eliminate {eliminated:>3}: "
            f"{dominating:>3} weakly dominates {eliminated:>3} "
            f"-> verified = {verified}"
        )

    all_verified = all(row[2] for row in trace)
    print()
    print(f"All elimination steps verified: {all_verified}")
    print(f"Final remaining strategy: {trace[-1][1]}")
    print()


def main() -> None:
    low = 2
    high = 100
    bonus = 2

    print("=" * 60)
    print("Traveler's Dilemma Simulation")
    print("=" * 60)
    print(f"Strategy space: {{{low}, {low + 1}, ..., {high}}}")
    print(f"Reward/penalty value: {bonus}")
    print()

    print_sample_payoffs()

    pareto_profiles = pareto_optimal_profiles(low, high, bonus)
    print("Pareto-optimal profile check")
    print("-" * 60)
    print(f"Number of Pareto-optimal pure profiles found: {len(pareto_profiles)}")
    print("Top Pareto-optimal profiles by total payoff:")
    for profile, p in sorted(
        pareto_profiles, key=lambda item: sum(item[1]), reverse=True
    )[:5]:
        print(f"profile = {profile}, payoff = {p}, total payoff = {sum(p)}")
    print()

    trace = iterated_elimination_trace(low, high, bonus)
    print_elimination_summary(trace)

    equilibria = find_nash_equilibria(low, high, bonus)
    print("Pure-strategy Nash equilibrium check")
    print("-" * 60)
    print(f"Nash equilibria found: {equilibria}")
    print()

    if equilibria == [(2, 2)]:
        print("Conclusion: the equilibrium claim is verified.")
        print("The unique pure-strategy Nash equilibrium is (2, 2).")
    else:
        print("Conclusion: the equilibrium result differs from the claim.")
        print("Please inspect the payoff rule and parameter settings.")


if __name__ == "__main__":
    main()
