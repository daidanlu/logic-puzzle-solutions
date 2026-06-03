# 佩尼博弈：非传递性与后手优势

## Overview

在构建多智能体演化博弈沙盒，例如 Evolutio 的策略配对池时，我们常常假设系统优势具有传递性：

$$A \succ B,\quad B \succ C \implies A \succ C$$

但 Penney's Game 展示了一个反直觉现象：即使底层随机过程完全公平，引入时序模式匹配之后，策略之间仍然可能出现非传递性的克制关系。

---

## 1. System Model

准备一枚公平硬币。每次抛掷得到正面 `H` 或反面 `T` 的概率均为：

$$P(H)=P(T)=\frac{1}{2}$$

系统中有两名博弈者：

- Alice 为先手。
- Bob 为后手。

游戏规则如下：

1. Alice 首先公开选择一个长度为 3 的序列，例如 `HTT`。
2. Bob 看到 Alice 的选择后，公开选择一个不同的长度为 3 的序列，例如 `THT`。
3. 系统不断抛掷硬币，生成随机状态流。
4. 谁选择的序列最先完整连续出现，谁获胜，系统停机。

直觉上，每个长度为 3 的序列出现的长期频率相同，因此先手和后手似乎应接近五五开。实际情况并非如此。

Penney's Game 的关键不是某个序列是否“更容易出现”，而是两个序列在随机流中谁能先拦截对方。

---

## 2. Conway's Counterstrategy

数学家 John Horton Conway 给出了一个简单的后手反制规则。

设 Alice 选择的序列为：

$$A=A_1A_2A_3$$

Bob 构造的序列为：

$$B=B_1B_2B_3$$

规则为：

$$B_1=\neg A_2,\quad B_2=A_1,\quad B_3=A_2$$

也就是说，Bob 复制 Alice 的前两个符号作为自己的后两个符号，并把 Alice 的第二个符号取反后放在最前面。

例如，如果 Alice 选择：

$$A=\text{HHT}$$

则 Bob 选择：

$$B=\text{THH}$$

---

## 3. Example: Why `THH` Beats `HHT`

现在考虑：

$$A=\text{HHT},\quad B=\text{THH}$$

我们要证明 Bob 选择 `THH` 时，其获胜概率为：

$$P(B)=\frac{3}{4}=75\%$$

---

## 4. State-Space Argument

将无限硬币流按照前几次抛掷结果划分为四个互斥分支。

### Branch 1: The first toss is `T`

该分支的概率为：

$$\frac{1}{2}$$

当前尾部状态为 `T`。之后 Alice 若要形成 `HHT`，必须先在某个时刻形成连续的 `HH`。但只要在尾部 `T` 之后先出现 `HH`，随机流就已经形成：

$$\text{THH}$$

因此 Bob 会先于 Alice 触发胜利条件。该分支中 Bob 必胜。

### Branch 2: The first two tosses are `HT`

该分支的概率为：

$$\frac{1}{4}$$

当前尾部再次为 `T`，因此后续逻辑与 Branch 1 相同。Bob 必胜。

### Branch 3: The first three tosses are `HHT`

该分支的概率为：

$$\frac{1}{8}$$

Alice 的目标序列直接出现，游戏立刻结束。Bob 必败。

### Branch 4: The first three tosses are `HHH`

该分支的概率为：

$$\frac{1}{8}$$

当前流末尾为连续的 `HH`。Bob 若要形成 `THH`，必须先等待一个 `T` 作为新的开头。但在当前连续 `HH` 之后，一旦出现 `T`，随机流立即形成：

$$\text{HHT}$$

因此 Alice 会先触发胜利条件。Bob 必败。

综上：

$$P(B)=\frac{1}{2}\cdot 1+\frac{1}{4}\cdot 1+\frac{1}{8}\cdot 0+\frac{1}{8}\cdot 0=\frac{3}{4}$$

因此：

$$P(B)=75\%$$

---

## 5. Conway's Leading Number Algorithm

除了状态空间分析，也可以使用前缀重叠算法直接计算胜率。

### Definition

对于两个长度为 $n$ 的序列 $X$ 和 $Y$，定义 $X \cdot Y$ 为：

- 对每个 $k=1,2,\dots,n$；
- 比较 $X$ 的后 $k$ 位与 $Y$ 的前 $k$ 位；
- 如果完全相等，则记录 $2^{k-1}$；
- 将所有命中的数值相加。

这个值衡量的是序列 $X$ 的后缀能够覆盖序列 $Y$ 的前缀的程度。

---

## 6. Computing the Overlaps

令：

$$A=\text{HHT},\quad B=\text{THH}$$

### 6.1 Self-overlap of Alice

对于 $A \cdot A$：

- $k=3$: `HHT` equals `HHT`, record $4$.
- $k=2$: `HT` does not equal `HH`, record $0$.
- $k=1$: `T` does not equal `H`, record $0$.

因此：

$$A \cdot A=4$$

### 6.2 Self-overlap of Bob

对于 $B \cdot B$：

- $k=3$: `THH` equals `THH`, record $4$.
- $k=2$: `HH` does not equal `TH`, record $0$.
- $k=1$: `H` does not equal `T`, record $0$.

因此：

$$B \cdot B=4$$

### 6.3 Alice-to-Bob overlap

对于 $A \cdot B$：

- $k=3$: `HHT` does not equal `THH`, record $0$.
- $k=2$: `HT` does not equal `TH`, record $0$.
- $k=1$: `T` equals `T`, record $1$.

因此：

$$A \cdot B=1$$

### 6.4 Bob-to-Alice overlap

对于 $B \cdot A$：

- $k=3$: `THH` does not equal `HHT`, record $0$.
- $k=2$: `HH` equals `HH`, record $2$.
- $k=1$: `H` equals `H`, record $1$.

因此：

$$B \cdot A=3$$

---

## 7. Odds Formula

Conway 的赔率公式为：

$$\frac{P(B)}{P(A)}=\frac{A \cdot A-A \cdot B}{B \cdot B-B \cdot A}$$

代入上面的数值：

$$\frac{P(B)}{P(A)}=\frac{4-1}{4-3}=3$$

所以：

$$P(B):P(A)=3:1$$

归一化得到：

$$P(B)=\frac{3}{3+1}=\frac{3}{4}=75\%$$

这与状态空间分析得到的结果一致。

---

## 8. General Counterstrategy Table

Conway 规则对 Alice 的任意长度为 3 的序列都有效。Bob 的最优反制序列如下：

| Alice's sequence | Bob's countersequence | Bob's winning probability |
|---|---:|---:|
| `HHH` | `THH` | $7/8=87.5\%$ |
| `HHT` | `THH` | $3/4=75\%$ |
| `HTH` | `HHT` | $2/3\approx 66.7\%$ |
| `HTT` | `HHT` | $2/3\approx 66.7\%$ |
| `THH` | `TTH` | $2/3\approx 66.7\%$ |
| `THT` | `TTH` | $2/3\approx 66.7\%$ |
| `TTH` | `HTT` | $3/4=75\%$ |
| `TTT` | `HTT` | $7/8=87.5\%$ |

因此，对任意 Alice 的选择，Bob 都能找到一个反制序列，使自己的胜率至少为：

$$\frac{2}{3}\approx 66.7\%$$

最高可达到：

$$\frac{7}{8}=87.5\%$$

---

## 9. Non-Transitive Cycle

在策略池：

$$\lbrace \text{HTT},\text{HHT},\text{THH},\text{TTH} \rbrace$$

中存在如下克制闭环：

$$\text{HTT}<\text{HHT}<\text{THH}<\text{TTH}<\text{HTT}$$

这里的 $X<Y$ 表示序列 $Y$ 在二者对局中优于序列 $X$。

具体来说：

$$\text{HHT beats HTT}$$

$$\text{THH beats HHT}$$

$$\text{TTH beats THH}$$

$$\text{HTT beats TTH}$$

这说明该系统不存在全局最强策略。优势关系不是线性的，而是循环的。

---

## 10. Conclusion

Penney's Game 说明，在多智能体博弈系统中，即使底层随机单元完全公平且独立，宏观策略关系仍然可能出现非传递性。

其原因不在于某个长度为 3 的序列具有更高的绝对出现概率，而在于不同序列之间存在前缀与后缀的覆盖结构。

核心现象可以概括为：

$$\text{fair randomness}+\text{temporal pattern matching}\implies \text{non-transitive advantage}$$

因此，在设计演化博弈沙盒或策略配对池时，不能简单假设：

$$A \succ B,\quad B \succ C \implies A \succ C$$

Penney's Game 提供了一个简洁的反例：局部公平并不保证全局传递性。

$$\text{Q.E.D.}$$
