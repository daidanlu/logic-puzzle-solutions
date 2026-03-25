# The Generalized Pirate Game

Original problem reference: <https://en.wikipedia.org/wiki/Pirate_game>

This directory contains a backward induction proof of the generalized pirate game (with $N$ pirates and $M$ coins), along with a Python algorithmic game theory simulation.

## Problem Setup

There are $N$ perfectly rational and extremely intelligent pirates, ranked by seniority from $N, N-1, \dots, 2, 1$ (pirate $N$ is the most senior, pirate $1$ is the most junior).  
They must divide $M$ gold coins (in the classical version, $M=100$).

The rules are as follows:
1. The most senior surviving pirate proposes a distribution of the coins.
2. All surviving pirates (including the proposer) vote on the proposal.
3. If the number of votes in favor is ≥ half of the total number of surviving pirates, the proposal passes, coins are distributed accordingly, and the game ends.
4. If the number of votes in favor is < half, the proposer is thrown into the sea and eaten by sharks. The next most senior pirate takes over, and the process restarts from step 1.

The pirates' utility function (priority order) is:
**Survival** > **Maximize coins received** > **Bloodthirst (if outcomes are equal, prefer others to die)**

What happens when the number of pirates $N$ is much larger than the number of coins $M$?

## Three Phase Transitions in the Optimal Strategy

When $M=100$, as $N$ increases, the system undergoes three phase transitions:

- **Phase 1 ($N \le 200$)**: The proposer always survives by bribing just enough pirates to secure half the votes; the remaining coins are kept.
- **Phase 2 ($N = 201$ or $202$)**: The proposer must distribute all coins to survive; they receive zero coins but remain alive.
- **Phase 3 ($N > 202$)**: Coins are insufficient to buy enough votes. Survival depends entirely on free votes from pirates who fear certain death in the next round. In this phase, only specific pirate indices can survive; all others are doomed regardless of strategy.

## Mathematical Proof (Backward Induction)

Let the current number of surviving pirates be $N$, and the total number of coins be $M$. The proposer (pirate $N$) needs at least:

```math
V_{required} = \lceil \frac{N}{2} \rceil
```

votes to pass the proposal.

### Phase 1: $N \le 2M$

When $N \le 2M$, the proposer votes for themselves (1 vote), and needs to buy:

```math
V_{buy} = \lceil \frac{N}{2} \rceil - 1
```

votes.

Due to the pirates' bloodthirsty preference, to bribe a pirate, the proposer must offer at least 1 coin more than what that pirate would receive in the $N-1$ scenario.

By backward induction, the proposer only needs to identify pirates who would receive $0$ coins in the $N-1$ scenario and give each of them 1 coin to secure their votes.

Thus, the proposer keeps:

```math
Profit_{N} = M - \left( \lceil \frac{N}{2} \rceil - 1 \right)
```

coins.

### Phase 2: $N = 2M + 1$ or $2M + 2$

Take $M=100$ as an example.

When $N = 201$, 101 votes are required. The proposer votes for themselves (1 vote) and distributes all 100 coins to the 100 pirates who would receive nothing in the $N=200$ case. This yields 101 votes, survival, and zero profit.

When $N = 202$, 101 votes are required. The proposer votes for themselves (1 vote) and distributes all 100 coins to the 100 pirates who would receive nothing in the $N=201$ case. This yields 101 votes, survival, and zero profit.

### Phase 3: $N > 2M + 2$

When $N \ge 203$, coins are no longer sufficient to buy enough votes. The only hope of survival comes from pirates who would certainly die in the next round if the proposal fails; these pirates will cast **free votes** to survive.

- For pirate 203: 102 votes are needed. They have 1 self-vote and can buy 100 votes with coins, totaling 101 votes. Pirate 202 has a survival strategy, so no one gives a free vote. Pirate 203 is doomed.
- For pirate 204: 102 votes are needed. They have 1 self-vote and can buy 100 votes. Pirate 203 knows that if 204 dies, they will become the proposer and certainly die, so 203 gives a free vote. Total:

```math
1 (\text{self}) + 100 (\text{bought}) + 1 (\text{from 203}) = 102
```

Thus, pirate 204 survives.

Continuing this reasoning:
- Pirate 205: needs 103 votes. 1 (self) + 100 (bought) + 0 (free, since 204 survives if 205 dies). Total 101 → doomed.
- Pirate 206: needs 103 votes. 1 + 100 + 1 (from doomed 205) = 102 → doomed.
- Pirate 207: needs 104 votes. 1 + 100 + 2 (from doomed 206, 205) = 103 → doomed.
- Pirate 208: needs 104 votes. 1 + 100 + 3 (from doomed 207, 206, 205) = 104:

```math
1 (\text{self}) + 100 (\text{bought}) + 3 (\text{free}) = 104
```

Thus, pirate 208 survives.

### Pattern

By induction, we observe that the number of free votes required for survival crosses powers of 2.

Let $S$ be the set of pirate indices that can survive:

```math
S = \{ N \mid N = 2M + 2^k, \quad k \in \mathbb{N} \} \cup \{ 2M + 1 \}
```

Therefore, when $M=100$, all surviving pirate indices greater than 200 satisfy:

```math
N = 200 + 2^k
```

Thus, the survival sequence converges to:

**201, 202, 204, 208, 216, 232, 264, 328...**

All pirates between these values are inevitably thrown into the sea, regardless of any strategy.

Q.E.D.
