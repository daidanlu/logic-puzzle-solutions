# Braess's Paradox: Inefficient Nash Equilibrium in Selfish Routing

## Problem Statement

Braess's paradox shows that in a selfish routing network, adding a seemingly beneficial new edge can make every participant worse off at Nash equilibrium.

Consider a directed traffic network with one source node $S$, one destination node $D$, and two intermediate nodes $A$ and $B$. A total of $4000$ drivers want to travel from $S$ to $D$.

Initially, the network contains four directed edges:

$$S \to A$$

$$A \to D$$

$$S \to B$$

$$B \to D$$

The travel times on these edges are defined as follows, where $x$ denotes the number of drivers using the edge:

$$T_{SA}(x)=\frac{x}{100}$$

$$T_{AD}(x)=45$$

$$T_{SB}(x)=45$$

$$T_{BD}(x)=\frac{x}{100}$$

Thus, before any new edge is added, drivers have two available routes:

$$P_1:S \to A \to D$$

$$P_2:S \to B \to D$$

Now suppose a new directed edge is added from $A$ to $B$:

$$A \to B$$

The travel time on this new edge is:

$$T_{AB}(x)=0$$

After this edge is added, drivers may also choose the third route:

$$P_3:S \to A \to B \to D$$

Each driver is selfish and rational. They only care about minimizing their own travel time, assuming the route choices of all other drivers are fixed.

The question is:

$$\text{After adding the zero-cost edge } A \to B\text{, what happens at Nash equilibrium?}$$

---

## Nash Equilibrium Before Adding the New Edge

Before the edge $A \to B$ is added, there are only two available routes:

$$P_1:S \to A \to D$$

$$P_2:S \to B \to D$$

Suppose $x$ drivers choose $P_1$. Then $4000-x$ drivers choose $P_2$.

The travel time on $P_1$ is:

$$C_1(x)=\frac{x}{100}+45$$

The travel time on $P_2$ is:

$$C_2(x)=45+\frac{4000-x}{100}$$

At Nash equilibrium, if both routes are used, they must have equal travel time. Otherwise, drivers on the slower route would switch to the faster route.

Therefore:

$$\frac{x}{100}+45=45+\frac{4000-x}{100}$$

Canceling $45$ from both sides gives:

$$\frac{x}{100}=\frac{4000-x}{100}$$

Thus:

$$x=4000-x$$

Hence:

$$x=2000$$

Therefore, before adding the new edge, the equilibrium routing is:

$$2000 \text{ drivers choose } P_1$$

$$2000 \text{ drivers choose } P_2$$

The travel time on each route is:

$$\frac{2000}{100}+45=20+45=65$$

So the Nash equilibrium travel time before adding the new edge is:

$$65 \text{ minutes}$$

---

## Available Routes After Adding the Zero-Cost Edge

After the edge $A \to B$ is added, the drivers have three natural routes:

$$P_1:S \to A \to D$$

$$P_2:S \to B \to D$$

$$P_3:S \to A \to B \to D$$

We now show that $P_3$ strictly dominates the other two routes.

Let $x$ be the number of drivers using the edge $S \to A$, and let $y$ be the number of drivers using the edge $B \to D$.

Since there are only $4000$ drivers in total, we always have:

$$x \le 4000$$

$$y \le 4000$$

Therefore:

$$\frac{x}{100}\le 40$$

$$\frac{y}{100}\le 40$$

The travel time on $P_3$ is:

$$C_3=\frac{x}{100}+0+\frac{y}{100}$$

First compare $P_3$ with $P_1$.

Both routes use the edge $S \to A$. The difference is that $P_1$ then uses $A \to D$, whose cost is $45$, while $P_3$ then uses $A \to B \to D$, whose remaining cost is:

$$0+\frac{y}{100}\le 40$$

Thus:

$$0+\frac{y}{100}<45$$

So:

$$C_3<C_1$$

Therefore, $P_3$ is strictly better than $P_1$.

Now compare $P_3$ with $P_2$.

Both routes eventually use the edge $B \to D$. The difference is that $P_2$ first uses $S \to B$, whose cost is $45$, while $P_3$ first uses $S \to A \to B$, whose cost is:

$$\frac{x}{100}+0\le 40$$

Thus:

$$\frac{x}{100}+0<45$$

So:

$$C_3<C_2$$

Therefore, $P_3$ is also strictly better than $P_2$.

Hence, for every driver, regardless of how the other drivers choose their routes, the route

$$P_3:S \to A \to B \to D$$

strictly dominates the other two routes.

---

## Nash Equilibrium After Adding the New Edge

Since $P_3$ is a strictly dominant route, every selfish driver chooses:

$$S \to A \to B \to D$$

Therefore, all $4000$ drivers use the edges $S \to A$ and $B \to D$.

The travel time on $S \to A$ becomes:

$$T_{SA}(4000)=\frac{4000}{100}=40$$

The travel time on $A \to B$ is:

$$T_{AB}(4000)=0$$

The travel time on $B \to D$ becomes:

$$T_{BD}(4000)=\frac{4000}{100}=40$$

Thus, each driver's total travel time is:

$$40+0+40=80$$

So the Nash equilibrium travel time after adding the zero-cost edge is:

$$80 \text{ minutes}$$

---

## Verification of Nash Equilibrium

We now verify that the state in which all drivers choose $P_3$ is indeed a Nash equilibrium.

In this state, suppose one driver unilaterally switches to:

$$S \to A \to D$$

That driver still uses the congested edge $S \to A$, whose cost is approximately $40$, and then uses $A \to D$, whose cost is $45$. The total cost is approximately:

$$40+45=85$$

If the driver unilaterally switches to:

$$S \to B \to D$$

then the driver first uses $S \to B$, whose cost is $45$, and then uses the congested edge $B \to D$, whose cost is approximately $40$. The total cost is approximately:

$$45+40=85$$

Both unilateral deviations are worse than staying on $P_3$, whose cost is $80$.

Therefore, no driver can reduce their own travel time by unilaterally changing routes.

Hence, the routing in which every driver chooses

$$S \to A \to B \to D$$

is a Nash equilibrium.

---

## Conclusion

Before the new edge is added, the Nash equilibrium splits the traffic evenly:

$$2000 \text{ drivers use } S \to A \to D$$

$$2000 \text{ drivers use } S \to B \to D$$

Each driver has travel time:

$$65 \text{ minutes}$$

After the zero-cost edge is added, the incentive structure changes. Every driver finds that

$$S \to A \to B \to D$$

is a strictly dominant route.

As a result, all drivers choose this route, and each driver's travel time becomes:

$$80 \text{ minutes}$$

Therefore:

$$65<80$$

This is Braess's paradox.

It shows that in a non-cooperative selfish routing network, adding a new edge or increasing local connectivity does not necessarily improve equilibrium performance. The new edge is not physically harmful by itself. Rather, it changes the incentive structure of the game, causing locally rational choices to aggregate into a globally inefficient Nash equilibrium.

$$\text{Q.E.D.}$$
