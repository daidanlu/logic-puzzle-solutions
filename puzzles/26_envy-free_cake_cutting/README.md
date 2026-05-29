# Envy-Free Cake-Cutting

## 1. Problem Setting

There are 3 rational participants, called Alice, Bob, and Charlie. They need to divide a continuous heterogeneous resource, usually described as a cake with different parts.

“Heterogeneous” means that different participants may assign different values to different parts of the cake, and these valuations are private. For example, Alice may think that the strawberry part is worth $80\%$ of the whole cake, while Bob may assign a much lower value to that part.

Let $V_i$ be participant $i$'s valuation function, and let $X_i$ be the piece finally assigned to participant $i$. The goal is to obtain an envy-free allocation. That is, for any two participants $i$ and $j$:

$$V_i(X_i) \ge V_i(X_j)$$

This means that no participant believes that someone else's piece is better than their own.

---

## 2. Algorithmic Challenge

With only 2 participants, the standard protocol is “I cut, you choose.” The cutter divides the cake into two pieces that are equal according to their own valuation, and the other participant chooses first. This guarantees that neither participant envies the other.

When the number of participants increases to 3, a simple turn-based cutting and choosing mechanism is no longer sufficient. For example, after Alice cuts the cake into three pieces, Bob and Charlie may choose the two pieces that Alice values the most. It is also possible that Bob believes Charlie's piece is better than his own.

Therefore, we need a deterministic discrete protocol. Regardless of the three participants' preferences, the protocol should terminate in finitely many steps and guarantee that the final allocation is envy-free.

---

## 3. The Selfridge-Conway Protocol

A classical protocol for the 3-person envy-free cake-cutting problem was independently discovered by John Selfridge and John Conway in the 1960s. The protocol handles the 3-person case by using trimming and asymmetric choosing.

Assume the three participants are Alice, Bob, and Charlie. The protocol has two stages.

---

## 4. Stage One: Trimming and Allocation of the Main Cake

### 4.1 Alice Cuts the Cake

Alice cuts the whole cake into 3 pieces that she values equally. In Alice's view, each piece is worth $1/3$ of the whole cake.

### 4.2 Bob Trims

Bob evaluates the 3 pieces.

- If Bob believes that two or three pieces are tied for largest, he does not trim.
- If Bob believes that one piece is strictly larger than the other two, he trims this largest piece until the trimmed piece has the same value as the second-largest piece according to Bob.
- The trimmed-off part is set aside and is not allocated during the first stage.

If no trimming occurs, then there is no trimmed-off remainder, and the protocol is completed after the first-stage choices. The rest of the proof considers the case where trimming occurs.

### 4.3 Charlie Chooses First

There are 3 main pieces on the table, one of which may have been trimmed by Bob. Charlie first chooses the piece he values the most.

### 4.4 Bob Chooses Second

Bob chooses his preferred piece among the remaining two pieces.

If Charlie did not take the trimmed piece, then Bob must take it. This does not hurt Bob, because in Bob's view, the trimmed piece is tied with another untrimmed piece for largest.

### 4.5 Alice Chooses Last

Alice takes the final remaining piece.

---

## 5. Envy-Freeness After Stage One

After the first stage, the allocation of the main cake is envy-free.

### Charlie

Charlie chooses first among the main pieces, so he does not envy anyone's main piece.

### Bob

Bob receives one of the pieces that is largest according to his valuation. If Charlie did not take the trimmed piece, Bob is required to take it; in Bob's view, this piece is equal in value to another untrimmed largest piece. Therefore, Bob does not envy anyone's main piece.

### Alice

Alice's final piece must be untrimmed. If a trimmed piece exists, it has already been taken by Charlie or Bob.

In Alice's view, each original piece was worth $1/3$. An untrimmed piece is still worth $1/3$, while a trimmed piece is worth no more than $1/3$. Therefore, Alice does not envy anyone's main piece.

---

## 6. Stage Two: Allocation of the Trimmed-Off Remainder

It remains to allocate the part trimmed off by Bob.

Let $T$ be the person who took the trimmed main piece, namely the Taker. Among Bob and Charlie, let $NT$ be the other person, namely the Non-Taker.

In Alice's view:

$$V_A(\text{T's main piece} \cup \text{all trimmed-off remainder}) = 1/3$$

This is because T's trimmed main piece plus all of the trimmed-off remainder exactly reconstructs one of the original pieces cut by Alice.

Therefore, even if all of the trimmed-off remainder were given to $T$, Alice would still value $T$'s total amount at no more than the value of Alice's own main piece. In this sense, Alice has a special no-envy guarantee with respect to $T$.

The protocol uses this asymmetry as follows.

### 6.1 NT Cuts the Remainder

$NT$ cuts the trimmed-off remainder into 3 equal parts according to $NT$'s own valuation.

### 6.2 Choosing Order

The choosing order is:

$$T \to \text{Alice} \to NT$$

- $T$ first chooses the part of the remainder that he likes best.
- Alice then chooses her preferred part among the remaining two.
- $NT$ receives the final remaining part.

---

## 7. Final Envy-Free Proof

We now check that the final allocation is envy-free.

### 7.1 NT Does Not Envy

The trimmed-off remainder was divided into three equal parts by $NT$, so all three parts have the same value according to $NT$. Although $NT$ chooses last, he does not envy anyone because of the remainder.

The main cake was already envy-free for $NT$ after the first stage. Therefore, $NT$ does not envy anyone in the final allocation.

### 7.2 T Does Not Envy

For the main cake, $T$ did not envy anyone after the first stage.

For the trimmed-off remainder, $T$ chooses first, so he receives his favorite part. Therefore, $T$ does not envy anyone in the final allocation.

### 7.3 Alice Does Not Envy NT

For the main cake, Alice and $NT$ both receive untrimmed pieces originally cut by Alice. Therefore, in Alice's view, both main pieces have value $1/3$.

For the trimmed-off remainder, Alice chooses before $NT$, so the part Alice receives is at least as good as the part $NT$ receives according to Alice's valuation. Therefore, Alice does not envy $NT$.

### 7.4 Alice Does Not Envy T

$T$ receives the trimmed main piece. From Alice's point of view, $T$'s main piece plus all of the trimmed-off remainder would only reconstruct one original piece cut by Alice:

$$V_A(\text{T's main piece} \cup \text{all trimmed-off remainder}) = 1/3$$

Alice's own main piece has value:

$$V_A(\text{Alice's main piece}) = 1/3$$

In the actual allocation, $T$ receives only one part of the trimmed-off remainder, not the entire remainder. Therefore, according to Alice:

$$V_A(\text{T's final share}) \le V_A(\text{Alice's final share})$$

So Alice does not envy $T$.

---

## 8. Conclusion

The Selfridge-Conway protocol completes a 3-person cake division in finitely many steps and guarantees an envy-free final allocation:

$$V_i(X_i) \ge V_i(X_j) \quad \text{for all } i,j\in\lbrace A,B,C\rbrace$$

The key step is Bob's trimming operation. It creates an asymmetric structure: Alice will not envy $T$ even when the trimmed-off remainder is allocated. Therefore, the remainder can be safely allocated in the order $T \to \text{Alice} \to NT$.

$$\blacksquare$$
