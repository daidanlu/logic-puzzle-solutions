# A Linear Algebra Proof of the Oddtown Theorem

This README gives a concise linear algebra proof of the Oddtown Theorem.

---

## 1. Problem Setup

Suppose a town has $N$ residents. There are $M$ different clubs, denoted by:

$$C_1, C_2, \dots, C_M$$

These clubs satisfy the following two conditions:

1. Each club has an odd number of members.
2. Any two different clubs have an even number of common members.

The question is: under these conditions, how many clubs can there be at most?

The Oddtown Theorem states that:

$$M \le N$$

That is, the number of clubs satisfying the two conditions cannot exceed the number of residents.

---

## 2. Vector Representation

For each club $C_i$, define its incidence vector:

$$\mathbf{v}_i=(x_1,x_2,\dots,x_N) \in \mathbb{F}_2^N$$

where:

- if the $k$-th resident belongs to $C_i$, then $x_k=1$;
- if the $k$-th resident does not belong to $C_i$, then $x_k=0$.

All computations are done over the finite field $\mathbb{F}_2$. Equivalently, we only keep track of parity.

---

## 3. Translating the Conditions into Algebra

First, the size of club $C_i$ modulo $2$ is equal to the dot product of its incidence vector with itself:

$$\mathbf{v}_i \cdot \mathbf{v}_i = |C_i| \pmod 2$$

Since every club has odd size, we have:

$$\mathbf{v}_i \cdot \mathbf{v}_i = 1$$

Second, for two different clubs $C_i$ and $C_j$, the size of their intersection modulo $2$ is equal to the dot product of their incidence vectors:

$$\mathbf{v}_i \cdot \mathbf{v}_j = |C_i \cap C_j| \pmod 2$$

Since any two different clubs have an even-sized intersection, when $i \ne j$ we have:

$$\mathbf{v}_i \cdot \mathbf{v}_j = 0$$

Therefore, the incidence vectors satisfy:

$$\mathbf{v}_i \cdot \mathbf{v}_j =
\begin{cases}
1, & i=j,\\
0, & i \ne j.
\end{cases}$$

---

## 4. Constructing the Incidence Matrix

Place the $M$ incidence vectors as row vectors of an $M \times N$ matrix:

$$A=
\begin{pmatrix}
\mathbf{v}_1 \\
\mathbf{v}_2 \\
\vdots \\
\mathbf{v}_M
\end{pmatrix}$$

Now consider the matrix product $AA^T$. This is an $M \times M$ matrix, and its entry in row $i$ and column $j$ is:

$$\left(AA^T\right)_{ij}=\mathbf{v}_i \cdot \mathbf{v}_j$$

By the dot product relations above, we obtain:

$$AA^T=I_M$$

where $I_M$ is the $M \times M$ identity matrix.

---

## 5. Rank Inequality

Since $AA^T=I_M$, we have:

$$\operatorname{rank}(AA^T)=\operatorname{rank}(I_M)=M$$

On the other hand, the rank of a matrix product cannot exceed the rank of either factor. Hence:

$$\operatorname{rank}(AA^T) \le \operatorname{rank}(A)$$

Since $A$ is an $M \times N$ matrix, its rank is at most the number of columns:

$$\operatorname{rank}(A) \le N$$

Combining these inequalities gives:

$$M=\operatorname{rank}(I_M)=\operatorname{rank}(AA^T) \le \operatorname{rank}(A) \le N$$

Therefore:

$$M \le N$$

$$\blacksquare$$

---

## 6. Conclusion

The Oddtown Theorem shows that, on a set of $N$ residents, if every club has odd size and every pair of different clubs has even-sized intersection, then the total number of clubs is at most $N$.

The key idea is to view each club as a vector in $\mathbb{F}_2^N$. The parity conditions become dot product conditions, and these conditions imply that the incidence matrix satisfies:

$$AA^T=I_M$$

The rank inequality then directly gives:

$$M \le N$$

Thus, the combinatorial problem is naturally solved using linear algebra over a finite field.
