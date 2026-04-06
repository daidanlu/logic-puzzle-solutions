# The Dining Cryptographers Problem

This directory presents a mathematical derivation of the Dining Cryptographers Problem, showing how anonymous broadcast can be achieved in a decentralized setting.

## 1. System Setup and Variable Definitions

Three cryptographers A, B, and C are seated around a table. The bill has been paid, either by one of them or by an external entity (NSA).

The goal is to determine whether the payer is one of the participants, without revealing their identity if that is the case.

Define the payment state vector:

$$
P = (P_A, P_B, P_C)
$$

If participant \( i \) paid, then:

$$
P_i = 1
$$

Otherwise:

$$
P_i = 0
$$

Since at most one participant pays:

$$
\sum P_i \in \{0, 1\}
$$

During initialization, each pair of adjacent participants shares a fair coin flip privately.

Let:

$$
c_{AB} \in \{0,1\}
$$

$$
c_{BC} \in \{0,1\}
$$

$$
c_{CA} \in \{0,1\}
$$

## 2. Local Encoding and Broadcast

Each participant computes a broadcast value based on the two coins they observe and their own payment state:

$$
M_A = c_{AB} \oplus c_{CA} \oplus P_A
$$

$$
M_B = c_{BC} \oplus c_{AB} \oplus P_B
$$

$$
M_C = c_{CA} \oplus c_{BC} \oplus P_C
$$

Each participant then publicly broadcasts their \( M_i \).

## 3. Correctness

All participants compute:

$$
S = M_A \oplus M_B \oplus M_C
$$

Expanding:

$$
S = (c_{AB} \oplus c_{CA} \oplus P_A)
\oplus (c_{BC} \oplus c_{AB} \oplus P_B)
\oplus (c_{CA} \oplus c_{BC} \oplus P_C)
$$

Rearranging:

$$
S = (c_{AB} \oplus c_{AB})
\oplus (c_{BC} \oplus c_{BC})
\oplus (c_{CA} \oplus c_{CA})
\oplus (P_A \oplus P_B \oplus P_C)
$$

Since:

$$
x \oplus x = 0
$$

we obtain:

$$
S = P_A \oplus P_B \oplus P_C
$$

Thus:

- If the NSA paid:

$$
P_A = P_B = P_C = 0
$$

$$
S = 0
$$

- If one participant paid:

$$
\exists i: P_i = 1
$$

$$
S = 1
$$

The protocol determines whether the payment was internal.

## 4. Anonymity

Consider participant C, with:

$$
P_C = 0,\quad S = 1
$$

The information available to C is:

$$
\{c_{CA}, c_{BC}, M_A, M_B, M_C\}
$$

The unknown variable is:

$$
c_{AB}
$$

### Case 1: A paid

$$
P_A = 1,\quad P_B = 0
$$

$$
M_A = c_{AB} \oplus c_{CA} \oplus 1
$$

$$
M_B = c_{AB} \oplus c_{BC}
$$

### Case 2: B paid

$$
P_A = 0,\quad P_B = 1
$$

$$
M_A = c_{AB} \oplus c_{CA}
$$

$$
M_B = c_{AB} \oplus c_{BC} \oplus 1
$$

Since:

$$
P(c_{AB} = 0) = P(c_{AB} = 1) = 0.5
$$

For any observed values:

$$
(M_A, M_B) = (x, y)
$$

the two cases correspond to opposite values of $c_{AB}$, but with equal probability. Therefore:

$$
P(M_A, M_B \mid P_A = 1) = P(M_A, M_B \mid P_B = 1)
$$

The observer cannot distinguish between the two cases.

The protocol achieves perfect secrecy.

Q.E.D.