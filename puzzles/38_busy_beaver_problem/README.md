# 38_busy_beaver_problem

## 1. Formal Problem Statement

### 1.1 Basic Model

Consider a deterministic Turing machine (DTM) with the following properties:

- **Tape:** A two-way infinite tape divided into discrete cells.
- **Alphabet:** The alphabet contains only the symbols $0$ and $1$, where $0$ is the blank symbol. Initially, every tape cell contains $0$.
- **States:** The machine has $N$ working states, written as:

$$Q_N=\lbrace A,B,C,\ldots \rbrace$$

There is also a special halt state $Halt$.

### 1.2 Transition Rule

At each step, the machine looks at its current state and the symbol under the tape head, then performs three actions:

1. Write either $0$ or $1$ on the current cell.
2. Move the tape head one cell left $L$ or right $R$.
3. Switch to another working state, or enter the halt state.

### 1.3 Target Functions

Let $TM_N$ be the set of all machines satisfying the above conditions and having exactly $N$ working states. Some machines in $TM_N$ eventually halt, while others run forever.

We only consider the machines that eventually halt, and define two functions:

- **Busy beaver function $BB(N)$:** the maximum number of $1$s left on the tape when a halting $N$-state machine stops.
- **Maximum step function $S(N)$:** the maximum number of steps taken before halting by any halting $N$-state machine.

The main claim is:

$$S(N)\text{ is uncomputable}$$

and also:

$$BB(N)\text{ is uncomputable}$$

Equivalently, there is no general algorithm that computes the exact value of $S(N)$ or $BB(N)$ for arbitrary $N$.

---

## 2. Undecidability of the Halting Problem

### 2.1 Formal Definition

Every Turing machine $M$ can be encoded as a finite string, denoted by $\langle M \rangle$. The input to a Turing machine is also a finite string, denoted by $w$.

If $M$ eventually enters a halt state on input $w$, then $M(w)$ halts. Otherwise, $M(w)$ does not halt.

### 2.2 Assumption for Contradiction

Assume that the halting problem is decidable. Then there exists a decider $H$ that always halts and takes $\langle M \rangle$ and $w$ as input, satisfying:

$$H(\langle M \rangle,w)=\text{accept} \iff M(w)\text{ halts}$$

$$H(\langle M \rangle,w)=\text{reject} \iff M(w)\text{ does not halt}$$

By assumption, $H$ itself must always return a definite answer in finitely many steps.

### 2.3 Diagonal Machine

Using $H$ as a subroutine, construct a new machine $D$. The machine $D$ takes a machine encoding $\langle M \rangle$ as input and runs $H(\langle M \rangle,\langle M \rangle)$.

The behavior of $D$ is defined by:

$$H(\langle M \rangle,\langle M \rangle)=\text{accept} \implies D(\langle M \rangle)\text{ loops forever}$$

$$H(\langle M \rangle,\langle M \rangle)=\text{reject} \implies D(\langle M \rangle)\text{ halts}$$

Thus, on the diagonal input, $D$ does the opposite of what $H$ predicts.

### 2.4 Applying the Machine to Its Own Encoding

Since $D$ is a valid Turing machine, it has an encoding $\langle D \rangle$. Now consider $D(\langle D \rangle)$.

If $D(\langle D \rangle)$ halts, then by the definition of $D$, $H(\langle D \rangle,\langle D \rangle)$ must output $\text{reject}$. But by the definition of $H$, this means that $D(\langle D \rangle)$ does not halt, a contradiction.

If $D(\langle D \rangle)$ does not halt, then by the definition of $D$, $H(\langle D \rangle,\langle D \rangle)$ must output $\text{accept}$. But by the definition of $H$, this means that $D(\langle D \rangle)$ halts, a contradiction.

Therefore:

$$D(\langle D \rangle)\text{ halts} \iff D(\langle D \rangle)\text{ does not halt}$$

This contradiction shows that the assumed decider $H$ cannot exist.

$$\text{The halting problem is undecidable.}$$

---

## 3. Undecidability of Blank-Tape Halting

The busy beaver functions concern machines started on a blank tape. Therefore, we also need the blank-tape version of the halting problem.

Assume that there exists a decider $H_{blank}$ that determines whether any given machine $M$ halts when started on an all-blank tape.

Given a general halting instance $\langle M \rangle$ and $w$, construct a new machine $B_{M,w}$:

1. Starting from a blank tape, write the fixed string $w$ on the tape.
2. Move the head to the required initial position.
3. Simulate $M$ on input $w$.

Then:

$$B_{M,w}\text{ halts on blank tape} \iff M(w)\text{ halts}$$

If $H_{blank}$ existed, it would decide the general halting problem. This contradicts the undecidability of the halting problem.

Therefore:

$$\text{Blank-tape halting is undecidable.}$$

---

## 4. Uncomputability of the Maximum Step Function $S(N)$

### 4.1 Assumption for Contradiction

Assume that $S(N)$ is computable. Then there exists a Turing machine $M_S$ that, for every input $N$, halts and outputs the exact value of $S(N)$.

### 4.2 Constructing a Blank-Tape Halting Decider

Given any Turing machine $M$ with $N$ working states, we want to decide whether $M$ halts when started on a blank tape.

If $M_S$ exists, we can run the following algorithm:

1. Read the encoding $\langle M \rangle$ and determine the number of working states $N$.
2. Compute:

$$K=S(N)$$

3. Simulate $M$ on a blank tape for at most $K$ steps.
4. If $M$ halts within $K$ steps, output $\text{accept}$.
5. If $M$ has not halted after $K$ steps, output $\text{reject}$.

This algorithm is correct because, by the definition of $S(N)$, every halting $N$-state machine must halt within at most $S(N)$ steps.

Thus:

$$M\text{ halts on blank tape} \implies M\text{ halts within }S(N)\text{ steps}$$

So if $M$ has not halted within $S(N)$ steps, then $M$ never halts.

### 4.3 Contradiction

The construction above gives a decider for blank-tape halting. But blank-tape halting is undecidable.

Therefore, $S(N)$ cannot be computable.

$$S(N)\text{ is uncomputable.}$$

---

## 5. Uncomputability of the Busy Beaver Function $BB(N)$

The uncomputability of $BB(N)$ should be proved separately; it does not follow merely by saying that $S(N)$ is uncomputable.

### 5.1 Assumption for Contradiction

Assume that $BB(N)$ is computable. Then there exists a Turing machine $M_{BB}$ that, for every input $N$, halts and outputs the exact value of $BB(N)$.

### 5.2 Constructing a Simulator with a Counter

Given any Turing machine $M$, construct a new machine $C_M$. The machine $C_M$ starts on a blank tape and does the following:

1. Simulate $M$ on a blank tape.
2. For every simulated step of $M$, write one new $1$ in a separate counter region of the tape.
3. If $M$ halts, then $C_M$ also halts.
4. If $M$ does not halt, then $C_M$ does not halt.

This construction adds only finitely many states, and the number of states of $C_M$ can be effectively obtained from the encoding of $M$.

Therefore, if $M$ halts after $t$ steps, then $C_M$ halts with at least $t$ ones on the tape:

$$M\text{ halts after }t\text{ steps} \implies C_M\text{ halts with at least }t\text{ ones}$$

Let $N_C$ be the number of working states of $C_M$. If $BB(N)$ is computable, we can compute:

$$B=BB(N_C)$$

Since $BB(N_C)$ is the maximum number of ones left by any halting $N_C$-state machine, if $M$ halts after $t$ steps, then:

$$t \le B$$

Now simulate $M$ on a blank tape for at most $B$ steps:

- If $M$ halts within $B$ steps, output $\text{accept}$.
- If $M$ has not halted within $B$ steps, output $\text{reject}$.

This gives a decider for blank-tape halting.

### 5.3 Contradiction

Blank-tape halting is undecidable. Therefore, the assumption that $BB(N)$ is computable is false.

Hence:

$$BB(N)\text{ is uncomputable.}$$

---

## 6. Conclusion

The busy beaver problem is not only a finite enumeration problem. Its central difficulty is deciding which machines eventually halt and which machines run forever. That distinction already contains the undecidability of the halting problem.

Therefore, both functions are uncomputable:

$$S(N)\text{ is uncomputable}$$

$$BB(N)\text{ is uncomputable}$$

There is no general program that outputs the exact value of $S(N)$ or $BB(N)$ for arbitrary $N$.

$$\text{Q.E.D.}$$
