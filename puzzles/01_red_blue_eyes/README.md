Original problem reference: [https://terrytao.wordpress.com/2008/02/05/the-blue-eyed-islanders-puzzle/](https://terrytao.wordpress.com/2008/02/05/the-blue-eyed-islanders-puzzle/)

This directory contains the mathematical proof and Python simulation verification for the Blue-Eyed Islanders puzzle proposed by Professor Terence Tao.

### Generalized Version of the Original Problem:
Assume there are *N* people on an island, and each person's eyes are either blue or brown.
- The islanders can see the eye colors of everyone else, but cannot see their own eye color.
- The islanders do not know the exact number of brown-eyed and blue-eyed people (this is a crucial premise often ignored in modified versions of the puzzle).
- The islanders are strictly forbidden from communicating about eye color with each other.
- All islanders are perfectly rational beings.
- Any islander who figures out their own eye color must publicly commit suicide in the town square at noon the following day.

**Triggering Event:** A blue-eyed foreigner visits the island and announces to all the islanders: "At least one of you has blue eyes like me."

---

The key to the puzzle lies in proving the following proposition:
**If there are actually *k* blue-eyed people on the island (*k* >= 1), then all *k* of them will inevitably commit suicide at noon on the *k*-th day after the foreigner's announcement.**

We will prove this using mathematical induction on the number of blue-eyed people, *k*.

#### Base Case: *k* = 1
There is exactly one blue-eyed islander. This blue-eyed person sees that everyone else has brown eyes, and thus immediately knows that they are the one with blue eyes.
Therefore, when *k* = 1, this single blue-eyed person will commit suicide at noon on the 1st day after the announcement.

#### Inductive Hypothesis:
Assume the proposition holds true when there are *m* (*m* >= 1) blue-eyed people on the island. We must now prove that when there are *m*+1 blue-eyed people, all *m*+1 of them will inevitably commit suicide at noon on the (*m*+1)-th day after the announcement.

#### Inductive Step:
When there are *m*+1 blue-eyed people, from the perspective of any one of these *m*+1 individuals, they can see exactly *m* blue eyes.
Because they cannot know the exact total number of blue eyes, they form the following two hypotheses:
1. There are exactly *m* blue-eyed people in total, and their own eyes are brown.
2. There are exactly *m*+1 blue-eyed people in total, and they are one of them.

Because they are perfectly rational, they will wait until the *m*-th day after the announcement to verify which hypothesis is true before deciding whether to commit suicide.
1. If Hypothesis 1 is true (i.e., they have brown eyes), then after *m* days, this brown-eyed person will observe that the *m* blue-eyed people they see have all committed suicide. This perfectly aligns with our Inductive Hypothesis, which we assume to be true in mathematical induction.
2. If Hypothesis 2 is true (i.e., they have blue eyes), then after *m* days, this blue-eyed person will observe that the *m* blue-eyed people they see did *not* commit suicide. This happens because all other blue-eyed people adopted the exact same strategy of waiting until this day to test their own hypotheses, resulting in a mutual waiting state. In this scenario, the observer deduces that Hypothesis 2 is correct, meaning they themselves have blue eyes. Consequently, they will go to the square and commit suicide at noon on the (*m*+1)-th day after the announcement.

Therefore, when *k* = *m*+1, all *m*+1 blue-eyed people will inevitably commit suicide at noon on the (*m*+1)-th day after the announcement.

In conclusion, by mathematical induction, the theorem holds true for any *k* >= 1. Q.E.D.