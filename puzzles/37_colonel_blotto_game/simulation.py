from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from itertools import product
from statistics import mean
from typing import Iterable, Sequence


Allocation = tuple[int, ...]


@dataclass(frozen=True)
class PureEquilibrium:
    player_a: Allocation
    player_b: Allocation
    payoff_to_a: int


@dataclass(frozen=True)
class CounterAllocation:
    allocation: Allocation
    counter: Allocation
    payoff_to_a: int


@dataclass(frozen=True)
class SampleSummary:
    name: str
    battlefield_mean: float
    total_mean: float
    total_min: float
    total_max: float
    q25: float
    q50: float
    q75: float
    overflow_rate: float


def sign(value: float) -> int:
    return (value > 0) - (value < 0)


def payoff(player_a: Sequence[float], player_b: Sequence[float]) -> int:
    return sum(sign(a_i - b_i) for a_i, b_i in zip(player_a, player_b))


def integer_allocations(total: int, battlefields: int) -> list[Allocation]:
    return [
        allocation
        for allocation in product(range(total + 1), repeat=battlefields)
        if sum(allocation) == total
    ]


def allocation_types(strategies: Iterable[Allocation]) -> list[Allocation]:
    return sorted({tuple(sorted(strategy, reverse=True)) for strategy in strategies}, reverse=True)


def pure_nash_equilibria(strategies: Sequence[Allocation]) -> list[PureEquilibrium]:
    equilibria: list[PureEquilibrium] = []

    for player_a in strategies:
        for player_b in strategies:
            current = payoff(player_a, player_b)
            best_a = max(payoff(candidate, player_b) for candidate in strategies)
            best_b = min(payoff(player_a, candidate) for candidate in strategies)

            if current == best_a and current == best_b:
                equilibria.append(PureEquilibrium(player_a, player_b, current))

    return equilibria


def best_counter(allocation: Allocation, strategies: Sequence[Allocation]) -> CounterAllocation:
    counter = min(strategies, key=lambda candidate: payoff(allocation, candidate))
    return CounterAllocation(allocation, counter, payoff(allocation, counter))


def independent_uniform_samples(total: float, battlefields: int, trials: int) -> list[list[float]]:
    upper = 2 * total / battlefields
    return [
        [random.uniform(0.0, upper) for _ in range(battlefields)]
        for _ in range(trials)
    ]


def simplex_samples(total: float, battlefields: int, trials: int) -> list[list[float]]:
    samples: list[list[float]] = []

    for _ in range(trials):
        weights = [random.expovariate(1.0) for _ in range(battlefields)]
        weight_sum = sum(weights)
        samples.append([total * weight / weight_sum for weight in weights])

    return samples


def quantile(values: Sequence[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[int(q * (len(ordered) - 1))]


def summarize_samples(
    name: str,
    samples: Sequence[Sequence[float]],
    total: float,
    battlefields: int,
) -> SampleSummary:
    upper = 2 * total / battlefields
    first_battlefield = [sample[0] for sample in samples]
    totals = [sum(sample) for sample in samples]

    return SampleSummary(
        name=name,
        battlefield_mean=mean(first_battlefield),
        total_mean=mean(totals),
        total_min=min(totals),
        total_max=max(totals),
        q25=quantile(first_battlefield, 0.25),
        q50=quantile(first_battlefield, 0.50),
        q75=quantile(first_battlefield, 0.75),
        overflow_rate=mean(value > upper for value in first_battlefield),
    )


def print_discrete_report(total: int, battlefields: int) -> None:
    strategies = integer_allocations(total, battlefields)
    equilibria = pure_nash_equilibria(strategies)

    print(f"Discrete Colonel Blotto: S={total}, N={battlefields}")
    print(f"Pure strategies: {len(strategies)}")
    print(f"Pure Nash equilibria: {len(equilibria)}")

    if equilibria:
        for equilibrium in equilibria:
            print(
                f"A={equilibrium.player_a}, "
                f"B={equilibrium.player_b}, "
                f"payoff={equilibrium.payoff_to_a}"
            )
        return

    print("\nCounter-allocations by sorted type:")
    print(f"{'A allocation':>16} | {'B counter':>16} | {'payoff to A':>11}")
    print("-" * 53)

    for allocation in allocation_types(strategies):
        result = best_counter(allocation, strategies)
        print(f"{str(result.allocation):>16} | {str(result.counter):>16} | {result.payoff_to_a:>11}")


def print_sample_summary(summary: SampleSummary) -> None:
    print(f"\n{summary.name}")
    print("-" * len(summary.name))
    print(f"battlefield mean: {summary.battlefield_mean:.4f}")
    print(f"total mean:       {summary.total_mean:.4f}")
    print(f"total min/max:    {summary.total_min:.4f} / {summary.total_max:.4f}")
    print(f"battlefield q25:  {summary.q25:.4f}")
    print(f"battlefield q50:  {summary.q50:.4f}")
    print(f"battlefield q75:  {summary.q75:.4f}")
    print(f"P(x_i > 2S/N):    {summary.overflow_rate:.4f}")


def print_continuous_report(total: float, battlefields: int, trials: int) -> None:
    print(f"\nContinuous sampling check: S={total:g}, N={battlefields}, trials={trials}")

    uniform_summary = summarize_samples(
        "Independent Uniform(0, 2S/N)",
        independent_uniform_samples(total, battlefields, trials),
        total,
        battlefields,
    )

    simplex_summary = summarize_samples(
        "Normalized simplex sampling",
        simplex_samples(total, battlefields, trials),
        total,
        battlefields,
    )

    print_sample_summary(uniform_summary)
    print_sample_summary(simplex_summary)

    print("\nKey check:")
    print("- independent uniforms match the marginal target but do not keep total resources fixed;")
    print("- simplex samples keep total resources fixed but do not match the uniform marginal.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Colonel Blotto discrete and continuous simulation.")
    parser.add_argument("--soldiers", type=int, default=6)
    parser.add_argument("--battlefields", type=int, default=3)
    parser.add_argument("--trials", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    random.seed(args.seed)

    print_discrete_report(args.soldiers, args.battlefields)
    print_continuous_report(float(args.soldiers), args.battlefields, args.trials)


if __name__ == "__main__":
    main()
