# The Twelve-Coin Counterfeit Problem and Ternary Weighing Codes

This README gives a concise mathematical proof of the classic twelve-coin counterfeit problem. The proof uses three balance-scale weighings as a ternary code that identifies both the counterfeit coin and whether it is heavier or lighter.

---

## 1. Problem Setup

There are 12 visually identical coins:

$$C=\lbrace 1,2,3,4,5,6,7,8,9,10,11,12 \rbrace$$

Exactly one coin is counterfeit. The counterfeit coin may be heavier than a genuine coin, or it may be lighter.

We have a balance scale. Each weighing has exactly three possible outcomes:

$$\text{left pan heavier},\quad \text{balanced},\quad \text{right pan heavier}$$

The goal is to determine, in at most 3 weighings:

1. which coin is counterfeit;
2. whether the counterfeit coin is heavier or lighter.

---

## 2. Information-Theoretic Lower Bound

If only 2 weighings are allowed, then there are at most:

$$3^2=9$$

possible outcome sequences.

However, there are 12 possible choices for the counterfeit coin, and each one can be either heavier or lighter. Therefore, the number of possible states is:

$$12\cdot 2=24$$

Since:

$$9<24$$

2 weighings cannot solve the problem. At least 3 weighings are necessary.

With 3 weighings, the number of possible outcome sequences is:

$$3^3=27$$

Thus, from an information-theoretic point of view, 3 weighings may be sufficient.

---

## 3. Encoding Weighings as Ternary Vectors

Represent the position of each coin across the three weighings by a vector of length 3.

For coin $i$, define its column vector as:

$$v_i=(a_{1i},a_{2i},a_{3i})$$

where:

$$a_{ji}=+1\quad \text{means coin } i \text{ is placed on the left pan in weighing } j$$

$$a_{ji}=-1\quad \text{means coin } i \text{ is placed on the right pan in weighing } j$$

$$a_{ji}=0\quad \text{means coin } i \text{ is not used in weighing } j$$

The outcome of the three weighings is also represented by a vector:

$$r=(r_1,r_2,r_3)$$

where:

$$r_j=+1\quad \text{means the left pan is heavier in weighing } j$$

$$r_j=-1\quad \text{means the right pan is heavier in weighing } j$$

$$r_j=0\quad \text{means weighing } j \text{ is balanced}$$

---

## 4. A Three-Weighing Construction

Use the following weighing matrix. Each column corresponds to a coin, and each row corresponds to a weighing.

| Coin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $W_1$ | -1 | -1 | -1 | +1 | +1 | +1 | -1 | +1 | 0 | 0 | 0 | 0 |
| $W_2$ | -1 | -1 | 0 | 0 | 0 | -1 | +1 | -1 | +1 | +1 | +1 | 0 |
| $W_3$ | 0 | +1 | -1 | 0 | -1 | +1 | 0 | -1 | +1 | 0 | -1 | +1 |

Equivalently, the three weighings are:

$$W_1:\quad \lbrace 4,5,6,8 \rbrace \text{ vs } \lbrace 1,2,3,7 \rbrace$$

$$W_2:\quad \lbrace 7,9,10,11 \rbrace \text{ vs } \lbrace 1,2,6,8 \rbrace$$

$$W_3:\quad \lbrace 2,6,9,12 \rbrace \text{ vs } \lbrace 3,5,8,11 \rbrace$$

Each weighing places 4 coins on the left pan and 4 coins on the right pan. Therefore, if all participating coins were genuine, the scale would balance.

---

## 5. Decoding Rule

The matrix gives the following 12 column vectors:

$$v_1=(-1,-1,0)$$

$$v_2=(-1,-1,+1)$$

$$v_3=(-1,0,-1)$$

$$v_4=(+1,0,0)$$

$$v_5=(+1,0,-1)$$

$$v_6=(+1,-1,+1)$$

$$v_7=(-1,+1,0)$$

$$v_8=(+1,-1,-1)$$

$$v_9=(0,+1,+1)$$

$$v_{10}=(0,+1,0)$$

$$v_{11}=(0,+1,-1)$$

$$v_{12}=(0,0,+1)$$

After observing the three weighings, let $r$ be the outcome vector.

The decoding rule is:

$$r=v_i\quad \Longrightarrow \quad \text{coin } i \text{ is counterfeit and heavier}$$

$$r=-v_i\quad \Longrightarrow \quad \text{coin } i \text{ is counterfeit and lighter}$$

The meaning is simple: the column vector $v_i$ is the outcome pattern that would be produced if coin $i$ were heavier. The opposite vector $-v_i$ is the outcome pattern that would be produced if coin $i$ were lighter.

---

## 6. Correctness Proof

We prove that the decoding rule is correct.

Suppose coin $i$ is the counterfeit coin. All other coins are genuine. Since each weighing places the same number of coins on both pans, the genuine coins cancel out in total weight. Therefore, the imbalance in any weighing is caused only by the position of coin $i$.

### 6.1 The Counterfeit Coin Is Heavier

If coin $i$ is heavier, then:

- if it is on the left pan, the left pan becomes heavier;
- if it is on the right pan, the right pan becomes heavier;
- if it is not used, it has no effect on that weighing.

Thus the outcome of weighing $j$ is exactly $a_{ji}$.

Therefore, the full outcome vector is:

$$r=(a_{1i},a_{2i},a_{3i})=v_i$$

Hence:

$$\text{coin } i \text{ is heavier}\quad \Longrightarrow \quad r=v_i$$

### 6.2 The Counterfeit Coin Is Lighter

If coin $i$ is lighter, then the effect is reversed:

- if it is on the left pan, the left pan becomes lighter, so the right pan is heavier;
- if it is on the right pan, the right pan becomes lighter, so the left pan is heavier;
- if it is not used, it has no effect on that weighing.

Thus the outcome of weighing $j$ is $-a_{ji}$.

Therefore, the full outcome vector is:

$$r=(-a_{1i},-a_{2i},-a_{3i})=-v_i$$

Hence:

$$\text{coin } i \text{ is lighter}\quad \Longrightarrow \quad r=-v_i$$

This proves that the observed outcome must be either a column vector or the opposite of a column vector.

---

## 7. Why the Decoding Is Unique

For unique decoding, two conditions are required:

1. no two coins have the same column vector;
2. no two coins have opposite column vectors.

In this construction, the 12 column vectors are pairwise distinct, and there are no indices $i,j$ such that $v_i=-v_j$.

If $v_i=v_j$, then the outcome $r=v_i$ could not distinguish coin $i$ being heavier from coin $j$ being heavier.

If $v_i=-v_j$, then the outcome $r=v_i$ would be ambiguous:

$$r=v_i\quad \Longrightarrow \quad \text{coin } i \text{ is heavier}$$

but also:

$$r=v_i=-v_j\quad \Longrightarrow \quad \text{coin } j \text{ is lighter}$$

Therefore, column vectors must be neither equal nor opposite.

The construction satisfies both conditions, so the 24 states:

$$\lbrace \text{coin } i \text{ heavy},\ \text{coin } i \text{ light}:1\le i\le 12 \rbrace$$

correspond to 24 distinct outcome vectors:

$$\lbrace v_i,-v_i:1\le i\le 12 \rbrace$$

Thus every possible outcome uniquely identifies both the counterfeit coin and whether it is heavier or lighter.

---

## 8. Why 13 Coins Cannot Be Solved in Three Weighings

Three weighings give:

$$3^3=27$$

possible outcome sequences.

If there are $n$ coins, then there are:

$$2n$$

possible states.

The information-theoretic condition is:

$$2n\le 27$$

which only implies:

$$n\le 13$$

However, without a known genuine coin, 13 coins still cannot be solved in 3 weighings.

The reason is as follows. Each coin must correspond to a nonzero column vector $v_i\in\lbrace -1,0,+1\rbrace^3$. If a coin had the zero vector as its column, then whether it was heavier or lighter would produce the same three outcomes, so it could not be identified.

Also, we cannot use both a vector $v$ and its opposite vector $-v$, because that would create ambiguity between a heavier coin and a lighter coin.

The set:

$$\lbrace -1,0,+1\rbrace^3\setminus\lbrace (0,0,0) \rbrace$$

contains:

$$3^3-1=26$$

nonzero vectors. These vectors form 13 opposite pairs.

If 13 coins were to be handled, we would have to choose exactly one representative from each of these 13 opposite pairs as a column vector.

Now look only at the first row. There are 9 opposite pairs whose first coordinate is nonzero. Therefore, after choosing one representative from each pair, the first row would contain 9 nonzero entries.

But a legal weighing must put the same number of coins on the left pan and on the right pan. Therefore, the number of $+1$ entries in this row must equal the number of $-1$ entries.

This requires the number of nonzero entries to be even.

However:

$$9\text{ is odd}$$

So the first weighing cannot be balanced. This is a contradiction.

Therefore, 13 coins cannot be solved in 3 weighings without a known genuine coin. The maximum number of coins solvable in 3 weighings is 12.

---

## 9. Conclusion

The three-weighing construction solves the twelve-coin counterfeit problem.

Each coin is assigned a ternary column vector. If the counterfeit coin is heavier, the outcome equals its column vector. If the counterfeit coin is lighter, the outcome equals the opposite of its column vector. Since the 12 column vectors are pairwise distinct and no two are opposite, all 24 possible states are uniquely identifiable.

The result is:

$$\text{3 weighings are sufficient to identify the counterfeit coin and its type among 12 coins.}$$

Moreover, 13 coins cannot be solved in 3 weighings without a known genuine coin. Therefore, the construction is optimal.

$$\blacksquare$$
