Original problem reference: https://en.wikipedia.org/wiki/100_prisoners_problem

This directory contains a mathematical proof and Python simulation for the 100 prisoners problem.

## Problem

There are 100 prisoners labeled 1 to 100.  
There are 100 boxes, each containing a unique label from 1 to 100 placed randomly, one per box.  

Each prisoner may enter the room individually and open at most 50 boxes. After each prisoner leaves, the boxes are reset to their original state. No communication is allowed between prisoners.  

If all prisoners find their own number, they are all released; otherwise, they are all executed.

What is the optimal strategy? How can it be proven?

---

## Optimal Strategy: Cycle-Following Strategy

For any prisoner $i$:

- Open box $i$. If it contains $i$, success.
- If it contains $j$ ($j \ne i$), then open box $j$.
- Repeat this process for up to 50 steps.

Surprisingly, this optimal strategy gives about $31.183\%$ probability that all prisoners are released.

---

## Proof

We now explain why this strategy is so effective.

If one is familiar with combinatorics or abstract algebra, the cycle notation of permutations provides a concise way to describe the structure used in this proof.

Let $f(x)$ denote the number inside box $x$.  
Since each number from $1$ to $100$ appears exactly once, $f$ is a bijection from the set  
$$
X = \{1, \dots, 100\}
$$  
to itself. That is, $f$ is a permutation on $X$.

---

The strategy can be abstracted as: for prisoner $i$,
$$
i, \ f(i), \ f(f(i)), \ \dots
$$

Prisoner $i$ succeeds if and only if the cycle containing $i$ has length $\le 50$.

For any $i \in X$, all prisoners succeed if and only if all cycles of the permutation $f$ have length $\le 50$.

---

$$
P(\text{all cycles have length } \le 50)
=
1 - P(\text{there exists a cycle of length } > 50)
$$

These two events are mutually exclusive, because it is impossible for two cycles to both have length greater than $50$ (their total size would exceed $100$).

Thus, we only need to compute the probability that at least one prisoner fails, and subtract it from 1 (since the failure of one implies failure of all).

---

For a cycle of length $k > 50$, there are
$$
\binom{100}{k}
$$
ways to choose the $k$ elements.

If we do not consider equivalence, there would be $k!$ arrangements. However, since cycles are invariant under rotation, we divide by $k$, giving
$$
(k - 1)!
$$
distinct cycles.

The remaining $(100 - k)$ elements can be arranged arbitrarily into cycles of length $\le 50$, giving
$$
(100 - k)!
$$
possibilities.

Therefore, the total number of permutations containing such a cycle is
$$
\binom{100}{k} \cdot (k - 1)! \cdot (100 - k)!
$$

Dividing by the total number of permutations
$$
100!
$$

we obtain
$$
\frac{1}{k}
$$

---

$$
P(\text{failure}) = \sum_{k=51}^{100} \frac{1}{k}
$$

$$
P(\text{success}) = 1 - \sum_{k=51}^{100} \frac{1}{k} = 0.31183
$$

---

Q.E.D.