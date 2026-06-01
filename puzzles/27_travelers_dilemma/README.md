# The Traveler's Dilemma

## 1. System Setting and Game Environment

Two travelers, agent A and agent B, bought identical antiques. During a flight, both antiques were lost by the airline. The airline manager needs to compensate them, but does not know the true value of the antiques.

The manager places A and B in two separate rooms and asks each of them to independently write down an integer in the following range:

$$
\lbrace 2,3,4,\ldots,100 \rbrace
$$

The integer represents the claimed value of the antique.

---

## 2. Mechanism and Payoff Rules

Let A's number be $a$, and let B's number be $b$.

If the two numbers are equal, namely:

$$
a=b=X
$$

then both travelers receive compensation equal to $X$.

If the two numbers are different, let the smaller number be $S$ and the larger number be $L$. The manager assumes that the smaller number $S$ is the true value.

The payoff rule is:

$$
\text{the traveler who wrote the smaller number receives } S+2
$$

$$
\text{the traveler who wrote the larger number receives } S-2
$$

Thus, the lower claimant receives a reward, while the higher claimant receives a penalty.

---

## 3. Theorem

Under the assumptions of perfect rationality and common knowledge of rationality, the unique Nash equilibrium of the game is:

$$
(2,2)
$$

In other words, both travelers eventually choose the number $2$.

---

## 4. Proof

This proof uses iterated elimination of weakly dominated strategies to derive the final choice of two perfectly rational travelers.

Strictly speaking, the dominance relation here is weak dominance. Writing $99$ instead of $100$ gives the same payoff against some opponent strategies, so it is not a strict dominance relation in every case.

---

### 4.1 Pareto-Optimal Outcome

If both travelers write $100$, then by the equal-claim rule, both travelers receive full compensation of $100$.

Therefore:

$$
(100,100)
$$

is the globally Pareto-optimal outcome.

However, a Pareto-optimal outcome is not necessarily a Nash equilibrium. We still need to examine whether either agent has an incentive to deviate unilaterally.

---

### 4.2 Unilateral Payoff Maximization

Suppose A believes that B will write $100$.

If A also writes $100$, then A receives:

$$
100
$$

If A instead writes $99$, then A has written the smaller number and receives:

$$
99+2=101
$$

Since:

$$
101>100
$$

A has an incentive to write $99$ whenever A expects B to write $100$.

By symmetry, B can make exactly the same reasoning.

---

### 4.3 Common Knowledge and Strategy Elimination

In game theory, rationality is common knowledge. That is:

$$
\text{A knows that B is rational, B knows that A is rational, and both know that the other knows this}
$$

Since A can see that writing $99$ is better than writing $100$ when the opponent writes $100$, rational B can also infer the same logic.

Therefore, both players realize that writing $100$ can be exploited by the opponent writing $99$.

Thus, the strategy $100$ is eliminated, and the strategy space becomes:

$$
\lbrace 2,3,4,\ldots,99 \rbrace
$$

---

### 4.4 Iterated Strategy Elimination

Once the largest available number becomes $99$, the same reasoning repeats.

If both players expect the other to write $99$, then each receives:

$$
99
$$

However, if A writes $98$ instead, then A writes the smaller number and receives the reward:

$$
98+2=100
$$

Since:

$$
100>99
$$

A does not want to remain at $99$.

Similarly, B knows that A does not want to remain at $99$. Therefore, $99$ is also eliminated, and the strategy space shrinks to:

$$
\lbrace 2,3,4,\ldots,98 \rbrace
$$

This logic continues:

$$
100 \to 99 \to 98 \to 97 \to \cdots \to 2
$$

That is, in order to defend against the opponent choosing the current highest number, a rational agent always has an incentive to choose one less than the current highest number and obtain the reward.

---

### 4.5 Convergence to Nash Equilibrium

This iterated elimination process stops only when the strategy space reaches the lower bound imposed by the rules.

The lower bound is:

$$
2
$$

When both players write $2$, their payoff is:

$$
(2,2)
$$

At this point, neither player can choose a smaller number.

If one player unilaterally increases the number, for example from $2$ to $3$, while the other player still writes $2$, then the deviating player becomes the higher claimant and receives:

$$
2-2=0
$$

Since:

$$
0<2
$$

neither player has an incentive to increase the number unilaterally when the other player writes $2$.

Therefore:

$$
(2,2)
$$

is a Nash equilibrium.

---

## 5. Uniqueness of the Equilibrium

If both players write the same number $k$, where $k>2$, then either player can deviate to $k-1$ and receive:

$$
(k-1)+2=k+1
$$

Since:

$$
k+1>k
$$

no outcome of the form:

$$
(k,k),\quad k>2
$$

can be a Nash equilibrium.

If the two players write different numbers, then the player who wrote the larger number can switch to the smaller number and improve from the penalty payoff to the equal-claim payoff. Therefore, unequal strategy profiles are not Nash equilibria either.

Hence, the unique Nash equilibrium of the game is:

$$
(2,2)
$$

---

## 6. Conclusion

The Traveler's Dilemma demonstrates the conflict between Pareto optimality and Nash equilibrium.

Although:

$$
(100,100)
$$

gives both travelers the highest cooperative payoff, the reasoning chain generated by perfect rationality and common knowledge drives both players to reduce their numbers step by step.

In the end, the system cannot sustain the cooperative payoff of $100$ and instead converges to the unique Nash equilibrium:

$$
(2,2)
$$

$$
\blacksquare
$$
