# Penney's Game: Non-Transitivity and Second-Mover Advantage

## Overview

When building a strategy-pairing pool for a multi-agent evolutionary game sandbox, such as Evolutio, it is natural to assume that strategic advantage is transitive:

$$A \succ B,\quad B \succ C \implies A \succ C$$

Penney's Game gives a compact counterexample. Even when the underlying random process is perfectly fair, temporal pattern matching can create non-transitive strategic dominance.

---

## 1. System Model

We use a fair coin. Each toss gives heads `H` or tails `T` with probability:

$$P(H)=P(T)=\frac{1}{2}$$

There are two players:

- Alice moves first.
- Bob moves second.

The rules are:

1. Alice publicly chooses a sequence of length 3, such as `HTT`.
2. Bob observes Alice's choice and publicly chooses a different sequence of length 3, such as `THT`.
3. The system repeatedly tosses the coin and generates a random stream.
4. The player whose sequence appears first as a consecutive block wins, and the system stops.

At first glance, every length-3 sequence has the same long-run frequency. This may suggest that the first player and the second player should have approximately equal chances of winning. That intuition is wrong.

The key point is not whether one sequence is absolutely more likely to appear. The key point is which sequence can intercept the other sequence first in the random stream.

---

## 2. Conway's Counterstrategy

The mathematician John Horton Conway gave a simple counterstrategy for the second player.

Suppose Alice chooses:

$$A=A_1A_2A_3$$

Bob constructs:

$$B=B_1B_2B_3$$

according to the rule:

$$B_1=\neg A_2,\quad B_2=A_1,\quad B_3=A_2$$

In words, Bob copies Alice's first two symbols as his last two symbols, and places the opposite of Alice's second symbol in front.

For example, if Alice chooses:

$$A=\text{HHT}$$

then Bob chooses:

$$B=\text{THH}$$

---

## 3. Example: Why `THH` Beats `HHT`

Consider:

$$A=\text{HHT},\quad B=\text{THH}$$

We claim that Bob's winning probability is:

$$P(B)=\frac{3}{4}=75\%$$

---

## 4. State-Space Argument

Partition the infinite coin stream by its first few tosses.

### Branch 1: The first toss is `T`

This branch has probability:

$$\frac{1}{2}$$

The current suffix is `T`. For Alice to form `HHT`, the stream must eventually form two consecutive `H` symbols after this suffix. But once `HH` appears after the suffix `T`, the stream has already formed:

$$\text{THH}$$

Therefore, Bob triggers his winning condition before Alice does. Bob wins in this branch.

### Branch 2: The first two tosses are `HT`

This branch has probability:

$$\frac{1}{4}$$

The current suffix is again `T`, so the same reasoning as in Branch 1 applies. Bob wins in this branch.

### Branch 3: The first three tosses are `HHT`

This branch has probability:

$$\frac{1}{8}$$

Alice's target sequence appears immediately, so the game stops. Bob loses in this branch.

### Branch 4: The first three tosses are `HHH`

This branch has probability:

$$\frac{1}{8}$$

The stream currently ends with consecutive `HH`. For Bob to form `THH`, he must first wait for a new `T` to start his pattern. But once a `T` appears after the current `HH`, the stream immediately forms:

$$\text{HHT}$$

Therefore, Alice triggers her winning condition first. Bob loses in this branch.

Combining the four cases:

$$P(B)=\frac{1}{2}\cdot 1+\frac{1}{4}\cdot 1+\frac{1}{8}\cdot 0+\frac{1}{8}\cdot 0=\frac{3}{4}$$

Thus:

$$P(B)=75\%$$

---

## 5. Conway's Leading Number Algorithm

The same result can be computed algebraically using a prefix-overlap method.

### Definition

For two sequences $X$ and $Y$ of length $n$, define $X \cdot Y$ as follows:

- For each $k=1,2,\dots,n$;
- compare the last $k$ symbols of $X$ with the first $k$ symbols of $Y$;
- if they are identical, record $2^{k-1}$;
- sum all recorded values.

This value measures how strongly the suffixes of $X$ cover the prefixes of $Y$.

---

## 6. Computing the Overlaps

Let:

$$A=\text{HHT},\quad B=\text{THH}$$

### 6.1 Self-overlap of Alice

For $A \cdot A$:

- $k=3$: `HHT` equals `HHT`, record $4$.
- $k=2$: `HT` does not equal `HH`, record $0$.
- $k=1$: `T` does not equal `H`, record $0$.

Therefore:

$$A \cdot A=4$$

### 6.2 Self-overlap of Bob

For $B \cdot B$:

- $k=3$: `THH` equals `THH`, record $4$.
- $k=2$: `HH` does not equal `TH`, record $0$.
- $k=1$: `H` does not equal `T`, record $0$.

Therefore:

$$B \cdot B=4$$

### 6.3 Alice-to-Bob overlap

For $A \cdot B$:

- $k=3$: `HHT` does not equal `THH`, record $0$.
- $k=2$: `HT` does not equal `TH`, record $0$.
- $k=1$: `T` equals `T`, record $1$.

Therefore:

$$A \cdot B=1$$

### 6.4 Bob-to-Alice overlap

For $B \cdot A$:

- $k=3$: `THH` does not equal `HHT`, record $0$.
- $k=2$: `HH` equals `HH`, record $2$.
- $k=1$: `H` equals `H`, record $1$.

Therefore:

$$B \cdot A=3$$

---

## 7. Odds Formula

Conway's odds formula is:

$$\frac{P(B)}{P(A)}=\frac{A \cdot A-A \cdot B}{B \cdot B-B \cdot A}$$

Substituting the values above:

$$\frac{P(B)}{P(A)}=\frac{4-1}{4-3}=3$$

Hence:

$$P(B):P(A)=3:1$$

After normalization:

$$P(B)=\frac{3}{3+1}=\frac{3}{4}=75\%$$

This agrees with the state-space argument.

---

## 8. General Counterstrategy Table

Conway's rule works for every length-3 sequence Alice can choose. Bob's optimal countersequences are:

| Alice's sequence | Bob's countersequence | Bob's winning probability |
|---|---:|---:|
| `HHH` | `THH` | $7/8=87.5\%$ |
| `HHT` | `THH` | $3/4=75\%$ |
| `HTH` | `HHT` | $2/3\approx 66.7\%$ |
| `HTT` | `HHT` | $2/3\approx 66.7\%$ |
| `THH` | `TTH` | $2/3\approx 66.7\%$ |
| `THT` | `TTH` | $2/3\approx 66.7\%$ |
| `TTH` | `HTT` | $3/4=75\%$ |
| `TTT` | `HTT` | $7/8=87.5\%$ |

Therefore, no matter what Alice chooses, Bob can choose a countersequence that gives him winning probability at least:

$$\frac{2}{3}\approx 66.7\%$$

and at most:

$$\frac{7}{8}=87.5\%$$

---

## 9. Non-Transitive Cycle

In the strategy pool:

$$\lbrace \text{HTT},\text{HHT},\text{THH},\text{TTH} \rbrace$$

we obtain the following dominance cycle:

$$\text{HTT}<\text{HHT}<\text{THH}<\text{TTH}<\text{HTT}$$

Here, $X<Y$ means that sequence $Y$ beats sequence $X$ in a pairwise match.

Equivalently:

$$\text{HHT beats HTT}$$

$$\text{THH beats HHT}$$

$$\text{TTH beats THH}$$

$$\text{HTT beats TTH}$$

Thus, there is no globally strongest strategy in this pool. The dominance relation is cyclic rather than linear.

---

## 10. Conclusion

Penney's Game shows that in a multi-agent game system, even perfectly fair and independent random primitives can generate non-transitive macroscopic strategic relationships.

The reason is not that one length-3 sequence has a higher absolute probability of appearing. The reason is that different sequences have different prefix-suffix overlap structures.

The central phenomenon can be summarized as:

$$\text{fair randomness}+\text{temporal pattern matching}\implies \text{non-transitive advantage}$$

Therefore, when designing an evolutionary game sandbox or a strategy-pairing pool, one should not simply assume:

$$A \succ B,\quad B \succ C \implies A \succ C$$

Penney's Game provides a compact counterexample: local fairness does not imply global transitivity.

$$\text{Q.E.D.}$$
