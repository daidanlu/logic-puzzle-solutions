# Ulam's Game with One Lie: Robust Search Under Adversarial Noise

## Problem Statement

An oracle secretly chooses one integer from the range:

$$
1,2,\dots,1{,}000{,}000
$$

The questioner may ask only yes-or-no questions.

If the oracle always tells the truth, this is just ordinary binary search. Since:

$$
2^{20}=1{,}048{,}576>1{,}000{,}000
$$

only:

$$
\lceil \log_2 1{,}000{,}000 \rceil=20
$$

questions are needed.

However, the oracle is now allowed to lie at most once during the entire game. The lie may occur at any question, or the oracle may choose not to lie at all. The questioner does not know whether a lie has occurred, nor where it occurred.

The question is: how many yes-or-no questions are necessary and sufficient to guarantee finding the hidden number?

The answer is:

$$
\boxed{25}
$$

---

## Information-Theoretic Lower Bound

Suppose we ask $q$ questions in total.

For each fixed number, if there are no lies, it corresponds to one ideal yes-or-no answer string of length $q$.

But since the oracle may lie at most once, each fixed number can produce the following possible answer strings:

1. no lie occurs;
2. the first answer is a lie;
3. the second answer is a lie;
4. and so on;
5. the $q$-th answer is a lie.

Therefore, each number has:

$$
q+1
$$

possible answer patterns.

Since there are $1{,}000{,}000$ possible hidden numbers, the system must distinguish at least:

$$
1{,}000{,}000(q+1)
$$

possible states.

On the other hand, $q$ yes-or-no questions can produce at most:

$$
2^q
$$

different answer strings.

Thus we must have:

$$
2^q \ge 1{,}000{,}000(q+1)
$$

Now test $q=24$:

$$
2^{24}=16{,}777{,}216
$$

but:

$$
1{,}000{,}000(24+1)=25{,}000{,}000
$$

So $24$ questions are not enough.

Now test $q=25$:

$$
2^{25}=33{,}554{,}432
$$

and:

$$
1{,}000{,}000(25+1)=26{,}000{,}000
$$

Hence:

$$
2^{25}>26{,}000{,}000
$$

So $25$ is the first number of questions for which the information capacity is large enough.

Therefore, the lower bound is:

$$
\boxed{25}
$$

---

## State Model

We now explain why $25$ questions are actually sufficient.

The problem with ordinary binary search is that a single lie at a critical step may permanently discard the true answer.

Therefore, we cannot immediately eliminate every number that disagrees with the current answers. Instead, we track how many times each number conflicts with the answers received so far.

At any point in the game, every number belongs to one of three states.

### White List

A white-list number is fully consistent with all answers so far.

If it is the true answer, then the oracle has not lied about it yet.

### Gray List

A gray-list number conflicts with exactly one answer so far.

If it is the true answer, then the oracle's single allowed lie has already been used.

### Black List

A black-list number conflicts with at least two answers so far.

Since the oracle is allowed to lie at most once, a black-list number cannot be the true answer and can be eliminated.

---

## Berlekamp Weight

Suppose there are $k$ questions remaining.

We assign weights to numbers according to their current states.

A black-list number has already been eliminated, so its weight is:

$$
0
$$

A gray-list number has already used its one allowed conflict. To remain possible, all of the next $k$ answers must be consistent with it. Hence each gray-list number has weight:

$$
1
$$

A white-list number has no conflicts yet. If it is the true answer, then among the next $k$ questions, the oracle may either never lie or lie at exactly one of those future questions.

Therefore, each white-list number has:

$$
k+1
$$

possible survival patterns.

So each white-list number has weight:

$$
k+1
$$

The total system weight is defined as:

$$
W=(k+1)\cdot |\text{White}|+|\text{Gray}|
$$

---

## Initial Weight

At the beginning, there are $25$ questions remaining.

All $1{,}000{,}000$ numbers are in the white list, and there are no gray-list numbers.

Thus the initial weight is:

$$
W=26\cdot 1{,}000{,}000=26{,}000{,}000
$$

The information capacity of $25$ yes-or-no questions is:

$$
2^{25}=33{,}554{,}432
$$

Therefore:

$$
26{,}000{,}000<2^{25}
$$

So the initial state fits within the information capacity of $25$ binary questions.

---

## The Question Strategy

At each step, we do not split the number of candidates. We split the total weight.

That is, we choose a set $A$ and ask:

$$
\text{Is the hidden number in } A\text{?}
$$

If the oracle answers yes:

- white-list numbers inside $A$ remain white;
- white-list numbers outside $A$ become gray;
- gray-list numbers inside $A$ remain gray;
- gray-list numbers outside $A$ become black and are eliminated.

If the oracle answers no, the transition is symmetric:

- white-list numbers outside $A$ remain white;
- white-list numbers inside $A$ become gray;
- gray-list numbers outside $A$ remain gray;
- gray-list numbers inside $A$ become black and are eliminated.

Thus each question creates two possible successor states:

1. the state after a yes answer;
2. the state after a no answer.

The goal is to choose $A$ so that the two successor weights are as close as possible.

In other words, each question tries to achieve:

$$
\text{yes-branch weight} \approx \text{no-branch weight}
$$

This makes the remaining weighted state space shrink by about one half, regardless of how the oracle answers.

---

## Why the Strategy Converges

The initial weight is:

$$
26{,}000{,}000
$$

The total capacity of $25$ questions is:

$$
2^{25}=33{,}554{,}432
$$

Since the initial weight is strictly below $2^{25}$, and since each question is chosen to split weight as evenly as possible, we can maintain the invariant:

$$
W \le 2^k
$$

where $k$ is the number of questions remaining.

Intuitively, whenever $k$ questions remain, the weighted state space is no larger than the capacity of those $k$ binary questions.

After $25$ questions, there are $0$ questions remaining.

Thus:

$$
W \le 2^0=1
$$

At that point, each surviving white-list number has weight $1$, and each surviving gray-list number also has weight $1$.

Therefore, $W\le 1$ means that at most one possible number remains.

On the other hand, the true answer can never be eliminated, because it can conflict with the received answers at most once.

So exactly one number remains.

That number is the hidden number chosen by the oracle.

---

## Conclusion

To find a number from $1$ to $1{,}000{,}000$ when the oracle may lie at most once, the minimum number of yes-or-no questions is:

$$
\boxed{25}
$$

The key idea is not ordinary binary search, but robust search with one-error correction.

Ordinary binary search splits the number of candidates. One-lie search splits the weighted state space.

The key weight function is:

$$
W=(k+1)\cdot |\text{White}|+|\text{Gray}|
$$

Here, the white list contains numbers with $0$ conflicts, and the gray list contains numbers with $1$ conflict that may still be the true answer.

By choosing each question to approximately split this weight, the state space contracts reliably. After $25$ questions, only one possible answer remains.

$$
\text{Q.E.D.}
$$
