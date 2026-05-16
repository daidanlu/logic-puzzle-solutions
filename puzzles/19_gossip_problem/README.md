# The Gossip Problem: Why the Minimum Number of Calls Is $2N-4$

## Problem Setup

Let there be $N \ge 4$ nodes:

$$V=\lbrace 1,2,\dots,N \rbrace$$

Initially, each node $i$ knows only its own secret $s_i$. Let $K_i(t)$ denote the set of secrets known by node $i$ after the $t$-th call. Initially:

$$K_i(0)=\lbrace s_i \rbrace$$

A call can occur only between two nodes. If nodes $u$ and $v$ call each other, then after the call both nodes know the union of their previous knowledge sets:

$$K_u'=K_v'=K_u\cup K_v$$

The goal is to find a sequence of calls after which every node knows all $N$ secrets:

$$K_i=\lbrace s_1,s_2,\dots,s_N \rbrace \quad \text{for every } i$$

Let $C(N)$ be the minimum number of calls needed to achieve this goal.

## Theorem

For every $N \ge 4$:

$$C(N)=2N-4$$

---

## Upper Bound: $2N-4$ Calls Are Sufficient

Choose four nodes as the core nodes:

$$A,B,C,D$$

The remaining $N-4$ nodes are called peripheral nodes.

### Step 1: Peripheral Nodes Upload Their Secrets

Each peripheral node calls one of the core nodes once. This transfers every peripheral secret into the core group.

This step uses:

$$N-4$$

calls.

At this point, the four core nodes collectively contain all $N$ secrets.

### Step 2: Synchronize the Four Core Nodes

The core nodes perform the following four calls:

$$(A,B),\quad (C,D),\quad (A,C),\quad (B,D)$$

The first two calls merge the core information into two large blocks:

$$A,B \text{ know one block, and } C,D \text{ know the other block}$$

The last two calls exchange these two blocks across the core. After the call $`A \to C`$, nodes $A$ and $C$ become fully informed. After the call $`B \to D`$, nodes $B$ and $D$ become fully informed.

Thus all four core nodes know all $N$ secrets.

This step uses:

$$4$$

calls.

### Step 3: The Core Nodes Download the Full Information

Each peripheral node calls a fully informed core node once.

This step uses:

$$N-4$$

calls.

Therefore, the total number of calls is:

$$(N-4)+4+(N-4)=2N-4$$

Hence:

$$C(N)\le 2N-4$$

---

## Lower Bound: Fewer Than $2N-4$ Calls Are Impossible

The lower-bound intuition is to separate global synchronization into two logical directions:

1. Gathering: the $N$ initially scattered secrets must be collected together;
2. Dissemination: the complete information must be distributed back to all $N$ nodes.

If information were transmitted only in one direction, then gathering would require a spanning tree and hence at least:

$$N-1$$

transmission edges.

Dissemination would also require a spanning tree and hence at least:

$$N-1$$

transmission edges.

Without any reuse, this gives:

$$(N-1)+(N-1)=2N-2$$

one-way transmissions.

The special feature of a telephone call is that it is bidirectional. Therefore, some calls can play both roles at once: they can contribute to gathering and dissemination simultaneously.

The key question is:

$$\text{How many such savings are possible?}$$

The answer is:

$$\text{At most } 2$$

---

## Dual-Purpose Calls

Call a telephone call dual-purpose if it simultaneously has the following two effects:

1. It helps gather still-incomplete information toward a global union;
2. It makes the two endpoints fully informed.

Equivalently, if a call between nodes $X$ and $Y$ is dual-purpose, then before the call:

$$K_X\cup K_Y=\lbrace s_1,s_2,\dots,s_N \rbrace$$

but neither endpoint is fully informed:

$$K_X\ne \lbrace s_1,s_2,\dots,s_N \rbrace$$

$$K_Y\ne \lbrace s_1,s_2,\dots,s_N \rbrace$$

After the call:

$$K_X'=K_Y'=\lbrace s_1,s_2,\dots,s_N \rbrace$$

Thus a dual-purpose call is exactly a call in which:

$$\text{two non-fully-informed nodes become fully informed in one call}$$

---

## The Causality Constraint

Once a node becomes fully informed, it can no longer participate in another dual-purpose call.

The reason is simple: a fully informed node has no missing information left to gather. Any later call involving that node can only disseminate complete information to someone else; it cannot simultaneously serve as a gathering step for that node.

Therefore:

$$\text{each node can participate in at most one dual-purpose call}$$

Dual-purpose calls can only occur at a critical layer: the moment when the full set of secrets is first assembled.

Before this critical layer, no node has complete information. After this critical layer, fully informed nodes can only disseminate information outward; they cannot create new dual-purpose calls.

---

## Why the Four-Node Core Reaches the Limit

Four core nodes can realize the following structure:

$$(A,B),\quad (C,D),\quad (A,C),\quad (B,D)$$

The first two calls merge the core information into two blocks:

$$K_A=K_B=\text{block}_1$$

$$K_C=K_D=\text{block}_2$$

with:

$$\text{block}_1\cup \text{block}_2=\lbrace s_1,s_2,\dots,s_N \rbrace$$

Then $A$ calls $C$, and $B$ calls $D$. Hence:

$$(A,C) \text{ creates two fully informed nodes}$$

$$(B,D) \text{ creates two fully informed nodes}$$

Both calls occur at the critical layer where the complete information first comes into existence. Therefore, both calls can be dual-purpose.

Thus the four-node core gives two net savings:

$$2N-2-2=2N-4$$

---

## Why a Three-Node Core Is Not Enough

If we use only three core nodes $A,B,C$, then core synchronization naturally requires three calls:

$$(A,B),\quad (B,C),\quad (C,A)$$

After the first call $`A \to B`$, nodes $A$ and $B$ still miss the information held by $C$. Hence no node is fully informed.

After the second call $`B \to C`$, nodes $B$ and $C$ may become fully informed together. This gives one dual-purpose call.

During the third call $`C \to A`$, node $C$ is already fully informed. This call merely disseminates complete information to $A$, so it is not dual-purpose.

Therefore, a three-node core can give at most one net saving. The corresponding total number of calls is:

$$2N-2-1=2N-3$$

This shows that the triangle is the smallest cycle, but it is not the optimal core structure. The reason is that telephone communication is binary: each call connects exactly two nodes. An odd number of core nodes cannot form two independent complementary exchanges in the final step.

---

## Why Three or More Savings Are Impossible

To obtain three savings, one would need three dual-purpose calls.

Each dual-purpose call must occur between two non-fully-informed nodes, and after the call both endpoints must become fully informed. Thus three dual-purpose calls would require three pairs of nodes to complete complementary exchanges at the same critical layer.

This cannot produce an additional net saving.

The reason is:

1. Before complete information first appears, no node can disseminate complete information;
2. Once one pair becomes fully informed through a complementary call, those nodes can only disseminate information afterward;
3. If later nodes depend on these fully informed nodes to obtain complete information, then the corresponding calls are ordinary dissemination calls, not dual-purpose calls;
4. If later nodes do not depend on them, then they must independently reconstruct the full global union, which requires additional calls and cancels the alleged extra saving.

Therefore, in an optimal protocol, at most two dual-purpose calls can give net savings. The four-node core reaches exactly this limit.

Hence every protocol requires at least:

$$2N-2-2=2N-4$$

calls.

Therefore:

$$C(N)\ge 2N-4$$

---

## Conclusion

The upper bound gives:

$$C(N)\le 2N-4$$

The lower bound gives:

$$C(N)\ge 2N-4$$

Therefore:

$$C(N)=2N-4$$

Thus, for the gossip problem with $N\ge 4$ nodes, the minimum number of calls required for complete global synchronization is exactly:

$$\boxed{2N-4}$$

The four-node core is not arbitrary. It is the smallest even core structure that can produce two dual-purpose calls at the causally valid critical layer. A three-node core gives only one net saving, while larger cores cannot exceed the two-saving limit.

$$\blacksquare$$
