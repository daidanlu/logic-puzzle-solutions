# The Stable Marriage Problem and the Gale-Shapley Algorithm

## The Stable Marriage Problem

The Stable Marriage Problem is a classic matching problem. It asks whether, given two sets of equal size where every agent has a complete and strict preference ordering over the agents on the other side, there always exists a stable perfect matching.

This problem was introduced by David Gale and Lloyd Shapley in 1962. Its constructive solution is known as the Gale-Shapley Algorithm. The algorithm not only proves that a stable matching must exist, but also gives a deterministic algorithm with time complexity $O(N^2)$.

---

## 1. System Setting

There are two finite sets of equal size: $N$ proposers, denoted by set $A$, and $N$ receivers, denoted by set $B$.

Each agent has a complete and strict preference list. That is, every element in set $A$ ranks all $N$ elements in set $B$ from $1$ to $N$, and every element in set $B$ ranks all $N$ elements in set $A$ from $1$ to $N$. There are no ties.

The goal is to pair these $2N$ agents into $N$ disjoint pairs, forming a perfect matching.

---

## 2. Stability and Blocking Pairs

A matching is unstable if the following situation occurs:

- There is an agent $a_1$ currently matched with $b_1$.
- There is an agent $b_2$ currently matched with $a_2$.
- In $a_1$'s preference list, $b_2$ is ranked higher than the current partner $b_1$.
- In $b_2$'s preference list, $a_1$ is ranked higher than the current partner $a_2$.

In this case, $a_1$ and $b_2$ would both prefer each other over their current partners. Such a pair is called a blocking pair.

Therefore, a matching is stable if and only if it contains no blocking pair.

---

## 3. Algorithmic Challenge

We want to answer two questions:

1. **Existence**: For any complete and strict preference lists, does there always exist at least one stable matching with no blocking pair?
2. **Constructive algorithm**: If such a matching always exists, can we design a deterministic algorithm with time complexity $O(N^2)$ to find it?

The main significance of the Gale-Shapley Algorithm is that it gives an explicit constructive process proving that the Stable Marriage Problem always has a solution.

---

# The Gale-Shapley Algorithm

To prove that the Stable Marriage Problem always has a solution, it is enough to run the algorithm introduced by David Gale and Lloyd Shapley in 1962.

This algorithm gives a constructive mathematical proof of the existence of stable matchings, and it is also a clean example of a finite-state process driven by greedy updates.

We call set $A$ the active side, or the proposers, and set $B$ the passive side, or the receivers.

---

## 1. Rules of the Gale-Shapley Algorithm

**Initial state:** Everyone is free.

**State-transition loop:**

As long as there is a free proposer in set $A$ who has not proposed to everyone in set $B$, repeat the following steps:

1. **Proposal step:** Choose a free proposer $a$. The proposer $a$ looks at his preference list and proposes to the highest-ranked receiver $b$ to whom he has not yet proposed.

2. **Review step:**

   - If $b$ is currently free, then $b$ accepts the proposal, and the two agents enter a temporary engaged state.
   - If $b$ is already engaged to someone else, say $a'$, then $b$ compares the current partner $a'$ with the new proposer $a$.
     - If $b$ prefers the current partner $a'$, then $b$ rejects $a$, and $a$ remains free.
     - If $b$ prefers the new proposer $a$, then $b$ rejects the current partner $a'$, sends $a'$ back to the free pool, and becomes temporarily engaged to $a$.

**Stopping condition:** When everyone is no longer free, or all proposers in $A$ have exhausted their preference lists, the algorithm stops. The current temporary engagements become the final matching.

---

## 2. Absolute Convergence Proof: Why the Algorithm Cannot Loop Forever

We prove that the system must stop in finitely many steps, with time complexity $O(N^2)$.

**Proof logic:**

1. Observe the behavior of a proposer $a$: he can only move down his own preference list from top to bottom. He never proposes to the same receiver twice, and he never goes backward.

2. There are $N$ proposers in total, and each proposer can make at most $N$ proposals.

3. Therefore, the maximum total number of proposals in the whole system is strictly bounded by:

$$N \times N = N^2$$

The finite-state process cannot fall into a backward cycle, and it must stop within $O(N^2)$ proposal steps.

---

## 3. Perfect Matching Proof: Why No One Remains Single

We prove that when the algorithm ends, all $N$ pairs are successfully formed, and no proposer is left unmatched.

**Proof logic by contradiction:**

1. Suppose that when the system stops, there is still a proposer $a$ who is single.

2. By the stopping condition, if $a$ is single, then he must have proposed to all $N$ receivers in set $B$, and all of them must have rejected him.

3. Observe the boundary condition of any receiver $b$: once a receiver becomes engaged, she can never become single again. She only moves to a better partner by replacing her current partner with someone ranked higher.

4. Since $a$ was rejected by all $N$ receivers, those $N$ receivers must all have been engaged when they rejected $a$.

5. A pigeonhole-principle contradiction appears: if $N$ receivers are engaged, then there must be $N$ proposers who are engaged. But under our assumption, $a$ is single, which means at most $N-1$ proposers are engaged. It is impossible for $N-1$ proposers to fill $N$ positions. This is a contradiction.

**Conclusion:** When the system stops, the result must be a perfect one-to-one matching.

---

## 4. Absolute Stability Proof: Why There Is No Blocking Pair

This is the core logical proof. We prove that the perfect matching output by the algorithm is stable, meaning that no two agents can mutually prefer each other over their final partners.

**Proof logic by contradiction:**

1. Suppose the system outputs a matching, but there exists a hidden blocking pair: agent $a$ and agent $b$ are not matched together, but each ranks the other strictly above their final legal partners, denoted by $b'$ and $a'$.

2. We trace backward through $a$'s proposal history. Since $a$ prefers $b$ over $b'$, when $a$ moved down his preference list, he must have proposed to $b$ before later proposing to $b'$.

3. Since $a$ once proposed to $b$, why did they not end up together? The only possible explanation is that $b$ either rejected $a$ immediately or accepted him temporarily and later rejected him.

4. In either case, by the state-transition rule for $b$, receiver $b$ rejects or abandons $a$ only because she has encountered someone ranked higher in her own preference list. Moreover, $b$'s later partners can only become better and never worse.

5. This means that $b$'s final legal partner $a'$ must be ranked strictly higher than $a$ in $b$'s preference list.

6. But this directly contradicts the assumption in Step 1, which says that $b$ prefers $a$ over $a'$. The logical chain breaks, and a contradiction is obtained.

**Conclusion:** The matching produced by the algorithm cannot contain a blocking pair.

---

## 5. Final Conclusion

The Gale-Shapley Algorithm gives both an existence proof and a constructive algorithm for the Stable Marriage Problem:

1. For any complete and strict preference lists, a stable matching always exists.
2. This stable matching can be constructed by the Gale-Shapley Algorithm.
3. The algorithm makes at most $N^2$ proposals, so it must stop in finitely many steps.
4. When the algorithm stops, it outputs a perfect matching.
5. The output matching contains no blocking pair, so it is stable.

Therefore, the Stable Marriage Problem always has a solution for any valid input, and the solution can be constructed by the Gale-Shapley Algorithm in $O(N^2)$ time.

$$\text{Q.E.D.}$$
