# Byzantine Generals Problem

This directory presents both a mathematical proof and a Python simulation of the classical **Byzantine Generals Problem**. Under the **Oral Messages** model, if the system contains at most Byzantine faulty nodes, then the necessary and sufficient condition for achieving interactive consistency is:

$$
N \ge 3m + 1
$$

where the total number of nodes is:

$$
N
$$

and the maximum number of Byzantine faulty nodes the system can tolerate is:

$$
m
$$

---

## 1. Model and Consistency Conditions

The system consists of two types of roles:

- one commander
- several lieutenants

Let the number of lieutenants be:

$$
n
$$

Then the total number of nodes is:

$$
N = n + 1
$$

Nodes are divided into two categories:

- **Loyal nodes**: nodes that strictly follow the protocol
- **Traitor nodes**: nodes that may send arbitrary, contradictory, or forged messages to different recipients

The system must satisfy **Interactive Consistency**.

### IC1: Agreement

All loyal lieutenants must obey the same order.

### IC2: Validity

If the commander is loyal, then all loyal lieutenants must obey the original order issued by the commander.

---

## 2. Impossibility Basis: Why 3 Nodes Cannot Tolerate 1 Traitor

Consider the smallest counterexample:

- one commander
- two lieutenants
- at most one traitor

Then the total number of nodes is:

$$
N = 3
$$

and the number of tolerable traitors is:

$$
m = 1
$$

We construct two scenarios that are indistinguishable from the perspective of a loyal lieutenant.

### Scenario A: The Commander Is Loyal and Lieutenant 2 Is a Traitor

The commander sends the order:

$$
\text{Attack}
$$

Lieutenant 1 receives two messages:

$$
\text{Commander: Attack}
$$

$$
\text{Lieutenant 2: Retreat}
$$

Therefore, the information set of Lieutenant 1 is:

$$
\{\text{Commander: Attack}, \text{Lieutenant 2: Retreat}\}
$$

### Scenario B: The Commander Is a Traitor and Both Lieutenants Are Loyal

The traitorous commander sends:

$$
\text{to Lieutenant 1: Attack}
$$

$$
\text{to Lieutenant 2: Retreat}
$$

Loyal Lieutenant 2 truthfully forwards the message it received, so Lieutenant 1 still receives:

$$
\{\text{Commander: Attack}, \text{Lieutenant 2: Retreat}\}
$$

### Contradiction

For Lieutenant 1, the input in these two scenarios is exactly the same, but the protocol requires different correct outputs.

In Scenario A, to satisfy the validity condition, Lieutenant 1 must choose:

$$
\text{Attack}
$$

In Scenario B, to satisfy the agreement condition, Lieutenant 1 must remain consistent with loyal Lieutenant 2, and therefore must choose:

$$
\text{Retreat}
$$

Hence, no deterministic algorithm can make Lieutenant 1 produce the correct decision in both cases.

### Conclusion

When:

$$
N = 3
$$

and:

$$
m = 1
$$

Byzantine agreement is impossible.

This shows that if the number of nodes is too small, the system falls into a logical deadlock caused by indistinguishable local information.

---

## 3. Special Case: How 4 Nodes Can Tolerate 1 Traitor

When the system needs to tolerate exactly one Byzantine node, the smallest solvable system size is:

$$
N = 4
$$

and at the same time:

$$
m = 1
$$

This exactly satisfies:

$$
N = 3m + 1
$$

Lamport's **OM(1)** algorithm achieves consistency under this condition.

### 3.1 Algorithm Procedure

Let the three lieutenants be:

$$
L_1
$$

$$
L_2
$$

$$
L_3
$$

Let the initial order issued by the commander be:

$$
v
$$

#### Step 1

The commander sends the initial order:

$$
v
$$

to all lieutenants.

#### Step 2

Each lieutenant forwards the value it received from the commander to the other two lieutenants.

Let the values received by the three lieutenants be:

$$
v_1
$$

$$
v_2
$$

$$
v_3
$$

Then each lieutenant forwards its corresponding value to the other two lieutenants.

#### Step 3

Each lieutenant finally collects three values:

- one value directly from the commander
- two forwarded values from the other lieutenants

It then applies the majority-vote function:

$$
majority(\cdot)
$$

and determines its final action accordingly.

---

## 4. Correctness Proof for the 4-Node Case

### Case 1: The Commander Is Loyal

If the commander is loyal, it sends the same order:

$$
v
$$

to all lieutenants.

Since the system contains at most one traitor, among the three lieutenants at most one can be traitorous. Suppose the traitor is:

$$
L_3
$$

Then for the loyal lieutenant:

$$
L_1
$$

the received information may be:

$$
v
$$

$$
v
$$

$$
x
$$

where the first two values come respectively from:

- the commander
- the forwarding message of loyal lieutenant:

$$
L_2
$$

and the third value:

$$
x
$$

comes from the forged message of the traitorous lieutenant.

Therefore, the result of majority voting is:

$$
majority(v, v, x) = v
$$

Similarly, loyal lieutenant:

$$
L_2
$$

also obtains:

$$
v
$$

Thus all loyal lieutenants execute:

$$
v
$$

This satisfies:

- IC1: all loyal lieutenants agree
- IC2: if the commander is loyal, then loyal lieutenants obey its original order

---

### Case 2: The Commander Is a Traitor

In this case, all three lieutenants are loyal.

Suppose the traitorous commander sends the following three values to the three lieutenants:

$$
x
$$

$$
y
$$

$$
z
$$

That is:

- the value sent to:

$$
L_1
$$

is:

$$
x
$$

- the value sent to:

$$
L_2
$$

is:

$$
y
$$

- the value sent to:

$$
L_3
$$

is:

$$
z
$$

Since all three lieutenants are loyal, they truthfully forward the values they received.

Therefore, lieutenant:

$$
L_1
$$

finally collects:

$$
(x, y, z)
$$

Lieutenant:

$$
L_2
$$

finally collects:

$$
(x, y, z)
$$

Lieutenant:

$$
L_3
$$

finally collects:

$$
(x, y, z)
$$

So all loyal lieutenants end up with exactly the same input. For the same deterministic majority function, they must therefore produce the same output.

Hence, all loyal lieutenants reach agreement, satisfying IC1.

Since the commander itself is traitorous in this case, IC2 no longer imposes any requirement.

---

## 5. Conclusion of the Special Case

Therefore, when tolerating exactly one Byzantine faulty node:

- three nodes are insufficient
- four nodes are sufficient

That is:

$$
N = 3
$$

is unsolvable, while:

$$
N = 4
$$

is solvable.

In other words, to tolerate one Byzantine faulty node, the system requires at least four nodes.

---

## 6. General Proof: Why the General Condition Must Be 3m + 1

We now give a general proof based on **set theory, intersection properties, and quorums**.

---

## 6.1 Definitions

Let the set of all nodes be:

$$
V
$$

The total number of nodes is:

$$
|V| = N
$$

Let the set of Byzantine malicious nodes be:

$$
B
$$

with:

$$
|B| \le m
$$

Let the set of loyal nodes be:

$$
C = V \setminus B
$$

In a distributed system, a loyal node does not need to wait for messages from the entire network before making a decision. It only needs to collect a sufficiently large subset of messages in order to decide safely. Denote this threshold by:

$$
Q
$$

Here:

$$
Q
$$

is the **quorum** required by the protocol, and also the minimum local threshold for majority voting.

---

## 6.2 Liveness Constraint

In the worst case, at most:

$$
m
$$

malicious nodes may remain silent and send no messages.

To prevent the protocol from waiting forever for those nodes, the quorum size cannot exceed the number of potentially responsive nodes. Therefore, it must satisfy:

$$
Q \le N - m
$$

Otherwise, the system would lose liveness by waiting for replies from malicious nodes.

---

## 6.3 Safety Constraint

Suppose two loyal nodes collect two quorum sets:

$$
Q_i
$$

and:

$$
Q_j
$$

and make decisions independently based on the messages they receive.

To guarantee that they do not make conflicting decisions, the intersection of these two quorum sets must contain at least one loyal node. Otherwise, if all nodes in the intersection were malicious, they could send contradictory information to the two sides and create a fork.

Since there are at most:

$$
m
$$

malicious nodes, we must require:

$$
|Q_i \cap Q_j| > m
$$

This guarantees that the intersection contains at least one loyal node.

---

## 6.4 Derivation via the Inclusion-Exclusion Principle

By the inclusion-exclusion principle in set theory:

$$
|Q_i \cap Q_j| = |Q_i| + |Q_j| - |Q_i \cup Q_j|
$$

In the worst case, the union of the two quorums covers the entire system, so:

$$
|Q_i \cup Q_j| = N
$$

Assume further that the two quorums have the same size:

$$
|Q_i| = |Q_j| = Q
$$

Then the minimum lower bound of the intersection is:

$$
|Q_i \cap Q_j| = 2Q - N
$$

Combining this with the safety condition gives:

$$
2Q - N > m
$$

that is:

$$
2Q > N + m
$$

Now use the largest quorum allowed by the liveness condition:

$$
Q = N - m
$$

Substituting this into the inequality yields:

$$
2(N - m) > N + m
$$

Simplifying gives:

$$
2N - 2m > N + m
$$

$$
N > 3m
$$

Since:

$$
N
$$

and:

$$
m
$$

are both integers, this is equivalent to:

$$
N \ge 3m + 1
$$

Q.E.D.

---

## 7. General Conclusion

From the set-theoretic derivation above, if a system is expected to:

- remain live in the presence of at most Byzantine nodes
- and guarantee that no two loyal nodes make conflicting decisions

then the total number of nodes must satisfy:

$$
N \ge 3m + 1
$$

This is the general lower bound for the Byzantine Generals Problem under the Oral Messages model.

---

## 8. Summary

The core difficulty of the Byzantine Generals Problem is that:

- malicious nodes may send mutually contradictory information to different recipients
- loyal nodes can only make decisions based on local observations
- if the system lacks sufficient redundancy, the same input may correspond to different required correct outputs, making the problem undecidable

The conclusion can be understood at two levels.

### Special Case: Tolerating 1 Traitor

- three nodes are insufficient
- four nodes are sufficient

That corresponds to:

$$
N = 3
$$

being unsolvable, and:

$$
N = 4
$$

being solvable.

### General Case: Tolerating an Arbitrary Number of Byzantine Nodes

To tolerate:

$$
m
$$

Byzantine faulty nodes, the total number of nodes must satisfy:

$$
N \ge 3m + 1
$$

Among these cases, the 4-node system tolerating 1 traitor is exactly the smallest solvable special case of the general theorem.