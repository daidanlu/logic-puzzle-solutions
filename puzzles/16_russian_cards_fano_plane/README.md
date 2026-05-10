# The Russian Cards Problem and the Fano Plane Protocol

This README gives a concise combinatorial proof of a secure communication protocol for the Russian Cards Problem using the Fano plane.

---

## 1. Problem Setup

There are seven cards:

$$V=\lbrace 0,1,2,3,4,5,6 \rbrace$$

The cards are dealt to three players:

- Alice receives 3 cards.
- Bob receives 3 cards.
- Eve receives 1 card.

Assume the actual deal is:

$$A=\lbrace 0,1,2 \rbrace$$

$$B=\lbrace 3,4,6 \rbrace$$

$$E=\lbrace 5 \rbrace$$

Alice wants to make a public announcement so that:

1. Bob can determine Alice's exact hand.
2. Eve cannot determine whether any card other than her own belongs to Alice or Bob.

This is a small example of secure communication without computational assumptions. The security comes from a combinatorial structure rather than from encryption based on computational hardness.

---

## 2. The Candidate-Set Announcement

Alice publicly announces that her hand is one of the following seven triples:

$$\mathcal{H}=
\lbrace
\lbrace 0,1,2 \rbrace,
\lbrace 0,3,4 \rbrace,
\lbrace 0,5,6 \rbrace,
\lbrace 1,3,5 \rbrace,
\lbrace 1,4,6 \rbrace,
\lbrace 2,3,6 \rbrace,
\lbrace 2,4,5 \rbrace
\rbrace$$

The actual hand of Alice is:

$$\lbrace 0,1,2 \rbrace$$

The other six triples are decoys.

The seven triples above are the seven lines of the Fano plane. They satisfy two important properties:

1. Any two different triples intersect in exactly one card.
2. Each card appears in exactly three triples.

These two properties are the reason the announcement is simultaneously informative to Bob and safe against Eve.

---

## 3. Why Bob Can Determine Alice's Hand

Bob knows that his hand is:

$$B=\lbrace 3,4,6 \rbrace$$

Since Alice cannot hold any card that Bob already holds, Bob can discard every candidate triple that intersects his own hand.

First, the true candidate has no intersection with Bob's hand:

$$\lbrace 0,1,2 \rbrace \cap \lbrace 3,4,6 \rbrace=\varnothing$$

Every other candidate intersects Bob's hand:

$$\lbrace 0,3,4 \rbrace \cap B=\lbrace 3,4 \rbrace$$

$$\lbrace 0,5,6 \rbrace \cap B=\lbrace 6 \rbrace$$

$$\lbrace 1,3,5 \rbrace \cap B=\lbrace 3 \rbrace$$

$$\lbrace 1,4,6 \rbrace \cap B=\lbrace 4,6 \rbrace$$

$$\lbrace 2,3,6 \rbrace \cap B=\lbrace 3,6 \rbrace$$

$$\lbrace 2,4,5 \rbrace \cap B=\lbrace 4 \rbrace$$

Therefore, the only candidate triple that is disjoint from Bob's hand is:

$$\lbrace 0,1,2 \rbrace$$

Hence Bob can uniquely determine Alice's hand.

---

## 4. Why Eve Cannot Determine Any Other Card

Eve knows that her own card is:

$$E=\lbrace 5 \rbrace$$

Therefore, Eve can discard every candidate triple containing 5:

$$\lbrace 0,5,6 \rbrace$$

$$\lbrace 1,3,5 \rbrace$$

$$\lbrace 2,4,5 \rbrace$$

The remaining possible hands from Eve's perspective are:

$$\mathcal{H}_E=
\lbrace
\lbrace 0,1,2 \rbrace,
\lbrace 0,3,4 \rbrace,
\lbrace 1,4,6 \rbrace,
\lbrace 2,3,6 \rbrace
\rbrace$$

Now consider the six cards that Eve does not hold:

$$0,1,2,3,4,6$$

Each of these cards appears in exactly two of the four remaining candidate triples:

| Card | Remaining candidate triples containing it | Count |
|---|---|---|
| 0 | $\lbrace 0,1,2 \rbrace$, $\lbrace 0,3,4 \rbrace$ | 2 |
| 1 | $\lbrace 0,1,2 \rbrace$, $\lbrace 1,4,6 \rbrace$ | 2 |
| 2 | $\lbrace 0,1,2 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |
| 3 | $\lbrace 0,3,4 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |
| 4 | $\lbrace 0,3,4 \rbrace$, $\lbrace 1,4,6 \rbrace$ | 2 |
| 6 | $\lbrace 1,4,6 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |

Thus, for every card $x \ne 5$, Eve sees two possible worlds in which $x$ belongs to Alice and two possible worlds in which $x$ does not belong to Alice.

Therefore, Eve cannot determine the ownership of any card other than her own.

---

## 5. Abstract Combinatorial Explanation

The key point is that Alice's announcement is not just a random list of seven triples. It is a block design: the Fano plane.

Because any two lines of the Fano plane intersect in exactly one point, every false candidate triple intersects Alice's true triple in exactly one card. Thus each false candidate contains two cards not held by Alice.

Since Eve holds only one card, each false candidate must contain at least one card held by Bob. Therefore, Bob can eliminate all false candidates.

At the same time, because every point lies on exactly three lines, Eve's single card eliminates exactly three candidate triples. The four remaining triples are still balanced: every card not held by Eve occurs in exactly two of them.

This balance prevents Eve from making any certain statement about the ownership of any card other than her own.

---

## 6. Conclusion

The Fano plane protocol solves this instance of the Russian Cards Problem.

Alice publicly announces seven possible hands. Bob uses his three cards to eliminate all false candidates and recover Alice's true hand. Eve uses her one card to eliminate some candidates, but the remaining candidates stay perfectly balanced.

The result is:

$$
\text{Bob has unique information, while Eve has no certain information about any other card.}
$$

This is an example of information-theoretic security obtained from finite geometry and combinatorial design.

$$
\blacksquare
$$
