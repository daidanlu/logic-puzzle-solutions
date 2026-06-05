# Conway's Rational Tangles

This README explains a basic fact about Conway's rational tangle model: under a fixed convention for the allowed operations, every rational tangle obtained from the initial state by finitely many operations can be returned to the initial state by finitely many allowed operations.

The purpose is not to give a full textbook treatment of low-dimensional topology. Instead, the goal is to translate the tangle operations into arithmetic on rational numbers and prove that the resulting untangling process terminates.

---

## 1. Mathematical Modeling

Four people stand at the four corners of a square, and two ropes connect the four endpoints. The initial state consists of two horizontal parallel ropes, which is treated as the untangled state.

Only two operations are allowed:

- **Twist, denoted by $T$**: the two people on the right exchange positions, creating one crossing according to a fixed convention.
- **Rotate, denoted by $R$**: all four people move one position clockwise, equivalently rotating the endpoint frame by $90^\circ$.

In the rational tangle model, each state is assigned an extended rational number:

$$x \in \mathbb{Q} \cup \lbrace \infty \rbrace$$

The initial horizontal untangled state is assigned:

$$x=0$$

The vertical parallel state is assigned:

$$x=\infty$$

This README assumes that the previous operation sequence is known, or equivalently that the current rational value $x$ can be tracked algebraically. If no information about the previous operations is available and the current state cannot be inspected, then there is no single fixed untangling sequence that works for all possible states.

---

## 2. Fraction Invariant

The key idea in Conway's rational tangles is to record the tangle state by a fraction invariant. This value can be viewed intuitively as a slope in the endpoint frame, but more precisely it is the fraction invariant of a rational tangle, not the ordinary slope of an isolated curve in three-dimensional space.

With the convention used here, the two physical operations correspond to the following algebraic transformations.

### 2.1 Rotation

A clockwise rotation of the endpoint frame sends the fraction to its negative reciprocal:

$$R(x)=-\frac{1}{x}$$

with the conventions:

$$R(0)=\infty$$

$$R(\infty)=0$$

### 2.2 Twist

One right-hand twist corresponds to a Dehn twist. In the fraction model, it adds $1$ to the current value:

$$T(x)=x+1$$

with the convention:

$$T(\infty)=\infty$$

Therefore, starting from $0$, any finite sequence of $T$ and $R$ operations always produces an extended rational number.

---

## 3. Theorem

We claim that:

$$\text{Every rational tangle generated from }0\text{ by }T\text{ and }R\text{ can be returned to }0\text{ by finitely many }T\text{ and }R\text{ operations.}$$

Equivalently, once the current fraction is known, the tangle can be restored to the untangled state without using an inverse twist operation.

---

## 4. Untangling Algorithm

If the current value is already $0$, the tangle is already untangled.

If the current value is $\infty$, apply one rotation:

$$R(\infty)=0$$

If the current value is negative, repeatedly apply $T$ until it becomes nonnegative.

It remains to handle the case where the current value is a positive rational number. Write:

$$x=\frac{p}{q}$$

where $p,q$ are positive integers.

Apply one $R$ operation to $x$:

$$R\left(\frac{p}{q}\right)=-\frac{q}{p}$$

Then repeatedly apply $T$, which means repeatedly adding $1$, until the value first becomes nonnegative.

---

## 5. Termination Proof

After applying one $R$ operation to the positive rational number $x=p/q$, the state becomes:

$$-\frac{q}{p}$$

Use division with remainder on $q$ by $p$:

$$q=mp+r,\quad 0\le r<p$$

There are two cases.

### Case A: The Remainder Is Zero

If $r=0$, then:

$$q=mp$$

Therefore:

$$-\frac{q}{p}+m=-m+m=0$$

So after applying $T$ exactly $m$ times, the state returns to $0$, and the tangle is untangled.

### Case B: The Remainder Is Positive

If $r>0$, then the first nonnegative value is reached after applying $T$ exactly $m+1$ times. The new value is:

$$-\frac{q}{p}+(m+1)=\frac{-(mp+r)+mp+p}{p}=\frac{p-r}{p}$$

Since:

$$0<r<p$$

we have:

$$0<p-r<p$$

Thus, after one complete cycle, meaning one $R$ operation followed by several $T$ operations, the positive rational number $p/q$ is transformed into:

$$\frac{p-r}{p}$$

After reducing the fraction if necessary, the new numerator is at most $p-r$, and hence is strictly smaller than the old numerator $p$.

Therefore, every nonterminal cycle strictly decreases a positive integer complexity measure. Positive integers cannot decrease forever, so the algorithm must eventually enter Case A and reach:

$$x=0$$

This proves that the untangling process terminates after finitely many allowed operations.

$$\blacksquare$$

---

## 6. Conclusion

The central idea of Conway's rational tangles is to encode a tangle state as an extended rational number and convert the two physical operations into two simple algebraic transformations:

$$R(x)=-\frac{1}{x}$$

$$T(x)=x+1$$

The untangling algorithm is essentially a variant of the Euclidean algorithm. Each nonterminal cycle decreases an integer complexity measure, so the process cannot continue forever.

Therefore, under the rational tangle model and the operation convention used here, once the current fraction can be computed from the operation history, the tangle can be restored to the initial state using only finitely many $T$ and $R$ operations.
