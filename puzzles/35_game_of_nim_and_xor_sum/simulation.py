from functools import reduce, lru_cache
from itertools import product
from operator import xor
from random import randint, seed


def nim_sum(heaps: list[int]) -> int:
    return reduce(xor, heaps, 0)


def is_winning_state(heaps: list[int]) -> bool:
    return nim_sum(heaps) != 0


def winning_move(heaps: list[int]) -> tuple[int, int, int] | None:
    s = nim_sum(heaps)

    if s == 0:
        return None

    for i, h in enumerate(heaps):
        target = h ^ s
        if target < h:
            return i, target, h - target

    return None


def apply_move(heaps: list[int], index: int, new_value: int) -> list[int]:
    if index < 0 or index >= len(heaps):
        raise ValueError("invalid heap index")

    if new_value < 0 or new_value >= heaps[index]:
        raise ValueError("invalid move")

    next_heaps = heaps[:]
    next_heaps[index] = new_value
    return next_heaps


def fallback_move(heaps: list[int]) -> tuple[int, int, int]:
    for i, h in enumerate(heaps):
        if h > 0:
            return i, h - 1, 1

    raise ValueError("no legal move")


def choose_move(heaps: list[int]) -> tuple[int, int, int]:
    move = winning_move(heaps)
    return move if move is not None else fallback_move(heaps)


def simulate_game(heaps: list[int]) -> str:
    if any(h < 0 for h in heaps):
        raise ValueError("heap sizes must be non-negative")

    current = heaps[:]
    player = 1

    print("=" * 72)
    print(f"Initial heaps: {current}")
    print(f"Initial nim-sum: {nim_sum(current)}")
    print(f"Initial state: {'winning' if is_winning_state(current) else 'losing'}")
    print("=" * 72)

    while any(current):
        index, new_value, removed = choose_move(current)
        old_value = current[index]
        next_state = apply_move(current, index, new_value)

        print(
            f"Player {player}: heap {index + 1}, "
            f"{old_value} -> {new_value}, removed {removed}; "
            f"nim-sum {nim_sum(current)} -> {nim_sum(next_state)}"
        )

        current = next_state
        player = 2 if player == 1 else 1

    winner = 2 if player == 1 else 1
    print("=" * 72)
    print(f"Winner: Player {winner}")
    return f"Player {winner}"


@lru_cache(maxsize=None)
def minimax_state(state: tuple[int, ...]) -> bool:
    if all(h == 0 for h in state):
        return False

    for i, h in enumerate(state):
        for new_value in range(h):
            next_state = list(state)
            next_state[i] = new_value

            if not minimax_state(tuple(next_state)):
                return True

    return False


def verify_against_minimax(max_heap: int = 7, pile_count: int = 4) -> None:
    checked = 0

    for state in product(range(max_heap + 1), repeat=pile_count):
        theorem_result = nim_sum(list(state)) != 0
        minimax_result = minimax_state(state)

        if theorem_result != minimax_result:
            raise AssertionError(
                f"Mismatch at {state}: "
                f"nim_sum={theorem_result}, minimax={minimax_result}"
            )

        checked += 1

    print(f"Minimax verification passed: {checked} states.")


def verify_winning_moves(
    samples: int = 10_000, pile_count: int = 6, max_heap: int = 10_000
) -> None:
    seed(0)

    for _ in range(samples):
        heaps = [randint(0, max_heap) for _ in range(pile_count)]

        if nim_sum(heaps) == 0:
            continue

        move = winning_move(heaps)

        if move is None:
            raise AssertionError(f"No winning move found for {heaps}")

        index, new_value, _ = move
        next_heaps = apply_move(heaps, index, new_value)

        if nim_sum(next_heaps) != 0:
            raise AssertionError(f"Invalid winning move: {heaps} -> {next_heaps}")

    print(f"Random winning-move verification passed: {samples} samples.")


if __name__ == "__main__":
    simulate_game([3, 4, 5])

    print()
    verify_against_minimax(max_heap=7, pile_count=4)

    print()
    verify_winning_moves(samples=10_000, pile_count=6, max_heap=10_000)
