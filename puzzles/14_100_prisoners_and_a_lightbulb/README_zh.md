# 100 囚犯与单比特共享内存：异步系统的共识协议与证明

本目录讨论经典的 **100 囚犯与灯泡问题**，并将其解释为一个极端受限的异步分布式系统中的共识协议。

系统中没有时钟同步，没有点对点通信，只有一块 $1$-bit 共享内存。问题是：100 个独立计算节点如何通过角色降维与单向数据流，实现绝对安全的全局停机断言。

---

## 1. Formal Setup

在一个由 $N=100$ 个独立节点，也就是囚犯，构成的完全异步系统中进行生存博弈。

### 1.1 Shared Memory

审讯室中存在唯一的状态寄存器，即灯泡。其状态空间为：

$$L\in\lbrace \text{ON},\text{OFF} \rbrace$$

初始状态为：

$$L=\text{OFF}$$

### 1.2 Scheduler

系统存在一个不可预测的随机调度器，即典狱长。

在每一个离散时间步 $t$，也就是每天，调度器从 100 个节点中均匀且独立地随机抽取一个节点，并将该节点接入共享内存。

### 1.3 Node Operations

被接入的节点可以读取 $L$ 的当前状态，并且可以执行覆写操作：

$$L\gets \text{ON}$$

或：

$$L\gets \text{OFF}$$

### 1.4 Global Assertion

任何节点都有权调用系统级函数：

```text
Halt_And_Assert()
```

该函数断言：

$$\text{All 100 nodes have been scheduled at least once.}$$

胜出条件为：该断言为真，全体无罪释放。

失败条件为：该断言为假，即存在至少一个从未被调度过的节点，全体立即失败。

---

## 2. Breaking Symmetry

如果 100 个节点执行完全对称的算法代码，那么由于每个人只能观察到 $1$-bit 的共享状态，他们无法区分以下两种情况：

$$\text{The light was turned on by myself.}$$

和：

$$\text{The light was turned on by someone else.}$$

在完全对称系统中，多个节点对同一个 $1$-bit 状态的解释会相互叠加，导致信息无法被可靠归因。

因此，协议的关键是主动打破对称性。

囚犯们在游戏开始前选出一个特殊节点，称为 **计数者**（Counter / Master）。其余 99 个节点称为 **跟随者**（Followers / Slaves）。

协议建立一条严格的单向数据流：

$$\text{Follower} \to \text{Shared 1-bit memory} \to \text{Counter}$$

其中：

- 跟随者的唯一任务是：通过这块 $1$-bit 共享内存，向计数者发送一次且仅一次“我已经出现过”的脉冲信号。
- 计数者的唯一任务是：接收脉冲，清空共享内存，在本地计数器中累加，并在计数达到 100 时触发停机断言。

---

## 3. Node Protocols

### 3.1 Follower FSM

每个跟随者在本地内存中维护一个布尔变量：

```text
has_transmitted = False
```

当跟随者被调度器接入房间时，严格执行以下逻辑。

如果：

$$L=\text{OFF}$$

并且：

```text
has_transmitted == False
```

则执行：

```text
L = ON
has_transmitted = True
```

否则，如果灯泡为 $\text{ON}$，或者该跟随者已经发送过信号，则不执行任何操作，保持状态不变并离开。

也就是说，跟随者最多只会执行一次状态翻转：

$$\text{OFF}\to\text{ON}$$

### 3.2 Counter FSM

计数者在本地维护一个整型累加器：

```text
count = 1
```

初始值为 1，表示计数者自己已经被确认出现过。

当计数者被调度器接入房间时，严格执行以下逻辑。

如果：

$$L=\text{ON}$$

则执行：

```text
L = OFF
count += 1
```

随后，如果：

```text
count == 100
```

则执行：

```text
Halt_And_Assert()
```

如果灯泡为：

$$L=\text{OFF}$$

则计数者不执行任何操作，保持状态不变并离开。

---

## 4. Proof of Correctness

一个分布式共识协议必须同时满足两个性质：

1. **安全性**（Safety）：协议绝对不会产生假阳性停机断言。
2. **活性**（Liveness）：在公平随机调度下，协议最终会停机，且停机概率趋近于 1。

---

## 5. Proof of Safety

我们要证明：

$$\text{If the counter calls Halt\_And\_Assert(), then all 100 prisoners have visited the room.}$$

### 5.1 Invariant

根据跟随者协议，只有满足：

```text
has_transmitted == False
```

的跟随者，才有权限将灯泡从 $\text{OFF}$ 变为 $\text{ON}$。

并且一旦该操作发生，该跟随者的本地状态会被永久更新为：

```text
has_transmitted = True
```

因此，每名跟随者最多只能产生一次状态翻转：

$$\text{OFF}\to\text{ON}$$

系统中一共有 99 名跟随者，所以跟随者产生的有效脉冲数最多为 99。

另一方面，根据计数者协议，只有计数者会将灯泡从 $\text{ON}$ 变为 $\text{OFF}$。每当计数者执行一次该操作，计数器 `count` 就增加 1。

令 $C$ 表示计数者的本地计数值。令 $B$ 表示灯泡当前携带的未收割脉冲：

$$B=\begin{cases}1, & L=\text{ON},\\0, & L=\text{OFF}.\end{cases}$$

令 $T$ 表示已经发送过脉冲信号的跟随者总数。

系统始终满足如下守恒不变量：

$$C+B=1+T$$

其中，左侧表示“已经被计数者确认的节点数”加上“当前仍保存在灯泡中的未收割脉冲”；右侧表示“计数者本人”加上“已经发出过脉冲的跟随者总数”。

### 5.2 Verification at Halt

当计数者调用：

```text
Halt_And_Assert()
```

时，必然有：

$$C=100$$

而且该调用发生在计数者刚刚读取到 $\text{ON}$ 并将灯泡关闭之后，所以：

$$B=0$$

代入守恒不变量：

$$C+B=1+T$$

得到：

$$100+0=1+T$$

因此：

$$T=99$$

系统中总共只有 99 名跟随者，并且每名跟随者最多只能发送一次脉冲。因此， $T=99$ 意味着 99 名不同的跟随者都已经被调度过，并且都各自发送过一次信号。

再加上计数者本人已经被调度过，100 名囚犯全部都已经进入过房间。

所以，当计数者调用 `Halt_And_Assert()` 时，断言必然为真。

这证明了协议的安全性。

$$\text{Safety holds.}$$

---

## 6. Proof of Liveness

我们要证明：在无限时间随机调度下，系统最终会停机，且停机概率为 1。

假设当前仍有未发送信号的跟随者集合：

$$U\subseteq\lbrace \text{followers} \rbrace$$

并且：

$$|U|=k>0$$

### 6.1 Generating a Pulse

如果当前灯泡为：

$$L=\text{OFF}$$

那么调度器抽中集合 $U$ 中任意一名跟随者的概率为：

$$P_1=\frac{k}{100}>0$$

一旦抽中，该跟随者会将灯泡打开：

$$\text{OFF}\to\text{ON}$$

于是系统产生一个新的未收割脉冲。

### 6.2 Harvesting a Pulse

如果当前灯泡为：

$$L=\text{ON}$$

那么调度器抽中计数者的概率为：

$$P_2=\frac{1}{100}>0$$

一旦抽中，计数者会将灯泡关闭，并使计数器增加 1：

$$\text{ON}\to\text{OFF}$$

因此，每一次完整的信息传递循环为：

$$\text{unsignaled follower visits} \to \text{light becomes ON} \to \text{counter visits} \to \text{light becomes OFF}$$

### 6.3 Almost-Sure Progress

只要还有未发送信号的跟随者，且灯泡最终能够回到 $\text{OFF}$，系统就存在正概率完成下一次有效脉冲传递。

由于调度器在每一天都从 100 个节点中独立且均匀地随机抽取一个节点，每一个固定节点在无限时间内被抽中的概率为 1。

因此：

$$\Pr(\text{each particular prisoner is eventually scheduled})=1$$

进一步地，每一个尚未发送信号的跟随者最终都会在某个灯泡为 $\text{OFF}$ 的时刻被调度到，并成功发送自己的唯一脉冲；每一个已产生的脉冲也最终都会被计数者收割。

于是，随着时间趋向无穷，计数者的本地计数值最终达到 100 的概率为 1：

$$\lim_{t\to\infty}\Pr(C_t=100)=1$$

因此，协议在概率 1 的意义下最终停机。

这证明了协议的活性。

$$\text{Liveness holds almost surely.}$$

---

## 7. Conclusion

该协议通过预先选举一个计数者，主动打破了 100 个节点之间的完全对称性。

跟随者只负责发送一次性脉冲，计数者只负责收割脉冲并累加计数。于是，唯一的 $1$-bit 共享内存被严格解释为一种消耗性的脉冲信道：

$$\text{Follower signal} \to \text{1-bit shared memory} \to \text{Counter confirmation}$$

安全性来自守恒不变量：

$$C+B=1+T$$

活性来自随机调度器对每个节点的无限次公平访问：

$$\lim_{t\to\infty}\Pr(C_t=100)=1$$

因此，在逻辑上，该协议是安全的；在概率意义上，该协议最终几乎必然达成全局共识并停机。

$$\blacksquare$$
