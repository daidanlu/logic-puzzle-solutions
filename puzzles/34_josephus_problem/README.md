# Binary Shift Representation of the Josephus Problem

## The Josephus Problem

The Josephus problem is a classical discrete mathematics model with a cyclic recursive structure. In the case where the step size is 2, it can be reduced to a simple binary shift formula, avoiding explicit simulation of the entire circular linked list.

## System Setting and Topological Environment

There are $N$ agents, numbered from $1$ to $N$, arranged in a circle according to their labels.

The elimination process starts from label $1$:
$1$ eliminates $2$, $3$ eliminates $4$, $5$ eliminates $6$, and so on. The elimination process continues along the circle, skipping already eliminated nodes, until only one surviving node remains.

The goal is to find the final survivor, denoted by:

$$W(N)$$

## Direct Method and Computational Cost

The most direct method is to construct a circular linked list and simulate the process with step size $2$. Since this method removes nodes one by one, its time complexity is:

$$O(N)$$

When $N$ is very large, linear simulation becomes inefficient. Therefore, we want to find a closed-form expression that does not rely on linked-list simulation.

---

# Proof via Recursive Structure and Bitwise Representation

The key to the problem is to find a structural invariant in the elimination process.

## Step 1: Define the Invariant State: $N = 2^m$

First consider the special case:

$$N = 2^m$$

That is, the initial number of agents is exactly an integer power of $2$.

In the first round of elimination, all even-numbered labels are eliminated:

$$2,4,6,\dots,2^m$$

The remaining nodes are:

$$1,3,5,\dots,2^m-1$$

The number of remaining nodes is:

$$2^{m-1}$$

Moreover, the next elimination starts again from label $1$.

Therefore, the problem is structurally reduced to the same type of problem: the number of remaining agents changes from $2^m$ to $2^{m-1}$, while the starting point is still label $1$.

By applying this argument recursively, when the initial number of agents is an integer power of $2$, the final survivor must be:

$$W(2^m)=1$$

---

## Step 2: Algebraically Decompose an Arbitrary $N$

For any positive integer $N$, let $2^m$ be the largest power of $2$ not exceeding $N$. Then $N$ can be uniquely written as:

$$N = 2^m + L$$

where:

$$0 \leq L < 2^m$$

Here, $L$ represents the excess part of $N$ beyond the largest power of $2$.

---

## Step 3: Eliminate $L$ Nodes First, Bringing the System into the $2^m$ State

Starting from label $1$, the first $L$ eliminations remove:

$$2,4,6,\dots,2L$$

Therefore, after $L$ eliminations, the number of surviving nodes becomes:

$$N-L = 2^m$$

That is, the number of remaining agents is exactly an integer power of $2$.

At the same time, the next node to perform an elimination is:

$$2L+1$$

Therefore, among the remaining $2^m$ nodes, label $2L+1$ becomes the new starting point.

---

## Step 4: Apply the Result for the $2^m$ Case

By Step 1, when the number of remaining agents is $2^m$, if the same elimination process starts from some node, then that starting node corresponds to position $1$ in the relabeled system, and hence it will become the final survivor.

At this point, the new starting point is the original label:

$$2L+1$$

Thus, for any $N = 2^m + L$, the final survivor is:

$$W(N)=2L+1$$

where:

$$L = N - 2^m$$

Equivalently:

$$W(N)=2(N-2^m)+1$$

---

## Step 5: Binary Representation and Circular Left Shift

Write $N$ in binary. Since:

$$N = 2^m + L$$

the term $2^m$ is represented by the leading $1$, while $L$ corresponds to the lower-order bits following it.

Therefore, the binary representation of $N$ can be written as:

$$N = (1b_{m-1}b_{m-2}\dots b_0)_2$$

where:

$$L = (b_{m-1}b_{m-2}\dots b_0)_2$$

From the closed-form formula:

$$W(N)=2L+1$$

we obtain the following operations:

1. Remove the leading $1$ from the binary representation of $N$, obtaining $L$.
2. Shift $L$ left by one bit, obtaining $2L$.
3. Fill the lowest bit with $1$, obtaining $2L+1$.

That is, the binary representation of $W(N)$ is equivalent to:

$$(b_{m-1}b_{m-2}\dots b_0 1)_2$$

This is precisely the result of moving the leading $1$ of $N$ to the lowest bit.

Therefore, under a fixed machine word length or a fixed effective bit width, the formula can be interpreted as applying one circular left shift to the effective binary representation of $N$:

$$(1b_{m-1}b_{m-2}\dots b_0)_2 \longmapsto (b_{m-1}b_{m-2}\dots b_0 1)_2$$

It is worth noting that if $N$ is an arbitrary-precision large integer, then from the perspective of input length, reading and moving all binary bits still takes time proportional to the number of bits. However, compared with linked-list simulation over $N$ agents, this method reduces the problem to computation over the length of the binary representation.

---

## Example

Let:

$$N=41$$

Then:

$$41 = 32 + 9 = 2^5 + 9$$

So:

$$L=9$$

Substituting into the formula:

$$W(41)=2L+1=2\cdot 9+1=19$$

From the binary perspective:

$$41=(101001)_2$$

Move the leading $1$ to the lowest bit:

$$101001 \longmapsto 010011$$

After removing the leading zero, we obtain:

$$10011_2 = 19$$

Therefore:

$$W(41)=19$$

---

## Conclusion

For the Josephus problem with step size $2$ starting from label $1$, if:

$$N = 2^m + L,\qquad 0 \leq L < 2^m$$

then the final survivor is:

$$\boxed{W(N)=2L+1}$$

Equivalently, in binary representation, the final survivor can be obtained by moving the leading $1$ of $N$ to the lowest bit. This shows that the recursive elimination process can be reduced to a simple binary shift structure, thereby avoiding explicit circular linked-list simulation.
