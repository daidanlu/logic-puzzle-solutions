# The El Farol Bar Problem (Minority Game)

This directory contains the mathematical deduction of the famous Minority Game in complex systems and algorithmic game theory, along with a multi-agent Python simulator based on inductive reasoning.

## Problem Setup

There are $N$ perfectly rational and extremely intelligent people in a town (classic setting: N = 100).
Every weekend, everyone must independently decide whether to go to the town's only El Farol Bar, with absolutely no communication allowed between them.

The bar's experience depends on the crowd level that night. We set a comfort threshold $M$ (classic setting: M = 60):
- If the total number of people going to the bar is <= M, the atmosphere is excellent. Those who go get a payoff of 1, and those who stay home get a payoff of 0.
- If the total number of people going to the bar is > M, the bar is extremely crowded. Those who go get a payoff of -1, and those who stay home get a payoff of 0.

Objective: In this system, what strategy should perfectly rational individuals adopt, and what is the final equilibrium state of the system?

## The Collapse of Deductive Reasoning

In this model, pure logical deduction leads to a self-referential paradox, making perfect deductive reasoning via common knowledge impossible.

Assume there is a perfect logical reasoning model that can predict the number of people going to the bar tonight, $K$:
1. If the model predicts $K \le 60$: Since everyone is perfectly rational and possesses the same information, everyone will reach the same conclusion. Thus, all 100 people will go to the bar tonight. The actual number becomes 100, the model's prediction fails, everyone who goes loses, and the payoff is -1.
2. If the model predicts $K > 60$: Everyone will conclude that the bar will be crowded, so all 100 people will choose not to go. The actual number becomes 0, the model's prediction fails again, and those who stay home get a payoff of 0.

Conclusion: There is no symmetric pure strategy Nash equilibrium in this system. Any deterministic logical prediction will invalidate itself once adopted by the public.

## Mathematical Proof: Mixed Strategy Nash Equilibrium

Since a deterministic pure strategy does not exist, we use game theory to find a mixed strategy equilibrium in a probabilistic sense.

Assume the system reaches a symmetric Nash equilibrium where everyone chooses to go to the bar with the exact same probability $p$.
For any individual A in the system, the choices of the remaining $N-1$ people constitute a Bernoulli experiment.
The number of other people going to the bar, $X$, follows a binomial distribution:
$$X \sim B(N-1, p)$$

For individual A to reach Nash equilibrium, their expected payoff of choosing to go must equal the expected payoff of choosing not to go.
The expected payoff of not going to the bar is constantly 0.
The expected payoff equation for going to the bar is:
$$E[U_{go}] = 1 \cdot P(X \le M-1) + (-1) \cdot P(X \ge M) = 0$$

From this, we deduce:
$$P(X \le M-1) = P(X \ge M) = 0.5$$

This means that among the remaining $N-1$ people, the median number of people going to the bar (the median perfectly splits a probability distribution in half: the probability of being below the critical point is 50%, and the probability of being above it is also 50%, which is exactly this value $M$) must equal the comfort threshold critical point.
For a binomial distribution $B(n, p)$, its median is approximately equal to its mean $np$.
Therefore, we get:
$$(N-1)p \approx M$$

When $N$ is sufficiently large, the equilibrium probability $p$ converges to:
$$p = \frac{M}{N}$$

## Conclusion & Takeaways

Therefore, under the setting of N = 100 and M = 60, the only symmetric equilibrium is: everyone stays at home and flips a coin, deciding to go to the bar with a 60% probability.

The conclusion is: in a competitive system with limited resources, the optimal decision that a group of perfectly rational people can make is, surprisingly, equivalent to randomly rolling a dice.

Q.E.D.
