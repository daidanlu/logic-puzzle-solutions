from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Literal, Optional, Tuple

Move = Literal[-1, 1]
State = int
Symbol = Literal[0, 1]
NextState = Optional[int]
Transition = Tuple[Symbol, Move, NextState]


@dataclass(frozen=True)
class RunResult:
    halted: bool
    steps: int
    ones: int
    min_pos: int
    max_pos: int
    tape_snapshot: str


@dataclass(frozen=True)
class BinaryTuringMachine:
    state_count: int
    transitions: Dict[Tuple[State, Symbol], Transition]
    start_state: State = 0

    def run(self, max_steps: int = 10_000) -> RunResult:
        tape: Dict[int, Symbol] = {}
        head = 0
        state: NextState = self.start_state
        min_seen = max_seen = 0

        for step in range(1, max_steps + 1):
            if state is None:
                return self._result(True, step - 1, tape, min_seen, max_seen)

            read = tape.get(head, 0)
            write, move, next_state = self.transitions[(state, read)]

            if write == 0:
                tape.pop(head, None)
            else:
                tape[head] = 1

            head += move
            min_seen = min(min_seen, head)
            max_seen = max(max_seen, head)
            state = next_state

            if state is None:
                return self._result(True, step, tape, min_seen, max_seen)

        return self._result(False, max_steps, tape, min_seen, max_seen)

    @staticmethod
    def _result(
        halted: bool,
        steps: int,
        tape: Dict[int, Symbol],
        min_seen: int,
        max_seen: int,
    ) -> RunResult:
        left = min(min_seen, min(tape.keys(), default=0))
        right = max(max_seen, max(tape.keys(), default=0))
        snapshot = "".join(str(tape.get(i, 0)) for i in range(left, right + 1))
        return RunResult(
            halted=halted,
            steps=steps,
            ones=sum(tape.values()),
            min_pos=left,
            max_pos=right,
            tape_snapshot=snapshot,
        )


def busy_beaver_2_state_machine() -> BinaryTuringMachine:
    return BinaryTuringMachine(
        state_count=2,
        transitions={
            (0, 0): (1, 1, 1),     # A0 -> 1 R B
            (0, 1): (1, -1, 1),    # A1 -> 1 L B
            (1, 0): (1, -1, 0),    # B0 -> 1 L A
            (1, 1): (1, 1, None),  # B1 -> 1 R HALT
        },
    )


def enumerate_binary_machines(state_count: int) -> Iterable[BinaryTuringMachine]:
    keys = [(state, symbol) for state in range(state_count) for symbol in (0, 1)]
    choices: list[Transition] = [
        (write, move, next_state)
        for write in (0, 1)
        for move in (-1, 1)
        for next_state in [*range(state_count), None]
    ]

    for table in product(choices, repeat=len(keys)):
        yield BinaryTuringMachine(
            state_count=state_count,
            transitions=dict(zip(keys, table)),
        )


def finite_search(state_count: int, max_steps: int) -> tuple[int, int, int, int]:
    best_ones = 0
    best_steps = 0
    halted_count = 0
    undecided_count = 0

    for machine in enumerate_binary_machines(state_count):
        result = machine.run(max_steps=max_steps)
        if result.halted:
            halted_count += 1
            best_ones = max(best_ones, result.ones)
            best_steps = max(best_steps, result.steps)
        else:
            undecided_count += 1

    return best_ones, best_steps, halted_count, undecided_count


def main() -> None:
    known = busy_beaver_2_state_machine()
    result = known.run(max_steps=100)

    print("Known 2-state busy beaver candidate")
    print(f"halted: {result.halted}")
    print(f"steps:  {result.steps}")
    print(f"ones:   {result.ones}")
    print(f"tape:   {result.tape_snapshot}")
    print()

    print("Finite exhaustive search with cutoff")
    for n, cutoff in [(1, 20), (2, 100)]:
        best_ones, best_steps, halted_count, undecided_count = finite_search(n, cutoff)
        print(f"N={n}, cutoff={cutoff}")
        print(f"  best ones among halted machines: {best_ones}")
        print(f"  best steps among halted machines: {best_steps}")
        print(f"  halted within cutoff: {halted_count}")
        print(f"  not halted within cutoff: {undecided_count}")
        print()

    print("Important: not halted within cutoff is not the same as proven non-halting.")


if __name__ == "__main__":
    main()
