# The Sylvester-Gallai Theorem

## 1. System Setup and Geometric Environment

* **Initial state**: In the two-dimensional Euclidean plane, we are given $n$ points, where $n \ge 3$.
* **Global constraint**: These $n$ points are not all collinear.

A line that passes through exactly two points of the given set is called an **ordinary line**.

---

## 2. Intuitive Question and Proof Goal

Any two distinct points determine a line.

A natural question is: can the $n$ points be arranged in a special way so that every line determined by any two of the points passes through at least 3 points of the set?

The Sylvester-Gallai theorem says that this is impossible.

**Goal**: prove that as long as the $n$ points are not all collinear, there must exist at least one ordinary line; that is, at least one line that passes through exactly two points of the given set.

---

# Kelly's Extremal Distance Proof

Kelly's proof does not directly enumerate all possible arrangements of the points. Instead, it considers distances from points to lines and chooses a smallest positive distance among finitely many point-line distances.

## Step 1: Define a Finite State Space and an Extremal Value

Consider all point-line pairs $(P,L)$ satisfying the following conditions:

* $P$ is one of the given $n$ points;
* $L$ is a line determined by two distinct points from the given set;
* $P$ does not lie on the line $L$.

Since the point set is finite, the number of lines determined by pairs of points is also finite. Therefore, the set of such point-line pairs $(P,L)$ is finite.

Since $P \notin L$, every such point-line pair has positive distance:

$$
d(P,L)>0
$$

Among finitely many positive numbers, there must be a minimum. Choose a point-line pair attaining this minimum distance and denote it by:

$$
(P_0,L_0)
$$

That is:

$$
d(P_0,L_0)
$$

is the minimum among all admissible point-line distances.

---

## Step 2: Assumption for Contradiction

Assume that the conclusion is false; that is, assume that there is no ordinary line.

This means that every line determined by two points from the given set passes through at least 3 points of the set.

In particular, the line $L_0$ is determined by two points from the given set. Therefore, under the contradiction assumption, $L_0$ contains at least 3 points of the given set.

---

## Step 3: Choose Two Points on $L_0$

Draw the perpendicular from $P_0$ to $L_0$, and denote the foot of the perpendicular by $Q$.

Since $L_0$ contains at least 3 given points, consider their positions relative to $Q$ along the line $L_0$. By the one-dimensional order on the line, we can choose two given points $A$ and $B$ on $L_0$ such that $A$ lies on the segment from $Q$ to $B$, and $A \neq B$.

Equivalently, $A$ is closer to the foot $Q$ than $B$ is, or $A=Q$.

Now connect $P_0$ with the farther point $B$ and obtain a new line:

$$
L_{\text{new}}=P_0B
$$

Since $A$ lies on $L_0$, while $L_{\text{new}}$ intersects $L_0$ at $B$, and $A \neq B$, we have:

$$
A \notin L_{\text{new}}
$$

Therefore, $(A,L_{\text{new}})$ is also an admissible point-line pair.

---

## Step 4: Construct a Smaller Point-Line Distance

Write:

$$
d(P_0,L_0)=P_0Q
$$

Now consider the distance from $A$ to the line $L_{\text{new}}=P_0B$, denoted by:

$$
d(A,L_{\text{new}})
$$

Since $A$ lies on the segment $QB$, the triangle $P_0AB$ sits in the corresponding position inside the triangle $P_0QB$.

The distances can be compared directly by an area argument.

The area of triangle $P_0QB$ is:

$$
[ P_0QB ]=\frac{1}{2}\cdot QB \cdot P_0Q
$$

On the other hand, using $P_0B$ as the base, the same area can also be written as:

$$
[ P_0QB ]=\frac{1}{2}\cdot P_0B \cdot d(Q,L_{\text{new}})
$$

Since $A$ lies on the segment $QB$, and $A$ is closer to $Q$ than $B$ is, the triangle $P_0AB$ shares the same directional structure from $P_0$ toward $L_0$ as triangle $P_0QB$, but has a shorter length along $L_0$. Therefore, the perpendicular distance from $A$ to the line $P_0B$ is strictly smaller than the perpendicular distance from $Q$ to the line $P_0B$, and the distance from $Q$ to the line $P_0B$ is strictly smaller than $P_0Q$.

Thus:

$$
d(A,L_{\text{new}})<P_0Q
$$

Equivalently:

$$
d(A,L_{\text{new}})<d(P_0,L_0)
$$

This contradicts the choice of $(P_0,L_0)$ as a point-line pair with globally minimal positive distance.

---

## Step 5: Conclusion of the Contradiction

The contradiction comes from the assumption in Step 2.

Therefore, it is impossible that every line determined by two given points contains at least 3 given points.

Hence, there must exist at least one line determined by two points of the given set that passes through exactly two points of the set.

This line is an ordinary line.

---

## Conclusion

For a finite set of points in the two-dimensional Euclidean plane, if the points are not all collinear, then there must exist an ordinary line.

That is, given $n \ge 3$ non-collinear points, there exists at least one line passing through exactly two of them.

This proves the Sylvester-Gallai theorem.
