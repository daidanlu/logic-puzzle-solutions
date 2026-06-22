# 38_busy_beaver_problem（忙碌的海狸问题）

## 一、问题的形式化题设

### 1. 基础环境定义

考虑一台确定性图灵机（Deterministic Turing Machine, DTM），其具备以下属性：

- **纸带（Tape）：** 一条双向无限长的纸带，划分为离散格子。
- **字母表（Alphabet）：** 仅包含两个符号 $0$ 和 $1$，其中 $0$ 表示空白符号。初始状态下，整条纸带全为 $0$。
- **状态集（States）：** 拥有 $N$ 个工作状态，记为：

$$Q_N=\lbrace A,B,C,\ldots \rbrace$$

此外还有一个特殊的停机状态 $Halt$。

### 2. 转移规则

在任意时刻，图灵机根据当前状态和当前格子的符号，执行以下三个动作：

1. 将当前格子改写为 $0$ 或 $1$。
2. 将读写头向左 $L$ 或向右 $R$ 移动一格。
3. 切换到另一个工作状态，或进入停机状态。

### 3. 目标函数定义

令 $TM_N$ 表示所有满足上述条件且包含 $N$ 个工作状态的图灵机集合。其中一部分机器会在有限步后停机，另一部分机器会无限运行。

我们只考虑最终能够停机的机器，并定义两个函数：

- **忙碌海狸函数 $BB(N)$：** 所有能停机的 $N$ 状态图灵机中，停机时纸带上留下的 $1$ 的最大数量。
- **最大步数函数 $S(N)$：** 所有能停机的 $N$ 状态图灵机中，停机前运行步数的最大值。

本文要证明的核心结论是：

$$S(N)\text{ is uncomputable}$$

并进一步得到：

$$BB(N)\text{ is uncomputable}$$

也就是说，不存在一个通用算法可以对任意 $N$ 计算出 $S(N)$ 或 $BB(N)$ 的精确值。

---

## 二、停机问题不可判定

### 1. 形式化定义

任意一台图灵机 $M$ 都可以编码为有限字符串，记为 $\langle M \rangle$。图灵机的输入也是有限字符串，记为 $w$。

如果 $M$ 在输入 $w$ 上最终进入停机状态，则称 $M(w)$ 停机；否则称 $M(w)$ 不停机。

### 2. 反证法假设

假设停机问题是可判定的。也就是说，存在一台总能停机的判定机 $H$，它接收 $\langle M \rangle$ 和 $w$ 作为输入，并满足：

$$H(\langle M \rangle,w)=\text{accept} \iff M(w)\text{ halts}$$

$$H(\langle M \rangle,w)=\text{reject} \iff M(w)\text{ does not halt}$$

根据假设， $H$ 自身必须在有限步内输出确定结果。

### 3. 构造自指机器

利用 $H$ 构造一台新机器 $D$。机器 $D$ 接收一个图灵机编码 $\langle M \rangle$，并运行 $H(\langle M \rangle,\langle M \rangle)$。

机器 $D$ 的行为定义为：

$$H(\langle M \rangle,\langle M \rangle)=\text{accept} \implies D(\langle M \rangle)\text{ loops forever}$$

$$H(\langle M \rangle,\langle M \rangle)=\text{reject} \implies D(\langle M \rangle)\text{ halts}$$

也就是说， $D$ 在对角输入上执行与 $H$ 预测相反的行为。

### 4. 代入自身编码

因为 $D$ 是合法图灵机，它也有编码 $\langle D \rangle$。现在考察 $D(\langle D \rangle)$。

如果 $D(\langle D \rangle)$ 停机，那么按照 $D$ 的定义， $H(\langle D \rangle,\langle D \rangle)$ 必须输出 $\text{reject}$。但按照 $H$ 的定义，这意味着 $D(\langle D \rangle)$ 不停机，矛盾。

如果 $D(\langle D \rangle)$ 不停机，那么按照 $D$ 的定义， $H(\langle D \rangle,\langle D \rangle)$ 必须输出 $\text{accept}$。但按照 $H$ 的定义，这意味着 $D(\langle D \rangle)$ 停机，矛盾。

因此得到矛盾链：

$$D(\langle D \rangle)\text{ halts} \iff D(\langle D \rangle)\text{ does not halt}$$

所以假设的判定机 $H$ 不存在。

$$\text{The halting problem is undecidable.}$$

---

## 三、空白纸带停机问题不可判定

忙碌海狸函数只讨论空白纸带上的机器。因此，在使用停机问题时，需要先说明空白纸带停机问题也不可判定。

假设存在一台判定机 $H_{blank}$，它能判断任意图灵机 $M$ 从全空白纸带开始运行时是否会停机。

给定一般停机问题实例 $\langle M \rangle$ 和 $w$，构造一台新机器 $B_{M,w}$：

1. 在空白纸带上写入固定字符串 $w$。
2. 将读写头移动到模拟所需的初始位置。
3. 模拟 $M$ 在输入 $w$ 上的运行。

于是有：

$$B_{M,w}\text{ halts on blank tape} \iff M(w)\text{ halts}$$

如果 $H_{blank}$ 存在，就可以用它判定任意 $M(w)$ 是否停机。这与停机问题不可判定矛盾。

因此：

$$\text{Blank-tape halting is undecidable.}$$

---

## 四、最大步数函数 $S(N)$ 不可计算

### 1. 反证法假设

假设 $S(N)$ 是可计算函数。也就是说，存在一台图灵机 $M_S$，对任意输入 $N$ 都能在有限步内输出 $S(N)$ 的精确值。

### 2. 构造空白纸带停机判定机

给定任意一台有 $N$ 个工作状态的图灵机 $M$，并要求判断它从空白纸带开始是否停机。

如果 $M_S$ 存在，则可以执行以下算法：

1. 从 $\langle M \rangle$ 中读出 $M$ 的工作状态数 $N$。
2. 计算：

$$K=S(N)$$

3. 在空白纸带上模拟 $M$ 的运行，最多模拟 $K$ 步。
4. 如果 $M$ 在 $K$ 步以内停机，输出 $\text{accept}$。
5. 如果 $M$ 运行 $K$ 步后仍未停机，输出 $\text{reject}$。

这个算法是正确的，因为按照 $S(N)$ 的定义，任何会停机的 $N$ 状态机器都必须在至多 $S(N)$ 步内停机。

因此：

$$M\text{ halts on blank tape} \implies M\text{ halts within }S(N)\text{ steps}$$

所以若 $M$ 在 $S(N)$ 步内没有停机，则 $M$ 永远不会停机。

### 3. 矛盾

上述构造给出了空白纸带停机问题的判定机。但第三部分已经说明，空白纸带停机问题不可判定。

因此， $S(N)$ 不可能是可计算函数。

$$S(N)\text{ is uncomputable.}$$

---

## 五、忙碌海狸函数 $BB(N)$ 不可计算

还需要单独说明 $BB(N)$ 的不可计算性，不能只从 $S(N)$ 不可计算直接推出。

### 1. 反证法假设

假设 $BB(N)$ 是可计算函数。也就是说，存在一台图灵机 $M_{BB}$，对任意输入 $N$ 都能在有限步内输出 $BB(N)$ 的精确值。

### 2. 构造带计数器的模拟机器

给定任意图灵机 $M$，构造一台新机器 $C_M$。机器 $C_M$ 在空白纸带上运行，并执行以下任务：

1. 模拟 $M$ 在空白纸带上的运行。
2. 每模拟 $M$ 的一步，就在纸带的计数区域额外写下一个新的 $1$。
3. 如果 $M$ 停机，则 $C_M$ 也停机。
4. 如果 $M$ 不停机，则 $C_M$ 也不停机。

这个构造只增加有限个状态，且 $C_M$ 的状态数可以从 $M$ 的编码有效得到。

因此，如果 $M$ 在 $t$ 步后停机，那么 $C_M$ 停机时至少留下 $t$ 个 $1$：

$$M\text{ halts after }t\text{ steps} \implies C_M\text{ halts with at least }t\text{ ones}$$

令 $C_M$ 的工作状态数为 $N_C$。如果 $BB(N)$ 可计算，就可以计算：

$$B=BB(N_C)$$

由于 $BB(N_C)$ 是所有能停机的 $N_C$ 状态机器停机时留下的 $1$ 的最大数量，如果 $M$ 在 $t$ 步后停机，则必有：

$$t \le B$$

于是，只需要在空白纸带上模拟 $M$ 最多 $B$ 步：

- 如果 $M$ 在 $B$ 步以内停机，输出 $\text{accept}$。
- 如果 $M$ 在 $B$ 步以内没有停机，输出 $\text{reject}$。

这就构造出了空白纸带停机问题的判定机。

### 3. 矛盾

空白纸带停机问题不可判定，因此假设 $BB(N)$ 可计算不成立。

所以：

$$BB(N)\text{ is uncomputable.}$$

---

## 六、结论

忙碌海狸问题的核心不是单纯枚举有限数量的机器，而是要区分哪些机器最终停机、哪些机器永远运行。这个区分本身已经包含停机问题的不可判定性。

因此，两个函数都不可计算：

$$S(N)\text{ is uncomputable}$$

$$BB(N)\text{ is uncomputable}$$

这意味着不存在一个通用程序，能够对任意 $N$ 输出 $S(N)$ 或 $BB(N)$ 的精确值。

$$\text{Q.E.D.}$$
