# Conway's Soldiers

This directory contains a reachability analysis and invariant proof for Conway's Soldiers.

---

## 1. Formal Definitions

We consider a single-player state-machine game on an infinite two-dimensional integer grid $\mathbb{Z}^2$.

### 1. State Space and Initial Conditions

- The initial boundary line that cannot be crossed directly is set to be $y = 0.5$.
- **Initial state**: Pegs, or soldiers, may only be placed on grid points in the half-plane $y \le 0$, namely $y = 0, -1, -2, \dots$. Each coordinate point may contain at most one peg. The total number of pegs in the initial configuration must be **finite**. The half-plane $y > 0$ is initially empty.

### 2. Move Rule: Peg Solitaire Rule

- Any form of ``sliding'' or ``translation'' of a peg is strictly forbidden.
- Suppose there are three adjacent and collinear grid points $A, B, C$, only in a horizontal or vertical direction. A **legal jump** is allowed if and only if $A$ and $B$ are occupied by pegs and $C$ is empty: the peg at $A$ jumps over $B$ and lands at $C$.
- After the operation, $C$ becomes occupied, while the pegs at $A$ and $B$ are removed. Each move necessarily decreases the total number of pegs in the system by one.

### 3. Target State

- Through finitely many legal moves, at least one peg must reach the target row $y = 5$, namely the point $(0, 5)$ or an equivalent position.

---

## 2. Physical Constraints and Reachability of Low-Level States

Under the forced constraints of the rules, any forward advance of a peg must sacrifice an adjacent peg as a ``jumping platform.'' This physical constraint causes the state space to expand exponentially when one tries to advance toward higher-level targets.

### Proposition 1: Reaching $y=1$ requires at least 2 initial pegs.

- **Construction**: Place pegs at $(0, 0)$ and $(0, -1)$.
- **Operation**: The peg at $(0, -1)$ jumps over $(0, 0)$ and lands at $(0, 1)$. The loss is 1 peg, and the target is reached.

### Proposition 2: Reaching $y=2$ requires at least 4 initial pegs.

- **Construction and derivation**: A necessary precondition for landing on $y=2$ is that there are surviving pegs on both $y=1$ and $y=0$ in the same column.

  1. First use 2 pegs, as in Proposition 1, to occupy $(0, 1)$. After this consumption, $(0, 0)$ becomes empty.
  2. Because translation is forbidden, another 2 pegs must be used, for example placed at $(-2, 0)$ and $(-1, 0)$, so that a horizontal jump lands at $(0, 0)$ and fills it.
  3. Finally, the peg at $(0, 0)$ jumps over $(0, 1)$ and lands at $(0, 2)$. The total consumption is 4 pegs.

### Corollary

Because lower-level horizontal jumps are repeatedly needed to ``transport'' and ``pave the way,'' overcoming spatial congestion causes very high path consumption. It can be proved mathematically that reaching $y=3$ requires 8 pegs, and reaching $y=4$ requires 20 pegs.

---

## 3. Motivation for the Algebraic Construction of the Monovariant

To prove that $y=5$ is unreachable, we introduce an invariant method. The core idea is to find a **monotonically decreasing quantity**, or **monovariant**: a state-mapping function such that the total ``potential energy'' of the system never increases under any legal operation.

### Derivation of the Weights

Assume that a grid point at distance $d$ from the target has weight $x^d$, where $x \in (0, 1)$ is an unknown decay factor.

According to the move rule, when a peg jumps toward the target, from distance $k$ over distance $k-1$ and lands at distance $k-2$, the system loses potential energies $x^k$ and $x^{k-1}$, and gains potential energy $x^{k-2}$. To ensure that the total potential energy is non-increasing, the following inequality constraint must hold:

$$x^{k-2} \le x^{k-1} + x^k$$

Since $x > 0$, dividing both sides by $x^{k-2}$ gives the core algebraic constraint corresponding to the physical rule of the system:

$$1 \le x + x^2$$

To make the proof boundary maximally tight, and to make an effective forward jump preserve potential energy, we take the critical equality case of this inequality:

$$x^2 + x - 1 = 0$$

Solving this quadratic equation and taking its positive root gives the reciprocal of the golden ratio, denoted by $\varphi$:

$$\varphi = \frac{\sqrt{5} - 1}{2}$$

This algebraic root is not a subjective choice; it is the unique metric factor strictly derived from the jump rule of the game.

---

## 4. Conway's Theorem and Formal Proof

## Theorem: Conway's Theorem

For any finite initial configuration of pegs, there is no finite sequence of legal moves that can make a peg reach the target row $y = 5$.

## Proof

### 1. Definition of the Potential Function

Let the target point be $T = (0, 5)$. Define the Manhattan distance from any grid point $S = (x, y)$ to $T$ by:

$$d(x, y) = |x| + |5 - y|$$

Assign to each point $S$ the weight $w(S) = \varphi^{d(x, y)}$.

At any moment, the total potential energy $V$ of the system is defined as the sum of the weights of all occupied grid points:

$$V = \sum_{S \in \text{Occupied}} \varphi^{d(S)}$$

It is known that $\varphi$ satisfies the algebraic identity $\varphi^2 + \varphi = 1 \implies 1 - \varphi = \varphi^2$.

### 2. Lemma 1: A Legal Move Does Not Increase the Total Potential Energy ($\Delta V \le 0$)

Consider one legal jump, where a peg jumps from $A$ over $B$ and lands on the empty position $C$. The change in potential energy is $\Delta V = w(C) - w(A) - w(B)$. We discuss three cases:

- **Moving toward the target point**: $d(C) = k-2$, $d(B) = k-1$, $d(A) = k$.

  $$\Delta V = \varphi^{k-2} - \varphi^{k-1} - \varphi^k = \varphi^{k-2}(1 - \varphi - \varphi^2) = 0$$

- **Moving away from the target point**: $d(C) = k+2$, $d(B) = k+1$, $d(A) = k$.

  $$\Delta V = \varphi^{k+2} - \varphi^{k+1} - \varphi^k < 0$$

- **Equidistant horizontal move**:

  $$\Delta V = \varphi^k - \varphi^{k-1} - \varphi^k = -\varphi^{k-1} < 0$$

Therefore, after any legal move, $V_{\text{final}} \le V_{\text{initial}}$.

### 3. Lemma 2: The Theoretical Limit of the Fully Loaded Lower Half-Plane ($V_{\max} \le 1$)

We compute the infinite-series limit of the sum of all grid-point weights in the half-plane $y \le 0$.

First, sum along the vertical axis $x=0$, where the distance is $d = 5 - y$:

$$V_{x=0} = \sum_{y=0}^{-\infty} \varphi^{5-y} = \sum_{n=0}^{\infty} \varphi^{5+n} = \frac{\varphi^5}{1 - \varphi} = \frac{\varphi^5}{\varphi^2} = \varphi^3$$

The symmetric sum includes the vertical axis and all columns on both sides. The distance increment for column $x$ is $|x|$:

$$V_{\max} = V_{x=0} + 2 \sum_{x=1}^{\infty} \varphi^x \cdot V_{x=0} = \varphi^3 + 2 \sum_{x=1}^{\infty} \varphi^{x+3}$$

$$V_{\max} = \varphi^3 + 2 \left( \frac{\varphi^4}{1 - \varphi} \right) = \varphi^3 + 2\varphi^2$$

Substitute $\varphi^2 + \varphi = 1$ to reduce the expression:

$$V_{\max} = \varphi(\varphi^2) + \varphi^2 + \varphi^2 = \varphi(1 - \varphi) + 2\varphi^2 = \varphi - \varphi^2 + 2\varphi^2 = \varphi + \varphi^2 = 1$$

Because the physical rules require the initial configuration to contain only a **finite number** of pegs, the actual initial potential energy of the system must be strictly smaller than this fully loaded limit:

$$V_{\text{initial}} < 1$$

### 4. Deriving the Contradiction

If there exists a legal sequence of moves that makes a peg reach the target point $T(0, 5)$, then the final potential-energy sum must contain the weight of the target point itself:

$$w(0, 5) = \varphi^0 = 1$$

It follows that the total final potential energy required for successfully reaching the target satisfies $V_{\text{final}} \ge 1$.

Combining Lemma 1 and Lemma 2, we obtain the system of inequalities:

$$1 \le V_{\text{final}} \le V_{\text{initial}} < 1$$

Clearly, this implies the absolute mathematical contradiction $1 < 1$.

Therefore, no matter what finite initial configuration of pegs and jump strategy are used, reaching $y = 5$ is impossible.

$$\blacksquare$$
