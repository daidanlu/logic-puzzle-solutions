# Infinite Prisoners and Hats Problem

This directory contains the mathematical proof and Python simulation verification for the Infinite Prisoners and Hats problem.

## Theorem

We claim that in the hat-guessing game with countably infinitely many prisoners, where each prisoner simultaneously guesses the color of their own hat and each hat is either black or white, there exists a deterministic strategy such that, for every possible actual hat assignment, only finitely many prisoners guess incorrectly.

---

## 1. State Space and the Equivalence Relation

Let the index set of prisoners be the natural numbers:

$$
\mathbb{N}=\lbrace 1,2,3,\dots \rbrace
$$

Let the set of hat colors be:

$$
C=\lbrace 0,1 \rbrace
$$

where $0$ and $1$ represent the two possible hat colors.

Define the global state space as the set of all infinite binary sequences:

$$
S=\lbrace 0,1 \rbrace^{\mathbb{N}}
$$

Suppose the actual hat assignment chosen by the warden is

$$
s=(s_1,s_2,s_3,\dots)\in S
$$

We define a binary relation $\sim$ on $S$ by declaring that, for any $x,y\in S$,

$$
x\sim y
\iff
\left|\lbrace i\in\mathbb{N}:x_i\neq y_i\rbrace\right|<\infty
$$

That is, two sequences are equivalent if and only if they differ in only finitely many coordinates.

### Lemma 1.1

The relation $\sim$ is an equivalence relation.

### Proof

**Reflexivity.** For every $x\in S$, the set

$$
\lbrace i\in\mathbb{N}:x_i\neq x_i\rbrace
$$

is empty, hence finite. Therefore,

$$
x\sim x
$$

**Symmetry.** If $x\sim y$, then the set of indices where $x$ and $y$ differ is the same as the set of indices where $y$ and $x$ differ. Hence,

$$
x\sim y \implies y\sim x
$$

**Transitivity.** Suppose $x\sim y$ and $y\sim z$. Then

$$
\lbrace i\in\mathbb{N}:x_i\neq z_i\rbrace
\subseteq
\lbrace i\in\mathbb{N}:x_i\neq y_i\rbrace
\cup
\lbrace i\in\mathbb{N}:y_i\neq z_i\rbrace
$$

Since a union of two finite sets is finite, it follows that

$$
x\sim z
$$

Therefore, $\sim$ is an equivalence relation.

As a result, $S$ is partitioned into disjoint equivalence classes. The quotient set is denoted by

$$
S/{\sim}
$$

For any $x\in S$, its equivalence class is denoted by

$$
[x]
$$

---

## 2. Invoking the Axiom of Choice

Each equivalence class in $S/{\sim}$ is nonempty. By the Axiom of Choice, there exists a choice function

$$
f:S/{\sim}\longrightarrow S
$$

such that for every equivalence class $C\in S/{\sim}$,

$$
f(C)\in C
$$

Before the game begins, all prisoners agree on this same function $f$. Although $f$ cannot in general be described by an explicit algorithm, its existence is guaranteed by the Axiom of Choice.

Thus, for every equivalence class, the prisoners have fixed one distinguished representative sequence.

---

## 3. Local Observation and the Common Equivalence Class

Now suppose the actual hat assignment is the sequence

$$
s=(s_1,s_2,s_3,\dots)\in S
$$

Then there is a unique equivalence class containing it, namely

$$
[s]
$$

Prisoner $i$ can see every hat except their own. So prisoner $i$ observes the incomplete configuration

$$
s_{-i}=(s_1,\dots,s_{i-1},?,s_{i+1},\dots)
$$

Given this observation, prisoner $i$ knows that the actual sequence must be one of the following two possibilities:

$$
s^{(0)}=(s_1,\dots,0,\dots)
$$

and

$$
s^{(1)}=(s_1,\dots,1,\dots)
$$

These two sequences differ in exactly one coordinate, namely the $i$-th coordinate. Hence,

$$
s^{(0)}\sim s^{(1)}
$$

Therefore, regardless of the true value of the $i$-th hat, prisoner $i$ can determine the same equivalence class.

### Lemma 3.1

All prisoners infer the same equivalence class, namely the true class $[s]$.

### Proof

Each prisoner sees all coordinates except one. Any two full sequences consistent with that prisoner's observation differ in at most one coordinate. Therefore, all such possibilities lie in a single equivalence class. Since the true sequence $s$ is one of them, that class must be $[s]$.

Thus every prisoner, despite having a different missing coordinate, identifies the same equivalence class.

---

## 4. The Strategy and Why Only Finitely Many Prisoners Fail

Since every prisoner identifies the same class $[s]$, they all apply the shared choice function and select the same representative sequence

$$
r=f([s])
$$

Write this representative as

$$
r=(r_1,r_2,r_3,\dots)
$$

The agreed strategy is:

- prisoner $i$ announces $r_i$ as their guess.

Thus the vector of all guesses is exactly the sequence $r$.

Now, by the definition of the choice function,

$$
r=f([s])\in [s]
$$

By the definition of the equivalence class, this means precisely that

$$
r\sim s
$$

Expanding the definition of $\sim$, we obtain

$$
\left|\lbrace i\in\mathbb{N}:r_i\neq s_i\rbrace\right|<\infty
$$

But the set

$$
\lbrace i\in\mathbb{N}:r_i\neq s_i\rbrace
$$

is exactly the set of prisoners whose guesses are wrong.

Therefore, only finitely many prisoners guess incorrectly.

---

## Conclusion

We have proved that there exists a deterministic strategy such that, for every possible infinite hat assignment,

$$
\left|\lbrace i\in\mathbb{N}:\text{prisoner }i\text{ guesses incorrectly}\rbrace\right|<\infty
$$

Hence, in the countably infinite prisoners hat problem, it is always possible to guarantee that all but finitely many prisoners guess correctly.

$$
\blacksquare
$$
