# De Bruijn Sequence

## 1. Mathematical Model

Consider a digital password lock with a rolling-window input mechanism. The password has length $n$, and each position has $k$ possible symbols.

For example, for a standard 4-digit decimal PIN, we have:

$$k=10, \quad n=4$$

The lock does not require the user to enter a full 4-digit password and then press a confirmation button. Instead, the user continuously enters digits, and the lock always checks the latest $n$ symbols entered.

Therefore, if the input string has length $L$, it produces:

$$L-n+1$$

sliding windows of length $n$.

For example, the input string `00001` produces two 4-digit windows:

$$0000, \quad 0001$$

Thus, 5 key presses test two different 4-digit passwords.

---

## 2. Goal

The total number of possible passwords of length $n$ is:

$$k^n$$

We want to construct the shortest possible input string such that every password of length $n$ appears as a consecutive substring.

Equivalently, we want to prove that there exists a shortest string that overlaps all $k^n$ passwords, with each password appearing exactly once.

---

## 3. Lower Bound on the Number of Key Presses

Any input string of length $L$ can produce at most $L-n+1$ windows of length $n$.

If it covers all $k^n$ passwords, then it must satisfy:

$$L-n+1 \ge k^n$$

Therefore:

$$L \ge k^n+n-1$$

Hence, any valid input string must require at least:

$$k^n+n-1$$

key presses.

It remains to prove that this lower bound is achievable.

---

## 4. Constructing the State Transition Graph

Construct a directed graph $G$.

### 4.1 Vertices

Each vertex represents a string of length $n-1$.

Therefore, the number of vertices is:

$$k^{n-1}$$

For example, in a 4-digit decimal PIN lock, each vertex is a 3-digit string such as `000`, `123`, or `999`.

### 4.2 Directed Edges

For any vertex:

$$a_1a_2\cdots a_{n-1}$$

and any possible input symbol $x$, add a directed edge:

$$a_1a_2\cdots a_{n-1} \to a_2a_3\cdots a_{n-1}x$$

This means that if the current rolling-window state is $a_1a_2\cdots a_{n-1}$, then after entering $x$, the new state becomes $a_2a_3\cdots a_{n-1}x$.

For example, from vertex `123`, entering `4` moves the state to `234`. Thus, we have the edge:

$$123 \to 234$$

This edge corresponds to the complete 4-digit password `1234`.

---

## 5. One-to-One Correspondence Between Edges and Passwords

Every edge in $G$ corresponds to exactly one password of length $n$.

An edge is uniquely determined by two pieces of information:

1. its starting vertex, which gives the first $n-1$ symbols;
2. its edge label, which gives the final symbol.

Therefore, the password represented by an edge is:

$$a_1a_2\cdots a_{n-1}x$$

Conversely, every password of length $n$ uniquely determines one edge: its first $n-1$ symbols determine the starting vertex, and its last symbol determines the edge label.

Thus:

$$\text{edges of }G \iff \text{passwords of length }n$$

Each vertex has $k$ outgoing edges, and there are $k^{n-1}$ vertices. Hence, the total number of edges is:

$$k^{n-1}\cdot k = k^n$$

This is exactly the number of passwords that must be covered.

---

## 6. Existence of an Eulerian Circuit

We want a continuous walk that traverses every edge of $G$ exactly once.

In graph theory, such a closed walk is called an Eulerian circuit.

A standard criterion for a directed graph to have an Eulerian circuit is:

1. all nonzero-degree vertices belong to one strongly connected component;
2. every vertex has equal in-degree and out-degree.

We now verify these two conditions.

### 6.1 Equal In-Degree and Out-Degree

From any vertex, we may append any of the $k$ possible symbols. Therefore, every vertex has out-degree:

$$d^+(v)=k$$

Similarly, any vertex can be reached by choosing any of the $k$ possible preceding symbols. Therefore, every vertex has in-degree:

$$d^-(v)=k$$

Thus, for every vertex $v$, we have:

$$d^-(v)=d^+(v)=k$$

### 6.2 Strong Connectivity

Let $u$ and $v$ be any two vertices of length $n-1$.

Starting from $u$, enter the symbols of $v$ one by one. After $n-1$ steps, the rolling window becomes exactly $v$.

Hence, every vertex can reach every other vertex, so $G$ is strongly connected.

---

## 7. From an Eulerian Circuit to an Input String

Since $G$ is strongly connected and every vertex has equal in-degree and out-degree, $G$ has an Eulerian circuit.

Following this Eulerian circuit traverses every edge exactly once.

Since each edge corresponds to one password of length $n$, the Eulerian circuit covers all $k^n$ passwords, with each password appearing exactly once.

To convert the Eulerian circuit into an actual input string, first write the $n-1$ symbols of the starting vertex. Then, for each edge traversed, write the newly appended symbol represented by that edge.

Since the graph has $k^n$ edges, the total input length is:

$$(n-1)+k^n$$

Equivalently:

$$k^n+n-1$$

---

## 8. Optimality

We already proved that any input string covering all $k^n$ passwords must have length at least:

$$k^n+n-1$$

The Eulerian circuit construction proves that this length is achievable.

Therefore, the minimum number of key presses for a rolling-window password lock is:

$$\boxed{k^n+n-1}$$

This means that a de Bruijn sequence gives a theoretically optimal input strategy.

---

## 9. Example: 4-Digit Decimal PIN

For a 4-digit decimal PIN, we have:

$$k=10, \quad n=4$$

Therefore, the minimum number of key presses is:

$$10^4+4-1=10003$$

Naive enumeration would require:

$$4\times 10000=40000$$

key presses.

Thus, under the rolling-window mechanism, a de Bruijn sequence reduces the number of key presses from 40000 to the theoretical minimum of 10003.

---

## 10. Conclusion

The existence of de Bruijn sequences can be proved using Eulerian circuits in directed graphs.

The key correspondence is:

$$\text{length-}n\text{ passwords} \iff \text{edges of the de Bruijn graph}$$

Since the graph is strongly connected and every vertex has equal in-degree and out-degree, it contains an Eulerian circuit.

This Eulerian circuit gives a shortest input string containing every password of length $n$, and its length is:

$$\boxed{k^n+n-1}$$

Therefore, the construction both covers all passwords and achieves the theoretical minimum length.

$$\blacksquare$$
