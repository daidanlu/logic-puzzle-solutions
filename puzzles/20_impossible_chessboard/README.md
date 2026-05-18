# The Impossible Chessboard Puzzle

## Puzzle Statement

There is a standard $8 \times 8$ chessboard with $64$ squares, numbered $0,1,2,\ldots,63$.

Each square contains one coin, and each coin has an arbitrary state:

$$\text{heads}=1, \quad \text{tails}=0$$

The warden hides a key under one square. Let the key position be $K$.
Alice can see both the key position and the initial coin configuration. Bob can only see the board after Alice has acted.

Alice and Bob may agree on a protocol beforehand. Once the game starts, Alice must flip exactly one coin. Then Bob enters the room and must identify the key position from the final board state alone.

The goal is to design a protocol that always lets Bob identify $K$ correctly.

---

## Mathematical Model

Treat each square number as a $6$-bit binary vector.
Since:

$$64=2^6$$

Each square number can be viewed as an element of the vector space $\mathbb{F}_2^6$.

For any board state, define its XOR checksum as the XOR of all square numbers whose coins are heads:

$$P=\bigoplus_{i:\,c_i=1} i$$

where $c_i$ is the state of the coin on square $i$.

Bob's decoding rule is: compute the current checksum $P$, and output $P$ as the key position.

---

## Key Observation

Flipping the coin on square $F$ changes the checksum by XORing it with $F$, regardless of whether the coin was originally heads or tails.

Therefore, if the checksum before the flip is $P_{current}$, then after flipping square $F$ the new checksum is:

$$P_{new}=P_{current}\oplus F$$

This holds because in $\mathbb{F}_2$, every element is its own additive inverse:

$$F\oplus F=0$$

Thus adding $F$ and removing $F$ are the same operation under XOR.

---

## Protocol

Alice first computes the current checksum of the board:

$$P_{current}=\bigoplus_{i:\,c_i=1} i$$

She wants Bob's final checksum to equal the key position $K$.
So Alice must choose a square $F$ such that:

$$P_{current}\oplus F=K$$

By the self-inverse property of XOR:

$$F=P_{current}\oplus K$$

Alice flips the coin on square $F$.
Bob enters, computes the checksum of the final board, and outputs that checksum.

---

## Correctness Proof

After Alice flips square $F$, Bob sees a board whose checksum is:

$$P_{new}=P_{current}\oplus F$$

By the protocol, Alice chooses:

$$F=P_{current}\oplus K$$

Substituting this into the checksum gives:

$$P_{new}=P_{current}\oplus (P_{current}\oplus K)$$

Using associativity and $P_{current}\oplus P_{current}=0$, we obtain:

$$P_{new}=(P_{current}\oplus P_{current})\oplus K$$

Therefore:

$$P_{new}=0\oplus K=K$$

Hence Bob's output is always exactly the key position $K$.

$$\blacksquare$$

---

## Edge Case

If the initial checksum already equals the key position, then:

$$P_{current}=K$$

Alice's formula gives:

$$F=P_{current}\oplus K=0$$

Alice flips the coin on square $0$.
Since square $0$ has binary label $000000$, flipping it does not change the XOR checksum:

$$P_{new}=P_{current}\oplus 0=P_{current}=K$$

Thus the protocol still works even though Alice is required to flip exactly one coin.

---

## Why This Works

Alice is not writing information into the face value of a single coin. Instead, she uses the position of the flipped coin to control the global checksum of the whole board.

The $64$ possible flip positions provide exactly $6$ bits of information:

$$\log_2 64=6$$

The key position also requires exactly $6$ bits to specify.

The core idea is that every board state has a global XOR fingerprint in $\mathbb{F}_2^6$. By flipping one carefully chosen position, Alice routes this fingerprint to any desired target square.

---

## Conclusion

This protocol shows that restricted communication does not necessarily mean local information transfer only.
With the right algebraic structure, one local action can control a global invariant.

The key formula is:

$$F=P_{current}\oplus K$$

It connects the random board state, the hidden key position, and Alice's single allowed flip into a perfectly reliable encoding protocol.
