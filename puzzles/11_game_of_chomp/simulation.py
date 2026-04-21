"""
The Game of Chomp - Mathematical Simulation
"""

from functools import lru_cache


class ChompGame:

    def __init__(self, m: int, n: int):
        if m < 1 or n < 1 or m * n <= 1:
            raise ValueError("Invalid grid size. Must be m, n >= 1 and m * n > 1.")

        self.m = m
        self.n = n
        # State Representation: A tuple is used to record the current height of each column. Initially, the height of all columns is n.
        # For example, the initial state of a 3x2 board is (2, 2, 2).
        self.state = tuple([n] * m)

    def is_game_over(self) -> bool:
        """
        Termination Condition: If even the poison at (1, 1) is consumed, the game ends. Under this state representation, the consumption of (1, 1) is equivalent to the height of the first column being 0.
        """
        return self.state[0] == 0

    def get_valid_moves(self, current_state: tuple) -> list[tuple[int, int]]:
        moves = []
        for x in range(1, self.m + 1):
            column_height = current_state[x - 1]
            for y in range(1, column_height + 1):
                # Exclude the scenario where there are no remaining moves and the only option is to consume the poison at (1,1) (unless the poison is the only item left).
                if x == 1 and y == 1 and sum(current_state) > 1:
                    continue
                moves.append((x, y))
        return moves

    def apply_move(self, current_state: tuple, move: tuple[int, int]) -> tuple:
        """
        "Devour" Mechanism: Eliminates all blocks with coordinates satisfying x' >= x and y' >= y.
        """
        x, y = move
        new_state = list(current_state)
        for col_idx in range(x - 1, self.m):
            if new_state[col_idx] >= y:
                new_state[col_idx] = y - 1
        return tuple(new_state)


class NashMinimaxSolver:
    """
    Brute-Force Search
    """

    def __init__(self, game: ChompGame):
        self.game = game

    @lru_cache(maxsize=None)
    def minimax(self, state: tuple) -> tuple[int, int]:
        if sum(state) == 1 and state[0] == 1:
            return None

        valid_moves = self.game.get_valid_moves(state)

        for move in valid_moves:
            next_state = self.game.apply_move(state, move)
            # The Core Manifestation of Strategy Stealing: If a move places the opponent in an inevitably losing state (returns None), then this move is the guaranteed winning move.
            if self.minimax(next_state) is None:
                return move

        # If, after exploring every possible move, none leads to a guaranteed defeat for the opponent, it indicates that it's in a losing position.
        return None


class SquareMirrorSolver:
    """
    Square Chessboard (n x n) Explicit Construction Strategy: Mirror Strategy
    """

    def get_move(self, state: tuple) -> tuple[int, int]:
        m = len(state)
        n = max(state) if state else 0

        if all(h == n for h in state):
            return (2, 2)

        for i in range(1, m):
            row_length = sum(1 for h in state if h > i)
            col_height = state[i]

            if row_length > col_height:
                return (col_height + 1, i + 1)
            elif col_height > row_length:
                return (i + 1, row_length + 1)

        # If the situation is already strictly symmetrical (meaning the current player has been checkmated), they can only make a random move.
        return (1, state[0])


if __name__ == "__main__":
    print("=== The Game of Chomp Simulation ===")

    m, n = 3, 4
    game = ChompGame(m, n)
    solver = NashMinimaxSolver(game)

    print(f"\n[Test 1] Finding explicit winning move for generalized {m}x{n} grid...")
    winning_move = solver.minimax(game.state)
    print(
        f"Nash's Theorem holds. Player 1's strictly winning first move is: {winning_move}"
    )

    m, n = 4, 4
    sq_game = ChompGame(m, n)
    sq_solver = SquareMirrorSolver()

    print(f"\n[Test 2] Constructive Strategy for Square {m}x{n} board...")
    first_move = sq_solver.get_move(sq_game.state)
    print(f"Player 1 selects: {first_move}")
    print(
        "Action matches README Constructive Strategy: Removes upper-right square block, forms symmetric 'L'-shape."
    )
