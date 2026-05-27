# The Hardest Logic Puzzle Ever

## Problem Statement

There are three gods, denoted by $A$, $B$, and $C$. Their identities are:

1. **True**: always tells the truth.
2. **False**: always lies.
3. **Random**: before each answer, randomly decides whether to tell the truth or lie.

You do not know which god is $A$, which is $B$, and which is $C$.

All three gods understand your language perfectly, but they answer only with two words:

- `Da`
- `Ja`

One of these words means yes, and the other means no. You do not know which word has which meaning.

You may ask exactly **three** yes-or-no questions. Each question must be addressed to one specified god. You may choose the next question and the next god depending on the previous answer.

The goal is to determine the identities of $A$, $B$, and $C$ after three questions.

---

## Key Lemma

For any proposition $p$, ask a god the following embedded question:

> If I asked you whether $p$ is true, would you answer `Ja`?

For **True** and **False**, regardless of whether `Ja` means yes or no, we have:

$$
p \text{ is true} \iff \text{the answer is Ja}
$$

$$
p \text{ is false} \iff \text{the answer is Da}
$$

This lemma does not apply to **Random**, since Random's answer is determined by a random choice of whether to tell the truth or lie.

---

## Proof of the Lemma

Assume that $p$ is true.

### Case 1: `Ja` means yes and `Da` means no

If the god is **True**, then if asked $p$ directly, he would answer `Ja`. Therefore, if asked whether he would answer `Ja`, the correct answer is yes. Since `Ja` means yes, he answers `Ja`.

If the god is **False**, then if asked $p$ directly, he must lie and would answer `Da`. Therefore, if asked whether he would answer `Ja`, the true answer is no. But False must lie, so he answers yes. Since `Ja` means yes, he also answers `Ja`.

### Case 2: `Ja` means no and `Da` means yes

If the god is **True**, then if asked $p$ directly, he would answer `Da`. Therefore, if asked whether he would answer `Ja`, the correct answer is no. Since `Ja` means no, he answers `Ja`.

If the god is **False**, then if asked $p$ directly, he must lie and would answer `Ja`. Therefore, if asked whether he would answer `Ja`, the true answer is yes. But False must lie, so he answers no. Since `Ja` means no, he answers `Ja`.

Therefore, when $p$ is true, both True and False answer `Ja`.

Similarly, when $p$ is false, both True and False answer `Da`.

Thus the embedded question eliminates two uncertainties at once:

$$
\text{unknown identity of True or False}
\quad + \quad
\text{unknown meaning of Da and Ja}
$$

$$
\blacksquare
$$

---

## Three-Question Strategy

### Question 1: Find a god who is not Random

Ask $B$:

> If I asked you whether $A$ is Random, would you answer `Ja`?

If $B$ is Random, then $A$ and $C$ are not Random. In this case, regardless of $B$'s answer, the selection rule below will choose a god who is not Random.

If $B$ is not Random, the lemma applies:

- If $B$ answers `Ja`, then $A$ is Random, so $C$ is not Random.
- If $B$ answers `Da`, then $A$ is not Random.

Use the following selection rule:

- If $B$ answers `Ja`, choose $C$.
- If $B$ answers `Da`, choose $A$.

Let the selected god be $X$. In all cases, $X$ is not Random.

---

### Question 2: Identify whether X is True or False

Ask $X$:

> If I asked you whether you are True, would you answer `Ja`?

Since $X$ is not Random, the lemma applies.

- If $X$ answers `Ja`, then $X$ is True.
- If $X$ answers `Da`, then $X$ is False.

Now the identity of $X$ is known.

---

### Question 3: Identify Random among the remaining two gods

Among the two gods other than $X$, choose one and call that god $Y$. Call the other one $Z$.

Ask $X$:

> If I asked you whether $Y$ is Random, would you answer `Ja`?

Since $X$ is not Random, the lemma applies again.

- If $X$ answers `Ja`, then $Y$ is Random, and $Z$ is the remaining True or False god.
- If $X$ answers `Da`, then $Y$ is not Random, and $Z$ is Random.

Question 2 has already determined whether $X$ is True or False. Therefore, the remaining non-Random god is also uniquely determined:

- If $X$ is True, then the remaining non-Random god is False.
- If $X$ is False, then the remaining non-Random god is True.

Thus, after three questions, the identities of $A$, $B$, and $C$ are completely determined.

$$
\text{Q.E.D.}
$$
