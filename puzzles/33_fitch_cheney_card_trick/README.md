# Fitch Cheney's Five-Card Trick

## Problem Setting

There are two cooperating agents, the assistant Alice and the magician Bob, together with a standard deck of 52 playing cards.

Before the trick begins, Alice and Bob may agree on a deterministic protocol.

The rules are as follows:

1. A spectator chooses any **5** cards from the 52-card deck and gives them only to Alice.
2. Alice must choose **1** of these 5 cards to hide. This card is the target card.
3. Alice places the remaining **4** cards face up on the table in a specific order.
4. Alice leaves the room and cannot communicate with Bob by speech, eye contact, timing, physical marks, or any other side channel.
5. Bob enters the room and must determine the hidden fifth card using only the identities and order of the 4 visible cards.

The goal is to design a deterministic protocol that always allows Bob to identify the hidden card correctly.

---

## The Apparent Information-Theoretic Difficulty

From Bob's point of view, 4 cards are visible on the table. Excluding these 4 cards, there are:

$$52-4=48$$

unknown cards remaining. The hidden card must be one of these 48 cards.

If Alice could communicate only through the order of the 4 visible cards, then the number of possible orders would be:

$$4!=24$$

Thus, the order of 4 cards alone cannot encode 48 possibilities, since:

$$24<48$$

This shows that if the hidden card were fixed in advance, the ordering of the 4 visible cards would not contain enough information for lossless encoding.

The key point is that the hidden card is not chosen by the spectator. Alice is allowed to choose which card to hide. This choice changes the search space that Bob must consider.

---

## Protocol Design

The protocol has three steps.

---

## Step 1: The Suit Pigeonhole Principle

The spectator gives Alice 5 cards, while a standard deck has only 4 suits.

By the pigeonhole principle, among the 5 cards, at least 2 cards must have the same suit.

Alice chooses a pair of cards with the same suit. If there are several such pairs, Alice and Bob use a pre-agreed total ordering rule to choose one pair, so that the protocol remains deterministic.

Then:

- one of these two cards is used as the **anchor card** and placed first on the table;
- the other card is used as the **hidden card**.

When Bob sees the first card, he immediately knows that the hidden card has the same suit as the first card.

Therefore, the hidden card is no longer one of 48 possible cards. It is restricted to the other 12 ranks of the same suit, since the anchor card itself is already visible.

---

## Step 2: Modulo 13 Cycle and Distance Compression

Treat the 13 ranks of a fixed suit as a cycle modulo 13:

$$A,2,3,\ldots,Q,K$$

For example, we may use the convention:

$$A=1,\ 2=2,\ \ldots,\ Q=12,\ K=13$$

For two cards of the same suit, let their ranks be $a$ and $b$. On the modulo 13 cycle, there is a positive clockwise distance from $a$ to $b$, and another positive clockwise distance from $b$ to $a$. These two distances sum to 13.

Since 13 is odd, exactly one of these two positive distances must lie in:

$$\lbrace 1,2,3,4,5,6 \rbrace$$

Therefore, Alice can always choose a direction such that the clockwise distance $d$ from the anchor card to the hidden card satisfies:

$$1\le d\le 6$$

The rule is:

- if the clockwise distance $d$ from card $a$ to card $b$ satisfies $1\le d\le 6$, Alice shows $a$ and hides $b$;
- otherwise, Alice shows $b$ and hides $a$.

After Bob sees the anchor card, he only needs to know one number:

$$d\in\lbrace 1,2,3,4,5,6 \rbrace$$

The rank of the hidden card is then obtained by adding $d$ to the rank of the anchor card modulo 13.

For example, suppose the two same-suit cards have ranks 3 and 10.

- The clockwise distance from 3 to 10 is $+7$.
- The clockwise distance from 10 to 3 is $+6$.

Therefore, Alice shows 10 as the anchor card, hides 3, and uses the remaining three cards to encode the number 6.

---

## Step 3: Encoding 1 Through 6 with the Last Three Cards

Alice still has 3 visible cards to place after the anchor card. She uses the order of these 3 cards to encode the number $d$.

Alice and Bob pre-agree on a total ordering of all cards. For example:

1. first compare ranks;
2. if the ranks are equal, compare suits, for instance by using:

$$\text{spades}>\text{hearts}>\text{clubs}>\text{diamonds}$$

Let the remaining three cards be ordered from smallest to largest as:

$$S<M<L$$

These three cards have:

$$3!=6$$

possible orders, exactly enough to encode the numbers 1 through 6. Use the following dictionary:

$$S,M,L\to +1$$

$$S,L,M\to +2$$

$$M,S,L\to +3$$

$$M,L,S\to +4$$

$$L,S,M\to +5$$

$$L,M,S\to +6$$

Thus, the order of the last three visible cards uniquely determines the offset $d$.

---

## Complete Example

Suppose the spectator gives Alice the following 5 cards:

**4 of spades, 9 of spades, Jack of hearts, 2 of clubs, 7 of diamonds.**

---

## Alice's Encoding Process

Alice finds a same-suit pair: 4 of spades and 9 of spades.

She computes their distances on the spade rank cycle:

$$4\to 9=+5$$

$$9\to 4=+8$$

Since $5\le 6$, Alice shows the 4 of spades and hides the 9 of spades.

The offset is:

$$d=5$$

The three remaining cards are:

**Jack of hearts, 2 of clubs, 7 of diamonds.**

Using the pre-agreed total order, they are sorted as:

$$\text{2 of clubs}=S,\quad \text{7 of diamonds}=M,\quad \text{Jack of hearts}=L$$

The number 5 corresponds to the order:

$$L,S,M$$

Therefore, Alice places the last three cards as:

**Jack of hearts, 2 of clubs, 7 of diamonds.**

The final visible sequence is:

**4 of spades, Jack of hearts, 2 of clubs, 7 of diamonds.**

---

## Bob's Decoding Process

Bob enters the room and sees:

**4 of spades, Jack of hearts, 2 of clubs, 7 of diamonds.**

The first card is the 4 of spades, so Bob knows that the hidden card is also a spade.

Bob sorts the last three cards as:

$$\text{2 of clubs}=S,\quad \text{7 of diamonds}=M,\quad \text{Jack of hearts}=L$$

Their actual order is:

$$L,S,M$$

By the agreed dictionary:

$$L,S,M\to +5$$

Therefore:

$$d=5$$

Starting from the 4 of spades and moving 5 steps clockwise gives:

$$4+5=9$$

Therefore, Bob concludes that the hidden card is:

**9 of spades.**

---

## Correctness Proof

The correctness of the protocol relies on three facts.

### 1. The pigeonhole principle guarantees a same-suit pair

Since 5 cards are distributed among 4 suits, at least two cards must have the same suit.

Therefore, Alice can always choose a same-suit pair and use the first displayed card to tell Bob the suit of the hidden card.

### 2. The modulo 13 cycle compresses the rank difference to 1 through 6

For any two cards of the same suit, the two clockwise distances between their ranks sum to 13.

Therefore, one of these two distances must lie in:

$$\lbrace 1,2,3,4,5,6 \rbrace$$

Alice shows the card used as the starting point and hides the card used as the endpoint. Bob then only needs to recover an offset $d$, where:

$$d\in\lbrace 1,2,3,4,5,6 \rbrace$$

### 3. The last three cards encode exactly six cases

The remaining three visible cards have:

$$3!=6$$

possible orders, which can uniquely encode the offset $d$.

Bob recovers $d$ from the order of the last three cards, then moves $d$ steps clockwise from the anchor card to determine the hidden card uniquely.

---

## Conclusion

Alice can use:

- the first visible card to transmit the suit and anchor rank of the hidden card;
- the order of the last three visible cards to transmit the offset.

Therefore, Bob can uniquely determine the hidden card.

The protocol is deterministic and requires no additional communication.

$$\text{Q.E.D.}$$
