# 100 Prisoners Problem

Original problem reference: <https://en.wikipedia.org/wiki/100_prisoners_problem>

This directory contains the mathematical proof and Python simulation of the 100 prisoners problem.

## Problem

There are 100 prisoners, numbered 1–100.  
There are 100 boxes, each containing a randomly placed label from 1–100, one label per box.  
Each prisoner may enter the room individually and open at most 50 boxes. After that, the boxes are restored to their original state, and no communication is allowed with subsequent prisoners.  
If all prisoners find their own number, they are all released; if even one fails, all are executed.

What is the optimal strategy? How can it be proven?

## Optimal Strategy: cycle-following strategy

For any prisoner i:

- Open box i; if it contains i, succeed.
- If opening box i reveals number j (j ≠ i), then open box j.
- Repeat this process for up to 50 steps.

The result is that this optimal strategy has a surprising probability of 31.183% that all prisoners are released.

## Proof

We now prove why this optimal strategy is so effective.

If one is familiar with some combinatorics or abstract algebra, one knows cycle notation (permutation cycle representation). This proof will use this concise representation.

Let f(x) denote the number inside the box labeled x.  
Since each number from 1–100 appears exactly once, f is a bijection from the set

```math
X = \{1, \dots, 100\}
```

to itself, i.e., f : X → X. In other words, f is a permutation on X.

The process of this strategy can be abstracted as: for prisoner i,

```math
i, f(i), f(f(i)), \dots
```

Prisoner i succeeds if and only if the cycle containing i has length ≤ 50.

For any i ∈ X, all prisoners succeed if and only if all cycles of the permutation f have length ≤ 50.

Therefore,

```math
P(\text{all cycle lengths} \le 50)
=
1 - P(\text{there exists a cycle with length} > 50)
```

These two events are mutually exclusive, because it is impossible for two cycles to both have length greater than 50, otherwise the total number of elements would exceed 100.

Therefore, we only need to compute the probability that some prisoner fails, and subtract it from 1 to obtain the result (the failure of one prisoner implies the failure of all).

For a cycle of length k > 50, there are

```math
\binom{100}{k}
```

ways to choose the k elements.

If equivalence is not considered, there would be k! permutations. However, since cycles are equivalent under rotation, we divide by k, giving

```math
(k - 1)!
```

distinct cycles.

The remaining (100 - k) elements can be arranged arbitrarily into one or more cycles of length ≤ 50, giving

```math
(100 - k)!
```

ways.

Therefore, the total number of permutations containing a cycle of length k is

```math
\binom{100}{k} \cdot (k - 1)! \cdot (100 - k)!
```

Dividing by the total number of permutations

```math
100!
```

we obtain the probability

```math
\frac{1}{k}
```

Thus,

```math
P(\text{failure}) = \sum_{k=51}^{100} \frac{1}{k}
```

So,

```math
P(\text{success}) = 1 - \sum_{k=51}^{100} \frac{1}{k} \approx 0.31183
```

Q.E.D.
