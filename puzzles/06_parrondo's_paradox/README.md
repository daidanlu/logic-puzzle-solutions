# Parrondo's Paradox

This directory contains a mathematical proof of the well-known Parrondo's paradox in stochastic processes, along with a Monte Carlo Markov chain simulator implemented in Python.

## 1. Core Setup and Parameter Definitions

We introduce a small constant $\epsilon = 0.005$ to represent the casino bias, ensuring that the games are slightly unfavorable to the player at the edge of fairness. Let the player's current capital be denoted by $C$.

### Game A (Simple Coin Toss)

The player tosses a biased coin with fixed probabilities:

Winning probability: $p = \frac{1}{2} - \epsilon = 0.495$  
Losing probability: $1 - p = 0.505$

### Game B (State-Dependent Markov Chain)

Game B involves two different coins. The choice depends on the current capital modulo 3:

State 0 (when $C \bmod 3 = 0$): use the bad coin.  
Winning probability: $p_1 = \frac{1}{10} - \epsilon = 0.095$

State 1 or 2 (when $C \bmod 3 \neq 0$): use the good coin.  
Winning probability: $p_2 = \frac{3}{4} - \epsilon = 0.745$

## 2. Proof of Losing Behavior in Individual Games

### Expectation of Game A

The expected change in capital per round is:

$$
E[\Delta C_A] = 1 \cdot p + (-1) \cdot (1 - p) = 2p - 1 = -2\epsilon = -0.01 < 0
$$

Conclusion: In the long run, Game A yields a negative linear drift. It is a losing game.

### Steady-State Analysis of Game B

The process $C \bmod 3$ forms a discrete-time Markov chain with three states (0, 1, 2).

By standard results on Markov chains, the necessary and sufficient condition for a positive drift is:

$$
p_1 \cdot p_2^2 > (1 - p_1) \cdot (1 - p_2)^2
$$

We first consider the ideal case $\epsilon = 0$:

Left-hand side (winning force):

$$
\left(\frac{1}{10}\right)\left(\frac{3}{4}\right)^2 = \frac{9}{160}
$$

Right-hand side (losing force):

$$
\left(1 - \frac{1}{10}\right)\left(1 - \frac{3}{4}\right)^2 = \left(\frac{9}{10}\right)\left(\frac{1}{16}\right) = \frac{9}{160}
$$

In the absence of bias, the system is perfectly fair.

However, with $\epsilon = 0.005 > 0$, we obtain:

$$
p_1 \cdot p_2^2 < (1 - p_1) \cdot (1 - p_2)^2
$$

Conclusion: Due to prolonged residence in state 0 (the bad coin), the losing force dominates. Game B is also a losing game.

## 3. Emergence of the Paradox: Winning Mixed Game C

We now construct Game C: at each step, play Game A with probability 0.5 and Game B with probability 0.5.

This random mixture alters the transition structure, forming a new Markov chain. The resulting transition probabilities are:

Winning probability in state 0:

$$
q_1 = 0.5 \cdot p + 0.5 \cdot p_1 = 0.5 \cdot (0.495 + 0.095) = 0.295
$$

Winning probability in state 1 or 2:

$$
q_2 = 0.5 \cdot p + 0.5 \cdot p_2 = 0.5 \cdot (0.495 + 0.745) = 0.620
$$

Substituting into the drift condition:

Left-hand side (winning force):

$$
q_1 \cdot q_2^2 = (0.295)(0.620)^2 \approx 0.1134
$$

Right-hand side (losing force):

$$
(1 - q_1) \cdot (1 - q_2)^2 = (0.705)(0.380)^2 \approx 0.1018
$$

We obtain the reversal:

$$
q_1 \cdot q_2^2 > (1 - q_1) \cdot (1 - q_2)^2
$$

The winning force (0.1134) strictly exceeds the losing force (0.1018).

## 4. Conclusion and Insight

Why does combining two losing games produce a winning one?

The failure of Game B is caused by the system spending too much time in state 0, where the win probability is extremely low (0.095).

Game A, despite having a negative expectation, acts as a source of stochastic noise. This noise perturbs the stationary distribution of the Markov chain, significantly reducing the residence time in state 0 and increasing the frequency of states 1 and 2, where the win probability is high (0.745).

As a result, the global expectation shifts from negative to positive, producing the paradoxical outcome.

Q.E.D.