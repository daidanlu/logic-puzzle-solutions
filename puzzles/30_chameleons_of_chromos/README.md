# The Chameleons of Chromos

This state-machine puzzle relies on an **invariant** and **modular arithmetic**. On the surface, it is a dynamic process in which random collisions change the colors of chameleons. The key question, however, can be reduced to a congruence analysis of the state vector.

---

## 1. System Setup and State Transition Rule

There are 45 chameleons on an island. The initial state is:

$$(R,G,B)=(13,15,17)$$

where:

- $R$ is the number of red chameleons.
- $G$ is the number of green chameleons.
- $B$ is the number of blue chameleons.

The transition rule is as follows.

Whenever two chameleons of **different colors** meet, both of them change into the third color. For example, if one red chameleon and one green chameleon meet, both become blue:

$$(R,G,B)\to(R-1,G-1,B+2)$$

If two chameleons of the same color meet, the state does not change.

The question is whether the system can eventually reach one of the monochromatic states:

$$(45,0,0),\quad(0,45,0),\quad(0,0,45)$$

Here, we discuss **mathematical reachability**: whether there exists a finite sequence of legal collisions that reaches a monochromatic state.

---

## 2. The Modulo 3 Invariant

Let the state at any time be:

$$(R,G,B)$$

Consider the pairwise differences between the numbers of colors:

$$R-G,\quad G-B,\quad B-R$$

For example, suppose a red chameleon and a green chameleon meet. The state changes as follows:

$$(R,G,B)\to(R-1,G-1,B+2)$$

Then the three differences become:

$$(R-1)-(G-1)=R-G$$

$$(G-1)-(B+2)=G-B-3$$

$$(B+2)-(R-1)=B-R+3$$

Thus, in a red-green collision, the three differences respectively stay unchanged, decrease by 3, and increase by 3.

The other two types of mixed-color collisions are symmetric. Therefore, every effective collision either preserves a pairwise difference or changes it by an integer multiple of 3.

Hence, the following quantities are invariant modulo 3:

$$R-G\pmod 3$$

$$G-B\pmod 3$$

$$B-R\pmod 3$$

This is the modulo 3 invariant of the system.

---

## 3. Comparing the Initial State with Monochromatic States

The initial state is:

$$(R,G,B)=(13,15,17)$$

The three differences are:

$$R-G=13-15=-2\equiv1\pmod 3$$

$$G-B=15-17=-2\equiv1\pmod 3$$

$$B-R=17-13=4\equiv1\pmod 3$$

Therefore, the initial state satisfies:

$$R-G\equiv G-B\equiv B-R\equiv1\pmod 3$$

If the system eventually becomes all red, it reaches:

$$(45,0,0)$$

Then:

$$R-G=45\equiv0\pmod 3$$

$$G-B=0\equiv0\pmod 3$$

$$B-R=-45\equiv0\pmod 3$$

The same conclusion holds if the system becomes all green or all blue, since the total number of chameleons is still 45. In any monochromatic state, all three pairwise differences are congruent to 0 modulo 3.

However, in the initial state, all three pairwise differences are congruent to 1 modulo 3. Since legal transitions cannot change these congruence classes, the system cannot move from:

$$(13,15,17)$$

to any of the monochromatic states:

$$(45,0,0),\quad(0,45,0),\quad(0,0,45)$$

---

## 4. Congruence Conditions for a Chosen Monochromatic Target

More generally, suppose the total number of chameleons is $N$, and we want the final state to be all red:

$$(N,0,0)$$

In that target state:

$$G-B=0$$

Since $G-B\pmod 3$ is invariant, the initial state must satisfy:

$$G-B\equiv0\pmod 3$$

Equivalently:

$$G\equiv B\pmod 3$$

Similarly:

- To reach an all-red state, it is necessary that:

$$G\equiv B\pmod 3$$

- To reach an all-green state, it is necessary that:

$$R\equiv B\pmod 3$$

- To reach an all-blue state, it is necessary that:

$$R\equiv G\pmod 3$$

These are necessary conditions derived from the invariant. To prove that a specific state is actually reachable, one must also give a legal collision sequence.

For the original state:

$$(13,15,17)$$

we have:

$$13\equiv1\pmod 3$$

$$15\equiv0\pmod 3$$

$$17\equiv2\pmod 3$$

The three color counts have residues 1, 0, and 2 modulo 3. No two of them are congruent. Therefore, the original state does not satisfy the necessary condition for reaching any monochromatic state.

---

## 5. Reachability After a Small Perturbation

Now modify the initial state slightly by adding one red chameleon.

The state changes from:

$$(13,15,17)$$

to:

$$(14,15,17)$$

The total number becomes 46.

Now:

$$14\equiv2\pmod 3$$

$$15\equiv0\pmod 3$$

$$17\equiv2\pmod 3$$

The numbers of red and blue chameleons are congruent modulo 3:

$$R\equiv B\pmod 3$$

Therefore, this state satisfies the necessary congruence condition for reaching an all-green state. We now give a concrete legal collision sequence, proving that the all-green state is indeed reachable.

---

## 6. Constructing a Path to the All-Green State

The current state is:

$$(14,15,17)$$

The target state is:

$$(0,46,0)$$

That is, all chameleons should eventually become green.

### Step 1: Make One Blue-Green Collision

When a blue chameleon and a green chameleon meet, both become red:

$$(R,G,B)\to(R+2,G-1,B-1)$$

Therefore:

$$(14,15,17)\to(16,14,16)$$

Now the numbers of red and blue chameleons are equal.

### Step 2: Pair Red and Blue Chameleons

When a red chameleon and a blue chameleon meet, both become green:

$$(R,G,B)\to(R-1,G+2,B-1)$$

There are now 16 red chameleons and 16 blue chameleons. Let them meet in pairs 16 times:

$$(16,14,16)\to(0,46,0)$$

The count is:

$$R=16-16=0$$

$$B=16-16=0$$

$$G=14+2\cdot16=46$$

Hence, after a finite sequence of legal collisions, the system reaches the all-green state:

$$(0,46,0)$$

---

## 7. Conclusion

The original state:

$$(13,15,17)$$

cannot evolve into any monochromatic state, because the three color counts are pairwise distinct modulo 3 and therefore fail the necessary invariant condition for every monochromatic target.

After a small perturbation, such as adding one red chameleon, the state becomes:

$$(14,15,17)$$

Now the red and blue counts are congruent modulo 3:

$$R\equiv B\pmod 3$$

A legal collision sequence can then be constructed to reach the all-green state:

$$(0,46,0)$$

This example shows that in some state-machine systems, macroscopic reachability can be determined by the modular structure of the initial state. The key is not to enumerate all possible collision sequences, but to identify the algebraic structure preserved by every transition.

$$\blacksquare$$
