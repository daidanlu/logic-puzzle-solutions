# Colonel Blotto Game: No Pure Equilibrium and the Marginal Structure of Mixed Strategies

## 1. Background

The Colonel Blotto Game is a resource allocation game. Two players have the same total amount of resources and must simultaneously distribute them across several battlefields. On each battlefield, the player who allocates more resources wins that battlefield.

The main phenomenon is that, in typical symmetric cases, a fixed allocation is not stable. The opponent can reallocate resources, win a majority of battlefields by small margins, and strategically abandon the remaining battlefields.

This README proves two claims:

1. In the discrete example $S=6,N=3$, there is no pure-strategy Nash equilibrium.
2. In the continuous symmetric version, the one-battlefield marginal distribution of a mixed equilibrium has a uniform structure.

---

## 2. Mathematical Model

Consider two players, A and B. Each player has total resource $S$ and must allocate it across $N$ battlefields.

For a concrete and verifiable discrete proof, take:

$$S=6, \qquad N=3$$

A pure strategy is an allocation vector:

$$X=(x_1,x_2,x_3)$$

where:

$$x_1+x_2+x_3=6, \qquad x_i\ge 0$$

If A uses strategy $X$ and B uses strategy $Y$, A's payoff can be written as:

$$u(X,Y)=\sum_{i=1}^{3}\operatorname{sgn}(x_i-y_i)$$

Here:

- if $x_i>y_i$, then A wins battlefield $i$;
- if $x_i<y_i$, then A loses battlefield $i$;
- if $x_i=y_i$, then battlefield $i$ is tied.

Since both players have the same resources and face the same battlefield rules, this is a symmetric zero-sum game.

---

## 3. Pure-Strategy Nash Equilibrium

A pure-strategy Nash equilibrium is a pair of fixed strategies $(X,Y)$ such that, while the opponent's strategy is fixed, neither player can improve their payoff by unilaterally changing their own strategy.

In a symmetric zero-sum game, if a stable pure equilibrium exists, then some fixed allocation must be impossible for the opponent to defeat by reallocating resources.

The following proof shows that no such fixed allocation exists in the discrete case $S=6,N=3$.

---

## 4. Discrete Theorem

## Theorem

In the Colonel Blotto Game with $S=6,N=3$, there is no pure-strategy Nash equilibrium.

## Proof

Since the three battlefields are symmetric, we may sort A's allocation in nonincreasing order without loss of generality:

$$a\ge b\ge c, \qquad a+b+c=6$$

There are only seven possible sorted allocation types:

$$\lbrace (6,0,0),(5,1,0),(4,2,0),(4,1,1),(3,3,0),(3,2,1),(2,2,2) \rbrace$$

For each allocation by A, B has a counter-allocation that wins two out of the three battlefields.

| A's allocation | B's counter-allocation | Outcome |
|---|---|---|
| $(6,0,0)$ | $(0,3,3)$ | B loses the first battlefield and wins the other two |
| $(5,1,0)$ | $(0,3,3)$ | B loses the first battlefield and wins the other two |
| $(4,2,0)$ | $(0,3,3)$ | B loses the first battlefield and wins the other two |
| $(4,1,1)$ | $(0,3,3)$ | B loses the first battlefield and wins the other two |
| $(3,3,0)$ | $(4,0,2)$ | B wins the first and third battlefields and loses the second |
| $(3,2,1)$ | $(0,3,3)$ | B loses the first battlefield and wins the other two |
| $(2,2,2)$ | $(3,3,0)$ | B wins the first two battlefields and loses the third |

Thus, for every pure strategy of A, there exists a pure strategy of B that wins a majority of the battlefields.

Therefore, no fixed allocation can prevent the opponent from obtaining a better payoff by reallocating resources. Hence this discrete version has no pure-strategy Nash equilibrium.

$$\blacksquare$$

---

## 5. Meaning of the Counter-Allocations

The proof above shows that the problem is not a particular weak allocation. Rather, every static allocation exposes some structural weakness.

A balanced allocation can be defeated by concentrating resources:

$$(2,2,2) \prec (3,3,0)$$

A concentrated allocation leaves weak battlefields:

$$(4,1,1) \prec (0,3,3)$$

A local-advantage allocation can still be bypassed:

$$(3,3,0) \prec (4,0,2)$$

Here $X\prec Y$ means that strategy $Y$ defeats strategy $X$.

Thus, the pure-strategy structure of the Colonel Blotto Game is similar to rock-paper-scissors: no fixed strategy stably dominates all others.

---

## 6. Why Mixed Strategies Are Needed

Since fixed allocations do not form an equilibrium, players must use mixed strategies. Instead of choosing one fixed allocation vector, a player randomly samples an allocation vector from a probability distribution.

The purpose of randomization is not arbitrary randomness. It is to prevent the opponent from targeting a predictable weakness.

In the continuous version, resources can be divided arbitrarily. A strategy vector satisfies:

$$x_1+x_2+\cdots+x_N=S, \qquad x_i\ge 0$$

In the classical symmetric homogeneous version, the one-battlefield marginal distribution in equilibrium has the form:

$$x_i\sim \operatorname{Uniform}\left(0,\frac{2S}{N}\right)$$

This statement concerns the marginal distribution on a single battlefield. It does not mean that the allocations across battlefields are independent. Since total resources are fixed, allocations across battlefields must be correlated.

---

## 7. Necessity of the Uniform Marginal Distribution

Suppose the opponent's allocation on any single battlefield has cumulative distribution function $F$ and density function $f$.

If I allocate $x$ to a battlefield, then my probability of winning that battlefield is:

$$F(x)$$

In the continuous case, ties have probability $0$, so tie terms can be ignored.

If I choose a deterministic allocation:

$$X=(x_1,x_2,\ldots,x_N)$$

then my expected number of won battlefields is:

$$E(X)=\sum_{i=1}^{N}F(x_i)$$

The allocation must also satisfy the resource constraint:

$$\sum_{i=1}^{N}x_i=S$$

On the interior support of an equilibrium, a player cannot improve expected payoff by moving a small amount of resource from one battlefield to another. Therefore, all battlefield allocations used in the support must have equal marginal returns.

Using Lagrange multipliers, define:

$$L(x_1,\ldots,x_N,\lambda)=\sum_{i=1}^{N}F(x_i)-\lambda\left(\sum_{i=1}^{N}x_i-S\right)$$

Taking the partial derivative with respect to each $x_i$ gives:

$$\frac{\partial L}{\partial x_i}=F'(x_i)-\lambda$$

At an optimum:

$$F'(x_i)-\lambda=0$$

Since:

$$F'(x_i)=f(x_i)$$

we obtain:

$$f(x_i)=\lambda$$

Thus, inside the support of the equilibrium, the marginal density must be constant. A distribution with constant density is a uniform distribution.

Therefore, the allocation on a single battlefield cannot concentrate around a high-probability point. Otherwise, the opponent could allocate slightly more than that likely value and win the battlefield at low cost.

---

## 8. Why the Upper Bound Is $2S/N$

Suppose the one-battlefield marginal distribution is uniform on $[0,M]$.

The expectation of this uniform distribution is:

$$\mathbb{E}[x_i]=\frac{M}{2}$$

There are $N$ battlefields, and the total resource is always $S$, so:

$$\sum_{i=1}^{N}\mathbb{E}[x_i]=S$$

By symmetry:

$$N\cdot \frac{M}{2}=S$$

Solving for $M$ gives:

$$M=\frac{2S}{N}$$

Hence the one-battlefield equilibrium marginal distribution is:

$$x_i\sim \operatorname{Uniform}\left(0,\frac{2S}{N}\right)$$

This is only a marginal distribution. A full mixed strategy must also specify a joint distribution such that every sampled vector satisfies:

$$x_1+x_2+\cdots+x_N=S$$

Therefore, one cannot simply sample $N$ independent uniform random variables, since that would usually violate the total resource constraint.

---

## 9. Geometric Meaning of Lagrange Multipliers

The geometric meaning of the Lagrange multiplier method is that, at a constrained optimum, the gradient of the objective function must be parallel to the normal vector of the constraint set.

The objective function is:

$$E(X)=\sum_{i=1}^{N}F(x_i)$$

The constraint function is:

$$g(X)=\sum_{i=1}^{N}x_i-S=0$$

The constraint set is an $(N-1)$-dimensional hyperplane. The player is only allowed to move resources within this hyperplane.

If the gradient $\nabla E$ still has a nonzero projection onto the constraint hyperplane, then the player can move in that projected direction and increase expected payoff. Therefore, the point cannot be optimal.

At the optimum, we must have:

$$\nabla E=\lambda \nabla g$$

Since:

$$\nabla g=(1,1,\ldots,1)$$

we get:

$$\nabla E=(\lambda,\lambda,\ldots,\lambda)$$

This is exactly the condition:

$$F'(x_1)=F'(x_2)=\cdots=F'(x_N)=\lambda$$

In other words, an optimal allocation requires equal marginal returns across all battlefields. If one battlefield has a higher marginal return, the player should move resources from a lower-return battlefield to that one. As long as such a transfer improves expected payoff, the allocation is not an equilibrium.

---

## 10. Conclusion

The Colonel Blotto Game demonstrates a basic fact about multi-battlefield resource allocation: fixed formations are generally unstable because the opponent can defeat them through local superiority and strategic abandonment.

In the discrete example $S=6,N=3$, every pure allocation can be defeated by another pure allocation, so there is no pure-strategy Nash equilibrium.

In the continuous symmetric version, equilibrium requires mixed strategies. The one-battlefield marginal distribution has the form:

$$\operatorname{Uniform}\left(0,\frac{2S}{N}\right)$$

A full mixed strategy must also satisfy the total resource constraint, so it is not independent random allocation. It is a joint probability distribution on the resource simplex.

Thus, the mathematical significance of the Colonel Blotto Game is that stability under limited resources does not come from a fixed defense, but from a randomized structure that cannot be stably targeted by the opponent.

$$\text{Q.E.D.}$$
