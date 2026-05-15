from typing import List, Tuple, Dict


Cell = Tuple[int, int]
Board = List[List[int]]


def color_of(cell: Cell) -> int:
    """
    Return the chessboard color of a cell.

    0 means black.
    1 means white.
    """
    row, col = cell
    return (row + col) % 2


def count_colors(size: int, removed: List[Cell]) -> Tuple[int, int]:
    """
    Count black and white squares on a size x size board
    after removing the given cells.
    """
    removed_set = set(removed)
    black = 0
    white = 0

    for row in range(size):
        for col in range(size):
            if (row, col) in removed_set:
                continue

            if color_of((row, col)) == 0:
                black += 1
            else:
                white += 1

    return black, white


def verify_mutilated_chessboard() -> None:
    """
    Verify the coloring invariant for the mutilated 8x8 chessboard.

    Removing two opposite corners removes two squares of the same color.
    Therefore the remaining board has unequal black and white counts,
    so it cannot be tiled by dominoes.
    """
    size = 8
    removed = [(0, 0), (7, 7)]

    black, white = count_colors(size, removed)

    print("Mutilated 8x8 chessboard:")
    print(f"Removed squares: {removed}")
    print(f"Black squares: {black}")
    print(f"White squares: {white}")

    assert black != white
    assert black == 30
    assert white == 32

    print("Domino tiling is impossible by the coloring invariant.")
    print()


def create_board(size: int, missing: Cell) -> Board:
    """
    Create a size x size board.

    -1 marks the missing square.
     0 marks an uncovered square.
    Positive integers will mark tromino IDs.
    """
    board = [[0 for _ in range(size)] for _ in range(size)]
    row, col = missing
    board[row][col] = -1
    return board


class TrominoTiler:
    def __init__(self, size: int, missing: Cell):
        if size < 2 or size & (size - 1) != 0:
            raise ValueError("size must be a power of 2 and at least 2")

        self.size = size
        self.board = create_board(size, missing)
        self.next_id = 1

    def tile(self) -> Board:
        self._tile_region(0, 0, self.size, self._find_missing(0, 0, self.size))
        return self.board

    def _find_missing(self, top: int, left: int, size: int) -> Cell:
        """
        Find the unique already-filled or missing square in a region.

        In the recursive proof, each sub-board has exactly one special square:
        either the original missing square or a square occupied by the central tromino.
        """
        found = []

        for row in range(top, top + size):
            for col in range(left, left + size):
                if self.board[row][col] != 0:
                    found.append((row, col))

        if len(found) != 1:
            raise ValueError(
                f"Region top={top}, left={left}, size={size} "
                f"has {len(found)} special squares, expected 1."
            )

        return found[0]

    def _tile_region(self, top: int, left: int, size: int, missing: Cell) -> None:
        """
        Recursively tile a defective size x size region.

        The region has top-left corner (top, left) and exactly one missing
        or already occupied square.
        """
        if size == 2:
            tile_id = self.next_id
            self.next_id += 1

            for row in range(top, top + 2):
                for col in range(left, left + 2):
                    if self.board[row][col] == 0:
                        self.board[row][col] = tile_id
            return

        half = size // 2
        mid_row = top + half
        mid_col = left + half

        missing_row, missing_col = missing

        # Determine which quadrant contains the missing square.
        if missing_row < mid_row and missing_col < mid_col:
            missing_quadrant = 0  # upper-left
        elif missing_row < mid_row and missing_col >= mid_col:
            missing_quadrant = 1  # upper-right
        elif missing_row >= mid_row and missing_col < mid_col:
            missing_quadrant = 2  # lower-left
        else:
            missing_quadrant = 3  # lower-right

        # The four central corner squares, one from each quadrant.
        central_cells = [
            (mid_row - 1, mid_col - 1),  # upper-left quadrant
            (mid_row - 1, mid_col),      # upper-right quadrant
            (mid_row, mid_col - 1),      # lower-left quadrant
            (mid_row, mid_col),          # lower-right quadrant
        ]

        # Place one central L-tromino covering the central cells
        # of the three quadrants that do not contain the original missing square.
        tile_id = self.next_id
        self.next_id += 1

        for quadrant, cell in enumerate(central_cells):
            if quadrant != missing_quadrant:
                row, col = cell
                self.board[row][col] = tile_id

        # Recursively tile the four quadrants.
        quadrants = [
            (top, left),
            (top, mid_col),
            (mid_row, left),
            (mid_row, mid_col),
        ]

        for q_top, q_left in quadrants:
            q_missing = self._find_missing(q_top, q_left, half)
            self._tile_region(q_top, q_left, half, q_missing)


def cells_with_id(board: Board) -> Dict[int, List[Cell]]:
    result: Dict[int, List[Cell]] = {}

    for row in range(len(board)):
        for col in range(len(board)):
            value = board[row][col]
            if value > 0:
                result.setdefault(value, []).append((row, col))

    return result


def is_l_tromino(cells: List[Cell]) -> bool:
    """
    Check whether three cells form an L-shaped tromino.

    They must be exactly three cells of some 2x2 block.
    """
    if len(cells) != 3:
        return False

    rows = [r for r, _ in cells]
    cols = [c for _, c in cells]

    if max(rows) - min(rows) != 1:
        return False

    if max(cols) - min(cols) != 1:
        return False

    return True


def verify_tromino_tiling(size: int, missing: Cell) -> None:
    """
    Construct and verify an L-tromino tiling for a defective board.
    """
    tiler = TrominoTiler(size, missing)
    board = tiler.tile()

    # Check the missing square remains missing.
    assert board[missing[0]][missing[1]] == -1

    # Check no square except the missing one is uncovered.
    for row in range(size):
        for col in range(size):
            if (row, col) == missing:
                continue
            assert board[row][col] > 0

    # Check every positive tile ID forms exactly one L-tromino.
    groups = cells_with_id(board)

    for tile_id, cells in groups.items():
        assert is_l_tromino(cells), (
            f"Tile {tile_id} is not a valid L-tromino: {cells}"
        )

    expected_trominoes = (size * size - 1) // 3

    assert len(groups) == expected_trominoes

    print(f"Defective {size}x{size} board:")
    print(f"Missing square: {missing}")
    print(f"L-trominoes used: {len(groups)}")
    print("Recursive L-tromino tiling verified successfully.")
    print()


def print_board(board: Board) -> None:
    """
    Print the board in a compact format.

    XX marks the missing square.
    Numbers mark tromino IDs.
    """
    for row in board:
        print(
            " ".join(
                "XX" if value == -1 else f"{value:02d}"
                for value in row
            )
        )


def demo_tromino_board(size: int, missing: Cell) -> None:
    tiler = TrominoTiler(size, missing)
    board = tiler.tile()
    print_board(board)


if __name__ == "__main__":
    verify_mutilated_chessboard()

    verify_tromino_tiling(2, (0, 0))
    verify_tromino_tiling(4, (1, 2))
    verify_tromino_tiling(8, (3, 5))
    verify_tromino_tiling(16, (10, 7))

    print("Example 8x8 tiling:")
    demo_tromino_board(8, (3, 5))