# Polyomino Tiling Invariants

This document gives mathematical proofs for two classical polyomino tiling problems. The first proof uses a coloring invariant to show that the mutilated chessboard cannot be tiled by dominoes. The second proof uses a recursive construction to show that every defective $2^n \times 2^n$ board can be tiled by L-shaped trominoes.

---

## 1. Basic Model

A board region is a finite collection of unit squares.

A domino covers two edge-adjacent unit squares. An L-shaped tromino covers three unit squares inside a $2 \times 2$ block.

A region is tileable by a given collection of tiles if the region can be covered completely by those tiles, with no overlaps and no uncovered squares.

---

## 2. Domino Tilings and the Mutilated Chessboard

Consider the standard $8 \times 8$ chessboard with its usual black-white coloring. Remove two opposite corner squares to obtain a mutilated chessboard.

The question is:

$$
\text{Can this mutilated board be tiled by }31\text{ dominoes?}
$$

The answer is no.

---

## 3. The Coloring Invariant

Under the standard chessboard coloring, any two edge-adjacent squares have different colors.

Therefore, every domino covers exactly one black square and one white square:

$$
\text{one domino}=1\text{ black square}+1\text{ white square}
$$

Hence, if a region can be tiled by dominoes, then the number of black squares in the region must equal the number of white squares:

$$
\#\text{black squares}=\#\text{white squares}
$$

This is the coloring invariant preserved by domino tilings.

---

## 4. Impossibility Proof for the Mutilated Chessboard

The original $8 \times 8$ chessboard has $64$ squares. Under the standard coloring, the numbers of black and white squares are equal:

$$
\#\text{black}=32
$$

$$
\#\text{white}=32
$$

The two opposite corner squares have the same color. Without loss of generality, assume that the two removed corners are black. Then the remaining board has:

$$
\#\text{black}=30
$$

$$
\#\text{white}=32
$$

If this mutilated board could be tiled by $31$ dominoes, then since each domino covers one black square and one white square, the $31$ dominoes would cover:

$$
31\text{ black squares}+31\text{ white squares}
$$

Thus the tiled region would have to satisfy:

$$
\#\text{black}=\#\text{white}=31
$$

But the actual mutilated board satisfies:

$$
\#\text{black}=30<32=\#\text{white}
$$

This contradicts the coloring invariant for domino tilings.

Therefore, the $8 \times 8$ board with two opposite corners removed cannot be tiled by $31$ dominoes.

$$
\blacksquare
$$

---

## 5. The General Coloring-Invariant Method

The previous proof illustrates a more general method.

Assign colors or weights to the unit squares of a board. If every allowed tile has a fixed color-count or weight contribution, then every tileable region must satisfy the corresponding global invariant condition.

The logic can be summarized as:

$$
\text{fixed local tile contribution}\Rightarrow\text{global invariant condition}
$$

For dominoes, the local contribution is:

$$
1\text{ black square}+1\text{ white square}
$$

So the whole region must satisfy:

$$
\#\text{black squares}=\#\text{white squares}
$$

If a target region violates this condition, then no domino tiling can exist.

Thus, a coloring invariant gives an impossibility proof. It does not fail by searching through tilings. Instead, it proves that every possible tiling would preserve a quantity that the target region does not have.

---

## 6. L-Trominoes and Defective Boards

Now consider another classical tiling problem.

Given a $2^n \times 2^n$ board with one arbitrary square removed, ask whether the remaining board can be tiled by L-shaped trominoes.

We will prove that the answer is yes.

---

## 7. The Area Condition

A $2^n \times 2^n$ board has:

$$
2^n\cdot 2^n=4^n
$$

unit squares. After one square is removed, the number of remaining squares is:

$$
4^n-1
$$

Since:

$$
4\equiv 1\pmod 3
$$

we have:

$$
4^n\equiv 1\pmod 3
$$

Therefore:

$$
4^n-1\equiv 0\pmod 3
$$

The remaining area is divisible by $3$. This shows that an L-tromino tiling is possible from the perspective of area.

However, the area condition is only necessary. The next section gives a constructive proof.

---

## 8. Theorem

For every integer $n\ge 1$, every $2^n \times 2^n$ board with one square removed can be tiled by L-shaped trominoes.

---

## 9. Inductive Proof

We prove the theorem by induction on $n$.

### 9.1 Base Case

When $n=1$, the board has size:

$$
2^1\times 2^1=2\times 2
$$

A $2\times 2$ board with one square removed has exactly three squares remaining. These three squares form one L-shaped tromino.

Therefore, the theorem holds for $n=1$.

### 9.2 Inductive Hypothesis

Assume that the theorem holds for $n-1$. That is, every defective board of size:

$$
2^{n-1}\times 2^{n-1}
$$

can be tiled by L-shaped trominoes.

### 9.3 Inductive Step

Consider a defective board of size:

$$
2^n\times 2^n
$$

Divide the board along its horizontal and vertical midlines into four equal quadrants. Each quadrant has size:

$$
2^{n-1}\times 2^{n-1}
$$

The originally missing square lies in exactly one of the four quadrants. Call this quadrant the special quadrant.

Near the center of the whole board, each quadrant has one central corner square. For each of the three non-special quadrants, choose its central corner square. These three chosen squares form the position of one L-shaped tromino.

Place one L-shaped tromino on those three central squares.

After this placement, each of the four quadrants is a defective $2^{n-1}\times 2^{n-1}$ board:

- the special quadrant already had the original missing square;
- each of the other three quadrants has one central corner square occupied by the central L-shaped tromino;
- hence each quadrant can be viewed as a smaller board with exactly one square missing.

By the inductive hypothesis, each of these four smaller defective boards can be tiled by L-shaped trominoes.

Together with the central L-shaped tromino, these four tilings cover the entire defective $2^n\times 2^n$ board.

Therefore, the theorem holds for $n$.

By mathematical induction, for every integer $n\ge 1$, every defective $2^n\times 2^n$ board can be tiled by L-shaped trominoes.

$$
\blacksquare
$$

---

## 10. Conclusion

These two tiling problems illustrate two complementary mathematical methods.

The mutilated chessboard problem uses a coloring invariant to prove impossibility:

$$
\text{domino tiling}\Rightarrow\#\text{black}=\#\text{white}
$$

The mutilated board violates this condition, so no tiling exists.

The defective chessboard problem uses recursion to prove existence:

$$
\text{large defective board}\Rightarrow\text{four smaller defective boards}
$$

After placing one central L-shaped tromino, the problem reduces recursively to four smaller problems of the same form.

Thus, the central idea of this project is:

$$
\text{invariant for impossibility}+\text{recursion for construction}
$$

In other words:

$$
\text{prove impossibility with invariants, and prove possibility with recursive construction.}
$$
