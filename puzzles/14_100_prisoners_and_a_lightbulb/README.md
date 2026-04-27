# 100 Prisoners and One-Bit Shared Memory: A Consensus Protocol for an Asynchronous System

This directory discusses the classical **100 prisoners and light bulb problem**, reinterpreted as a consensus protocol in an extremely constrained asynchronous distributed system.

The system has no clock synchronization, no point-to-point communication, and only a single $1$-bit shared memory cell. The question is how 100 independent computational nodes can use role reduction and one-way data flow to achieve a globally safe halting assertion.

---

## 1. Formal Setup

Consider a survival game in a fully asynchronous system consisting of $N=100$ independent nodes, also called prisoners.

### 1.1 Shared Memory

There is a single state register in the interrogation room, represented by a light bulb. Its state space is:

$$L\in\lbrace \text{ON},\text{OFF} \rbrace$$

The initial state is:

$$L=\text{OFF}$$

### 1.2 Scheduler

The system contains an unpredictable random scheduler, represented by the warden.

At each discrete time step $t$, that is, each day, the scheduler selects one of the 100 nodes uniformly and independently at random, and grants that node access to the shared memory.

### 1.3 Node Operations

The selected node can read the current state of $L$ and may overwrite it by executing either:

$$L\gets \text{ON}$$

or:

$$L\gets \text{OFF}$$

### 1.4 Global Assertion

Any node is allowed to call the system-level function:

```text
Halt_And_Assert()
```

This function asserts:

$$\text{All 100 nodes have been scheduled at least once.}$$

The winning condition is that this assertion is true, in which case all prisoners are released.

The losing condition is that this assertion is false, meaning that at least one node has never been scheduled. In that case, all prisoners lose immediately.

---

## 2. Breaking Symmetry

If all 100 nodes execute a completely symmetric algorithm, then because each node can observe only a $1$-bit shared state, no node can reliably distinguish between the following two cases:

$$\text{The light was turned on by myself.}$$

and:

$$\text{The light was turned on by someone else.}$$

In a fully symmetric system, multiple nodes may assign incompatible meanings to the same $1$-bit state, making reliable attribution impossible.

Therefore, the key idea of the protocol is to break symmetry deliberately.

Before the game begins, the prisoners elect one special node called the **counter** or **master**. The remaining 99 nodes are called **followers** or **slaves**.

The protocol establishes a strict one-way data flow:

$$\text{Follower} \to \text{Shared 1-bit memory} \to \text{Counter}$$

The roles are as follows:

- Each follower's only task is to use the $1$-bit shared memory to send exactly one pulse meaning "I have appeared."
- The counter's only task is to receive pulses, clear the shared memory, increment a local counter, and trigger the halting assertion once the count reaches 100.

---

## 3. Node Protocols

### 3.1 Follower FSM

Each follower maintains a local Boolean variable:

```text
has_transmitted = False
```

When a follower is selected by the scheduler and enters the room, it executes the following logic strictly.

If:

$$L=\text{OFF}$$

and:

```text
has_transmitted == False
```

then it executes:

```text
L = ON
has_transmitted = True
```

Otherwise, if the light is $\text{ON}$, or if this follower has already transmitted its signal, the follower does nothing and leaves the state unchanged.

Thus, each follower can perform at most one state transition of the form:

$$\text{OFF}\to\text{ON}$$

### 3.2 Counter FSM

The counter maintains a local integer accumulator:

```text
count = 1
```

The initial value is 1, representing the fact that the counter itself has already been confirmed to have appeared.

When the counter is selected by the scheduler and enters the room, it executes the following logic strictly.

If:

$$L=\text{ON}$$

then it executes:

```text
L = OFF
count += 1
```

Then, if:

```text
count == 100
```

it executes:

```text
Halt_And_Assert()
```

If the light is:

$$L=\text{OFF}$$

then the counter does nothing and leaves the state unchanged.

---

## 4. Proof of Correctness

A distributed consensus protocol must satisfy two properties:

1. **Safety**: the protocol never produces a false positive halting assertion.
2. **Liveness**: under fair random scheduling, the protocol eventually halts, and the probability of halting tends to 1.

---

## 5. Proof of Safety

We prove the following claim:

$$\text{If the counter calls Halt\_And\_Assert(), then all 100 prisoners have visited the room.}$$

### 5.1 Invariant

By the follower protocol, only a follower satisfying:

```text
has_transmitted == False
```

is allowed to change the light from $\text{OFF}$ to $\text{ON}$.

Once this operation occurs, that follower's local state is permanently updated to:

```text
has_transmitted = True
```

Therefore, each follower can generate at most one state transition:

$$\text{OFF}\to\text{ON}$$

There are 99 followers in the system, so the number of valid pulses generated by followers is at most 99.

On the other hand, by the counter protocol, only the counter changes the light from $\text{ON}$ to $\text{OFF}$. Each time the counter performs this operation, its local variable `count` increases by 1.

Let $C$ denote the counter's local count value. Let $B$ denote the unharvested pulse currently carried by the light bulb:

$$B=\begin{cases}1, & L=\text{ON},\\0, & L=\text{OFF}.\end{cases}$$

Let $T$ denote the total number of followers that have already transmitted their pulse.

The system always satisfies the following conservation invariant:

$$C+B=1+T$$

The left-hand side represents the number of nodes already confirmed by the counter, plus the unharvested pulse still stored in the light. The right-hand side represents the counter itself, plus the total number of followers that have already emitted a pulse.

### 5.2 Verification at Halt

When the counter calls:

```text
Halt_And_Assert()
```

we necessarily have:

$$C=100$$

Moreover, this call occurs immediately after the counter has read $\text{ON}$ and turned the light off, so:

$$B=0$$

Substituting into the conservation invariant:

$$C+B=1+T$$

we obtain:

$$100+0=1+T$$

Therefore:

$$T=99$$

There are exactly 99 followers in the system, and each follower can transmit at most one pulse. Hence, $T=99$ means that 99 distinct followers have all been scheduled and have each transmitted exactly one signal.

Together with the counter itself, which has also been scheduled, all 100 prisoners have entered the room.

Therefore, when the counter calls `Halt_And_Assert()`, the assertion must be true.

This proves the safety of the protocol.

$$\text{Safety holds.}$$

---

## 6. Proof of Liveness

We prove that under infinite random scheduling, the system eventually halts with probability 1.

Assume that there is still a set of followers that have not yet transmitted:

$$U\subseteq\lbrace \text{followers} \rbrace$$

and:

$$|U|=k>0$$

### 6.1 Generating a Pulse

If the current light state is:

$$L=\text{OFF}$$

then the probability that the scheduler selects some follower in $U$ is:

$$P_1=\frac{k}{100}>0$$

Once such a follower is selected, it turns the light on:

$$\text{OFF}\to\text{ON}$$

Thus, the system generates a new unharvested pulse.

### 6.2 Harvesting a Pulse

If the current light state is:

$$L=\text{ON}$$

then the probability that the scheduler selects the counter is:

$$P_2=\frac{1}{100}>0$$

Once the counter is selected, it turns the light off and increments its counter by 1:

$$\text{ON}\to\text{OFF}$$

Therefore, one complete information-transfer cycle has the form:

$$\text{unsignaled follower visits} \to \text{light becomes ON} \to \text{counter visits} \to \text{light becomes OFF}$$

### 6.3 Almost-Sure Progress

As long as there remains at least one follower that has not transmitted, and as long as the light eventually returns to $\text{OFF}$, the system has positive probability of completing the next valid pulse transfer.

Since the scheduler independently and uniformly selects one node from the 100 nodes each day, every fixed node is selected at least once over infinite time with probability 1.

Therefore:

$$\Pr(\text{each particular prisoner is eventually scheduled})=1$$

Furthermore, every follower that has not yet transmitted will eventually be scheduled at a time when the light is $\text{OFF}$ and will successfully send its unique pulse. Every generated pulse will also eventually be harvested by the counter.

Hence, as time tends to infinity, the probability that the counter's local count eventually reaches 100 is 1:

$$\lim_{t\to\infty}\Pr(C_t=100)=1$$

Therefore, the protocol eventually halts with probability 1.

This proves the liveness of the protocol.

$$\text{Liveness holds almost surely.}$$

---

## 7. Conclusion

This protocol deliberately breaks the complete symmetry among the 100 nodes by electing one counter in advance.

Followers only send one-time pulses, while the counter only harvests pulses and increments its local count. Thus, the single $1$-bit shared memory cell is interpreted as a consumable pulse channel:

$$\text{Follower signal} \to \text{1-bit shared memory} \to \text{Counter confirmation}$$

Safety follows from the conservation invariant:

$$C+B=1+T$$

Liveness follows from the random scheduler's fair infinite access to every node:

$$\lim_{t\to\infty}\Pr(C_t=100)=1$$

Therefore, the protocol is logically safe, and in the probabilistic sense, it almost surely reaches global consensus and halts.

$$\blacksquare$$
