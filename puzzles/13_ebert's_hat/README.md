# Ebert's Hat Problem

This directory contains a proof-oriented explanation of the classical **Ebert's Hat Problem** in theoretical computer science (TCS). It presents a geometric hedging strategy based on the $(7,4,3)$ Hamming code, reinterpreted through the topology of a three-circle Venn diagram.

The strategy shows how, in a zero-error and zero-communication distributed system, algebraic coding can raise the group's survival probability from the naive $50\%$ benchmark to $87.5\%$.

---

## 0. Problem Setup

A warden places **7 prisoners** in an interrogation room and sets up a life-or-death game.

1. **State assignment**: The warden places one hat on each prisoner. Each hat is either **black** or **white**, denoted by $0$ and $1$, respectively. Each hat color is chosen independently and uniformly at random, with each color having probability $50\%$.
2. **Information isolation**: Each prisoner can see the hat colors of the other 6 prisoners, but cannot see the color of their own hat.
3. **Zero-communication constraint**: After the hats are placed, the prisoners are forbidden from communicating in any way, including speech, eye contact, gestures, or physical signals.
4. **Action space**: All prisoners must simultaneously write down exactly one of the following three actions: **black**, **white**, or **Pass**.

The prisoners are released if and only if both of the following conditions hold:

1. At least one prisoner guesses their own hat color correctly.
2. No prisoner guesses their own hat color incorrectly.

Passing is neither correct nor incorrect.

If at least one prisoner guesses incorrectly, or if all 7 prisoners pass, the group loses immediately. If the prisoners act independently, or if they use a trivial strategy such as having one prisoner guess randomly while all others pass, the success probability is only $50\%$.

---

## 1. System Mapping and Parity Rings

To break the $50\%$ success barrier, we use a three-way set intersection structure, namely a Venn diagram topology, to formulate the $(7,4,3)$ Hamming-code strategy.

Let the set of prisoners be:

$$P=\lbrace 1,2,3,4,5,6,7 \rbrace$$

Let the hat color of prisoner $i$ be:

$$v_i \in \lbrace 0,1 \rbrace$$

where $0$ denotes black and $1$ denotes white.

The true global state is:

$$\mathbf{v}=(v_1,v_2,\dots,v_7)$$

Hence, the total number of possible global states is:

$$2^7=128$$

Define three overlapping subsets of $P$, called **parity rings**:

$$S_A=\lbrace 1,2,3,5 \rbrace$$

$$S_B=\lbrace 1,2,4,6 \rbrace$$

$$S_C=\lbrace 1,3,4,7 \rbrace$$

These three parity rings have the following topological structure:

- Prisoner 1 lies in the common intersection $S_A \cap S_B \cap S_C$.
- Prisoner 2 lies in $S_A \cap S_B$.
- Prisoner 3 lies in $S_A \cap S_C$.
- Prisoner 4 lies in $S_B \cap S_C$.
- Prisoner 5 belongs only to $S_A$.
- Prisoner 6 belongs only to $S_B$.
- Prisoner 7 belongs only to $S_C$.

In other words, the 7 prisoners correspond exactly to the 7 nonempty regions of the three parity rings.

---

## 2. Construction of the Death Set

Before the game begins, the prisoners agree on a special subset:

$$W \subseteq \lbrace 0,1 \rbrace^7$$

This set is called the **death set**. In coding-theoretic terms, it is precisely the codeword set of the corresponding Hamming code.

A state vector $\mathbf{x}=(x_1,x_2,\dots,x_7)$ belongs to $W$ if and only if it satisfies the following three even-parity equations:

$$\sum_{i \in S_A} x_i \equiv 0 \pmod 2$$

$$\sum_{i \in S_B} x_i \equiv 0 \pmod 2$$

$$\sum_{i \in S_C} x_i \equiv 0 \pmod 2$$

That is, each parity ring must contain an even number of entries equal to $1$.

### Cardinality of the Death Set

The colors of prisoners 1, 2, 3, and 4 may be chosen arbitrarily, giving:

$$2^4=16$$

possible assignments.

Once these four values are fixed, the colors of prisoners 5, 6, and 7 are uniquely determined by the three even-parity equations above. Therefore, the death set $W$ contains exactly:

$$|W|=16$$

states.

Since the total number of global states is $128$, we have:

$$\Pr(\mathbf{v}\in W)=\frac{16}{128}=\frac{1}{8}$$

---

## 3. Action Axioms

During the game, each prisoner $i$ can see the hat colors of the other 6 prisoners, denoted by $\mathbf{v}_{-i}$.

All prisoners follow the same action rule:

$$\text{Assume that the true global state is not in } W.$$

In other words, every prisoner acts under the assumption that the true state does not belong to the death set $W$.

For prisoner $i$, they consider the two possible values of their own hat color, $0$ and $1$, producing two candidate global states:

$$\mathbf{v}^{(0)} \quad \text{and} \quad \mathbf{v}^{(1)}$$

They then apply the following rule:

1. If there exists $c \in \lbrace 0,1 \rbrace$ such that:

   $$\mathbf{v}^{(c)}\in W$$

   then prisoner $i$ concludes that color $c$ would place the global state inside the death set. Since the prisoner acts under the assumption that the true state is not in $W$, they guess the opposite color:

   $$A_i=1-c$$

2. If, for both $c=0$ and $c=1$, we have:

   $$\mathbf{v}^{(c)}\notin W$$

   then prisoner $i$ cannot infer a definite answer from the agreed rule, and therefore chooses:

   $$A_i=\text{Pass}$$

---

## 4. Proof of Survival Probability

Whether the system survives depends only on whether the true state $\mathbf{v}$ belongs to the death set $W$.

---

### Case 1: The True State Lies in the Death Set

Assume that:

$$\mathbf{v}\in W$$

This happens with probability:

$$\Pr(\mathbf{v}\in W)=\frac{1}{8}$$

For any prisoner $i$, the true state $\mathbf{v}$ itself is in $W$. Therefore, when prisoner $i$ assumes their own color to be the true value $v_i$, the corresponding candidate state is:

$$\mathbf{v}^{(v_i)}=\mathbf{v}\in W$$

By the action rule, prisoner $i$ rejects the color $v_i$ that would place the state in $W$, and instead guesses the opposite color:

$$A_i=1-v_i$$

Thus, all 7 prisoners speak, and all 7 prisoners guess incorrectly.

Therefore, when $\mathbf{v}\in W$, the system fails.

---

### Case 2: The True State Lies Outside the Death Set

Assume that:

$$\mathbf{v}\notin W$$

This happens with probability:

$$\Pr(\mathbf{v}\notin W)=1-\frac{1}{8}=\frac{7}{8}$$

Since $\mathbf{v}$ does not satisfy the three even-parity equations, at least one parity ring has odd parity. Define the syndrome, or error pattern, of the three parity rings by:

$$\mathbf{s}=(s_A,s_B,s_C)$$

where:

$$s_A=\sum_{i\in S_A} v_i \pmod 2$$

$$s_B=\sum_{i\in S_B} v_i \pmod 2$$

$$s_C=\sum_{i\in S_C} v_i \pmod 2$$

Because $\mathbf{v}\notin W$, we have:

$$\mathbf{s}\neq (0,0,0)$$

The three binary parity values have $2^3-1=7$ possible nonzero error patterns. These 7 nonzero patterns correspond exactly to the 7 Venn-diagram regions occupied by the prisoners.

More explicitly, each prisoner corresponds to one nonzero parity vector:

$$h_1=(1,1,1)$$

$$h_2=(1,1,0)$$

$$h_3=(1,0,1)$$

$$h_4=(0,1,1)$$

$$h_5=(1,0,0)$$

$$h_6=(0,1,0)$$

$$h_7=(0,0,1)$$

These vectors are pairwise distinct and enumerate all nonzero three-bit binary vectors. Therefore, there exists a unique prisoner $k$ such that:

$$h_k=\mathbf{s}$$

This prisoner $k$ lies exactly in the intersection of all parity rings whose parity is currently odd.

If prisoner $k$ flips their own color, every odd parity ring is repaired into an even parity ring, while every even parity ring remains even. Hence, after flipping $v_k$, the resulting candidate state belongs to $W$.

Equivalently, from the viewpoint of prisoner $k$, the color that would make the candidate state fall into $W$ is:

$$c=1-v_k$$

By the action rule, prisoner $k$ guesses the opposite color:

$$A_k=1-c=v_k$$

Therefore, prisoner $k$ necessarily guesses correctly.

For any other prisoner $j\neq k$, the corresponding parity vector $h_j$ is not equal to the error pattern $\mathbf{s}$. Thus, flipping $v_j$ cannot repair the syndrome $\mathbf{s}$ into the zero vector. Equivalently, no matter whether prisoner $j$ assumes their own color to be $0$ or $1$, they cannot obtain a candidate state that belongs to $W$.

Therefore, every prisoner $j\neq k$ chooses:

$$A_j=\text{Pass}$$

Thus, when $\mathbf{v}\notin W$, exactly one prisoner speaks, and that prisoner is guaranteed to be correct; the other 6 prisoners pass. The system succeeds.

---

## 5. Conclusion

The size of the death set $W$ is:

$$|W|=16$$

The total number of global states is:

$$2^7=128$$

Therefore, the failure probability is:

$$\Pr(\text{Failure})=\frac{16}{128}=\frac{1}{8}$$

The survival probability is:

$$\Pr(\text{Survival})=1-\frac{1}{8}=\frac{7}{8}=87.5\%$$

Through the parity decomposition of the $(7,4,3)$ Hamming code, all failure risk is concentrated inside the death set $W$, which occupies only $\frac{1}{8}$ of the state space. On the remaining $\frac{7}{8}$ of the state space, the Venn-diagram topology guarantees the existence of exactly one prisoner who can safely and correctly speak.

Therefore, the strategy accepts a $12.5\%$ systematic failure risk in exchange for an $87.5\%$ overall success probability.

$$\blacksquare$$
