# Bulgarian Solitaire

## Problem Statement

There are $N$ cards. Initially, the $N$ cards are divided into any number of nonempty piles.

A state can be written as an unordered multiset. For example:

$$\lbrace 5,4,1 \rbrace$$

means that there are three piles of sizes $5,4,1$.

At each step, the following operation is performed:

1. Remove one card from every current pile.
2. Put all removed cards together to form a new pile.
3. Remove any old pile whose size becomes $0$.

For example, starting from the state

$$\lbrace 5,4,1 \rbrace$$

the old piles first become

$$\lbrace 4,3,0 \rbrace$$

The pile of size $0$ disappears, leaving

$$\lbrace 4,3 \rbrace$$

Since there were originally $3$ piles, the $3$ removed cards form a new pile. Therefore the next state is:

$$\lbrace 4,3,3 \rbrace$$

This process is deterministic. Once the current state is known, the next state is uniquely determined.

---

## Theorem

Suppose the total number of cards $N$ is a triangular number. That is, for some positive integer $k$,

$$N=\frac{k(k+1)}{2}$$

Then, from any initial state, the system eventually reaches and stays at the unique fixed point:

$$\lbrace k,k-1,k-2,\dots,2,1 \rbrace$$

For example, when $N=10$,

$$10=\frac{4\cdot 5}{2}=4+3+2+1$$

so the final stable state is:

$$\lbrace 4,3,2,1 \rbrace$$

---

## Proof

### 1. The staircase state is a fixed point

Consider the state:

$$\lbrace k,k-1,k-2,\dots,2,1 \rbrace$$

This state has exactly $k$ piles.

After one operation, each old pile decreases by $1$, so the old piles become:

$$\lbrace k-1,k-2,\dots,1,0 \rbrace$$

The pile of size $0$ disappears, leaving:

$$\lbrace k-1,k-2,\dots,1 \rbrace$$

At the same time, since there were $k$ piles, the $k$ removed cards form a new pile of size $k$. Hence the new state is:

$$\lbrace k,k-1,k-2,\dots,1 \rbrace$$

This is exactly the original state. Therefore

$$\lbrace k,k-1,\dots,1 \rbrace$$

is a fixed point.

---

### 2. The system must eventually enter a cycle

The total number of cards $N$ is fixed, so there are only finitely many possible states.

Also, the transition rule is deterministic. Each state has exactly one next state.

Therefore, starting from any initial state, the system cannot keep producing new states forever. After finitely many steps, it must enter a cycle.

Thus, to prove convergence to the staircase state, it is enough to prove:

$$\text{If } N=\frac{k(k+1)}{2}\text{, then every cycle consists only of } \lbrace k,k-1,\dots,1 \rbrace$$

---

### 3. The maximum number of piles in a cycle gives a capacity bound

Assume that the system has entered a cycle.

Inside this cycle, the number of piles has a maximum value. Denote this maximum by $m$.

Thus, at every time in the cycle, the number of piles is at most $m$, and at least one state in the cycle has exactly $m$ piles.

By the transition rule,

$$\text{size of the newly created pile}=\text{number of current piles}$$

Therefore, in this cycle, every newly created pile has size at most $m$.

After a pile is created, its size decreases by $1$ at each subsequent step. Hence, at any time in the cycle, if the piles are ordered from largest to smallest, their sizes can be at most:

$$m,\ m-1,\ m-2,\ \dots,\ 2,\ 1$$

Therefore, the total number of cards in any state of the cycle is at most:

$$m+(m-1)+\cdots+1=\frac{m(m+1)}{2}$$

But the actual total number of cards is always

$$N=\frac{k(k+1)}{2}$$

Hence we must have:

$$\frac{k(k+1)}{2}\leq \frac{m(m+1)}{2}$$

Since triangular numbers strictly increase with their index, this implies:

$$m\geq k$$

Thus, the maximum number of piles in the cycle cannot be less than $k$.

---

### 4. The maximum number of piles in a cycle cannot be greater than $k$

Now we show that $m>k$ is impossible.

Suppose that some state in the cycle has $m$ piles, where $m>k$. Then the next operation creates a new pile of size $m$.

However, the total number of cards is only:

$$N=\frac{k(k+1)}{2}$$

A complete staircase of height $m$ would require:

$$\frac{m(m+1)}{2}$$

cards. Since $m>k$, we have:

$$\frac{m(m+1)}{2}>\frac{k(k+1)}{2}=N$$

Therefore, the system does not have enough cards to fill a complete staircase of height $m$.

In a cycle whose maximum number of piles is $m$, the ideal capacity pattern, ordered by pile age, is:

$$m,\ m-1,\ m-2,\ \dots,\ 1$$

But since the total number of cards is smaller than this full capacity, at least one position in this pattern is not filled.

As the operation is repeated, this gap moves toward smaller pile sizes. Eventually it reaches the position that would have contained a pile of size $1$. At that moment, a pile disappears, and the number of piles drops below $m$.

Thus, a state with more than $k$ piles cannot be stably maintained inside a cycle. Therefore:

$$m\leq k$$

Together with the previous inequality $m\geq k$, we obtain:

$$m=k$$

---

### 5. When the maximum number of piles is $k$, the cycle must be the staircase state

We now know that the maximum number of piles in the cycle is exactly $k$.

By the capacity bound above, the total number of cards in any cycle state is at most:

$$k+(k-1)+\cdots+1=\frac{k(k+1)}{2}$$

But the actual total number of cards is exactly:

$$N=\frac{k(k+1)}{2}$$

Therefore, all the upper bounds must be attained exactly.

So the pile sizes must be exactly:

$$k,\ k-1,\ k-2,\ \dots,\ 2,\ 1$$

No card can be missing from any position. If any pile were smaller than its upper bound, the total number of cards would be less than $N$, which is impossible.

Therefore, the only possible state in the cycle is:

$$\lbrace k,k-1,\dots,1 \rbrace$$

This state has already been shown to be a fixed point. Hence the cycle is a one-state cycle.

---

## Conclusion

When

$$N=\frac{k(k+1)}{2}$$

the Bulgarian Solitaire system, starting from any initial state, reaches the unique fixed point after finitely many steps:

$$\boxed{\lbrace k,k-1,k-2,\dots,2,1 \rbrace}$$

For $N=10$, the final state is:

$$\boxed{\lbrace 4,3,2,1 \rbrace}$$

---

## Main Idea

The proof does not examine every possible initial state. Instead, it studies the maximum number of piles $m$ inside a possible cycle and uses it to derive a capacity bound.

The invariant is the total number of cards:

$$N=\frac{k(k+1)}{2}$$

The key upper bound is the staircase capacity determined by the maximum number of piles $m$:

$$\frac{m(m+1)}{2}$$

When the total number of cards is itself a triangular number, the capacity bound forces every cycle to be the complete staircase. Therefore, every trajectory eventually enters the unique fixed point.

$$\text{Q.E.D.}$$
