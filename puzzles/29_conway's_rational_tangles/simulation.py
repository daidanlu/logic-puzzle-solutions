"""
Simulation for Conway's Rational Tangles.

Model used:
    T(x) = x + 1
    R(x) = -1/x
with special values:
    R(0) = infinity
    R(infinity) = 0
    T(infinity) = infinity

The script randomly generates operation sequences from the initial value 0,
then computes an untangling sequence using only T and R.
"""

from __future__ import annotations

import argparse
import random
from fractions import Fraction
from typing import Optional, Iterable

# None represents infinity.
Value = Optional[Fraction]
INF: Value = None


def fmt(x: Value) -> str:
    if x is INF:
        return "∞"
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def twist(x: Value) -> Value:
    """Apply T(x) = x + 1, with T(∞) = ∞."""
    if x is INF:
        return INF
    return x + 1


def rotate(x: Value) -> Value:
    """Apply R(x) = -1/x, with R(0)=∞ and R(∞)=0."""
    if x is INF:
        return Fraction(0)
    if x == 0:
        return INF
    return -Fraction(1, 1) / x


def apply_op(x: Value, op: str) -> Value:
    """Apply one operation, T or R."""
    if op == "T":
        return twist(x)
    if op == "R":
        return rotate(x)
    raise ValueError(f"Unknown operation {op!r}; expected 'T' or 'R'.")


def apply_ops(ops: Iterable[str], start: Value = Fraction(0)) -> Value:
    """Apply a sequence of operations from a starting value."""
    x = start
    for op in ops:
        x = apply_op(x, op)
    return x


def ceil_fraction(x: Fraction) -> int:
    """Return ceil(x) for a nonnegative Fraction."""
    if x < 0:
        raise ValueError("ceil_fraction expects a nonnegative Fraction.")
    return (x.numerator + x.denominator - 1) // x.denominator


def untangle(start: Value, max_steps: int = 100_000) -> tuple[list[str], list[Value]]:
    """
    Return operations that transform start back to 0 using only T and R.

    This implements the algorithm:
      - if x = ∞, apply R;
      - if x < 0, apply T until x >= 0;
      - if x > 0, apply R, then apply T until x >= 0;
      - repeat until x = 0.
    """
    x = start
    ops: list[str] = []
    values: list[Value] = [x]

    while x != 0:
        if len(ops) > max_steps:
            raise RuntimeError(
                "Untangling exceeded max_steps; check the model or input."
            )

        if x is INF:
            x = rotate(x)
            ops.append("R")
            values.append(x)
            continue

        if x < 0:
            n = ceil_fraction(-x)
            for _ in range(n):
                x = twist(x)
                ops.append("T")
                values.append(x)
            continue

        # Now x is a positive rational number.
        x = rotate(x)
        ops.append("R")
        values.append(x)

        # After rotation, x is negative, so add 1 until it becomes nonnegative.
        if x is not INF and x < 0:
            n = ceil_fraction(-x)
            for _ in range(n):
                x = twist(x)
                ops.append("T")
                values.append(x)

    return ops, values


def compress_ops(ops: Iterable[str]) -> str:
    """Compress runs such as TTTTRTT into T^4 R T^2."""
    ops = list(ops)
    if not ops:
        return "(none)"
    chunks: list[str] = []
    current = ops[0]
    count = 1
    for op in ops[1:]:
        if op == current:
            count += 1
        else:
            chunks.append(current if count == 1 else f"{current}^{count}")
            current = op
            count = 1
    chunks.append(current if count == 1 else f"{current}^{count}")
    return " ".join(chunks)


def random_ops(length: int, rng: random.Random) -> list[str]:
    """Generate a random sequence of T/R operations."""
    return [rng.choice(["T", "R"]) for _ in range(length)]


def run_one(ops: list[str], trace: bool = False) -> bool:
    """Simulate one generated tangle and print its untangling result."""
    x = apply_ops(ops)
    undo_ops, values = untangle(x)
    final = apply_ops(undo_ops, start=x)
    ok = final == 0

    print(f"Generated ops:   {compress_ops(ops)}")
    print(f"Current value:   {fmt(x)}")
    print(f"Untangle ops:    {compress_ops(undo_ops)}")
    print(f"Final value:     {fmt(final)}")
    print(f"Verified:        {ok}")

    if trace:
        print("Trace:")
        print(f"  start {fmt(x)}")
        for op, value in zip(undo_ops, values[1:]):
            print(f"  {op:>2} -> {fmt(value)}")

    return ok


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate Conway rational tangles and untangle them using only T and R."
    )
    parser.add_argument(
        "--sequence",
        type=str,
        help="A specific operation sequence, e.g. TRTT. If omitted, random trials are used.",
    )
    parser.add_argument(
        "--trials", type=int, default=10, help="Number of random trials."
    )
    parser.add_argument(
        "--max-ops", type=int, default=12, help="Maximum generated sequence length."
    )
    parser.add_argument("--seed", type=int, default=1, help="Random seed.")
    parser.add_argument(
        "--trace", action="store_true", help="Print every untangling step."
    )
    args = parser.parse_args()

    if args.sequence:
        ops = [c.upper() for c in args.sequence if not c.isspace()]
        invalid = sorted(set(ops) - {"T", "R"})
        if invalid:
            raise ValueError(
                f"Invalid symbols in sequence: {invalid}. Use only T and R."
            )
        ok = run_one(ops, trace=args.trace)
        raise SystemExit(0 if ok else 1)

    rng = random.Random(args.seed)
    passed = 0

    for i in range(1, args.trials + 1):
        length = rng.randint(0, args.max_ops)
        ops = random_ops(length, rng)
        print(f"\nTrial {i}")
        print("-" * 40)
        if run_one(ops, trace=args.trace):
            passed += 1

    print(f"\nSummary: {passed}/{args.trials} trials returned to 0.")


if __name__ == "__main__":
    main()
