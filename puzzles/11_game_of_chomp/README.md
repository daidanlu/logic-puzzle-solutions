# The Game of Chomp

This directory contains the mathematical proof and Python simulation verification for The Game of Chomp.

**I. Definition of the Game**

A two-player alternating game is played on a discrete $m \times n$ grid, where $m, n \ge 1$ and $m \cdot n > 1$.

* **State Space**: Each coordinate point $(x, y)$ on the grid represents one square of chocolate.
* **Terminal Condition**: The square at coordinate $(1, 1)$ is the “poison” square. The player who selects this square immediately loses.
* **Move Rule**: On each turn, a player may select any square $(x, y)$ that has not yet been removed, and simultaneously remove all squares satisfying $x' \ge x$ and $y' \ge y$.

---

**II. Theorem (Nash's Chomp Theorem)**

For every $m \times n$ game of Chomp satisfying $m \cdot n > 1$, the first player (Player 1) must have a winning strategy.

**III. Proof**

This proof uses contradiction together with the strategy-stealing argument.

1.  **Characterization of the Game**:
    This game is a finite, perfect-information, deterministic, two-player zero-sum game with no possibility of a draw. By Zermelo's Theorem, in any such game, exactly one of the two players must have a winning strategy.

2.  **Assumption for Contradiction**:
    Assume that the first player does not have a winning strategy. Then by Zermelo's Theorem, the second player (Player 2) must have a winning strategy. That is, no matter what the first player does, the second player has a corresponding winning response.

3.  **Strategy-Stealing**:
    * Suppose the first player makes a probing move on the first turn by removing only the upper-right corner square $(m, n)$.
    * By the assumption in Step 2, the second player has a winning response to this position. Let that move be the selection of square $(x, y)$.
    * By the move rule, selecting $(x, y)$ removes all squares above and to the right of it. Since $(m, n)$ is the upper-rightmost square of the entire grid, it must necessarily lie inside the region removed by $(x, y)$.
    * Therefore, the resulting position after the sequence “Player 1 selects $(m, n)$ $\rightarrow$ Player 2 selects $(x, y)$” is **exactly equivalent** to the position obtained if “Player 1 directly selects $(x, y)$” on the first move.

4.  **Deriving the Contradiction**:
    * If selecting $(x, y)$ is a winning move that allows the second player to force victory, then the first player could simply select $(x, y)$ immediately on the first turn and thereby take over that same winning position.
    * This implies that “the first player has a winning strategy,” which directly contradicts the assumption in Step 2 that “the second player has a winning strategy.”

5.  **Conclusion**:
    The assumption is false. Once the possibility that the second player has a winning strategy is ruled out, it necessarily follows that the first player has a winning strategy.

$$\blacksquare$$

---

**IV. Remark: Non-Constructiveness and Explicit Strategies in Special Cases**

The argument above is a non-constructive existence proof. It does not provide the exact first move for the first player on a general $m \times n$ board. However, in certain lower-dimensional special cases, there are explicit constructive winning strategies:

* **Square Board ($n \times n$): Mirroring Strategy**
    * **First Move**: The first player selects $(2, 2)$, removing the upper-right square block and turning the board into a symmetric “L”-shape.
    * **Continuation**: No matter what move the second player makes on one branch, the first player makes the strictly symmetric corresponding move on the other branch, maintaining the symmetry invariant of the position and forcing the second player eventually to select $(1, 1)$.
* **Two-Row Board ($2 \times n$): Offset Suppression**
    * **First Move**: The first player selects $(n, 2)$ (the rightmost single square in the first row).
    * **Continuation**: By calculation, the first player ensures that after each move the board satisfies a fixed state invariant: the number of remaining squares in the bottom layer (the first row) is always exactly $1$ greater than the number of remaining squares in the top layer (the second row). Repeating this invariant causes the position to converge, and the second player is ultimately left with the losing position in which only $(1, 1)$ remains.
