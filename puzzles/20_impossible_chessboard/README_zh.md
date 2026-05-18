# 恶魔的 64 格棋盘密码

## Puzzle Statement

有一张标准的 $8 \times 8$ 棋盘，共有 $64$ 个格子，编号为 $0,1,2,\ldots,63$。

每个格子上放一枚硬币，硬币状态任意：

$$\text{heads}=1, \quad \text{tails}=0$$

典狱长将钥匙藏在某个格子下面，设钥匙位置为 $K$。
Alice 能看到钥匙位置和初始硬币状态，Bob 只能看到 Alice 操作后的棋盘。

Alice 和 Bob 可以事先约定协议。游戏开始后，Alice 必须且只能翻转恰好一枚硬币。随后 Bob 进入房间，只能根据当前棋盘状态指出钥匙位置。

目标是设计一个协议，使 Bob 总能正确指出 $K$。

---

## Mathematical Model

将每个格子编号看作一个 $6$ 位二进制向量。
因为：

$$64=2^6$$

所以每个编号都可以看作有限域向量空间 $\mathbb{F}_2^6$ 中的一个元素。

对任意棋盘状态，定义它的 XOR 校验和为所有正面朝上硬币所在格子编号的异或和：

$$P=\bigoplus_{i:\,c_i=1} i$$

其中 $c_i$ 表示第 $i$ 格硬币的状态。

Bob 的解码规则是：计算当前棋盘的校验和 $P$，并将 $P$ 作为钥匙位置。

---

## Key Observation

翻转第 $F$ 格硬币，无论它原来是正面还是反面，都会使校验和异或上 $F$。

因此，若翻转前的校验和为 $P_{current}$，翻转第 $F$ 格后的校验和为：

$$P_{new}=P_{current}\oplus F$$

这是因为在 $\mathbb{F}_2$ 中，每个元素都是自己的加法逆元：

$$F\oplus F=0$$

所以加入 $F$ 和删除 $F$ 在 XOR 运算中是同一个操作。

---

## Protocol

Alice 先计算当前棋盘的校验和：

$$P_{current}=\bigoplus_{i:\,c_i=1} i$$

她希望 Bob 最后算出的校验和等于钥匙位置 $K$。
因此 Alice 需要选择一个格子 $F$，使得：

$$P_{current}\oplus F=K$$

由 XOR 的自反性可得：

$$F=P_{current}\oplus K$$

Alice 翻转第 $F$ 格硬币。
Bob 进入房间后重新计算校验和，并输出该校验和。

---

## Correctness Proof

Alice 翻转第 $F$ 格后，Bob 看到的新棋盘校验和为：

$$P_{new}=P_{current}\oplus F$$

根据协议，Alice 选择：

$$F=P_{current}\oplus K$$

代入得到：

$$P_{new}=P_{current}\oplus (P_{current}\oplus K)$$

由结合律和 $P_{current}\oplus P_{current}=0$，有：

$$P_{new}=(P_{current}\oplus P_{current})\oplus K$$

因此：

$$P_{new}=0\oplus K=K$$

所以 Bob 的输出必定等于钥匙位置 $K$。

$$\blacksquare$$

---

## Edge Case

如果初始校验和已经等于钥匙位置，即：

$$P_{current}=K$$

则 Alice 的公式给出：

$$F=P_{current}\oplus K=0$$

Alice 翻转第 $0$ 格硬币。
由于第 $0$ 格编号为 $000000$，翻转它不会改变 XOR 校验和：

$$P_{new}=P_{current}\oplus 0=P_{current}=K$$

因此即使 Alice 必须翻转一枚硬币，协议仍然有效。

---

## Why This Works

Alice 并不是把信息写进某一枚硬币的正反面，而是利用“翻转哪一个位置”来改变整个棋盘的全局校验和。

$64$ 个可选择的位置正好提供 $6$ 比特信息：

$$\log_2 64=6$$

而钥匙位置也正好需要 $6$ 比特表示。

这道谜题的核心思想是：在 $\mathbb{F}_2^6$ 中，每个棋盘状态都有一个全局 XOR 指纹。Alice 只需翻转一个精确选择的位置，就能把这个指纹路由到任意目标格子。

---

## Conclusion

这个协议说明，受限通信并不一定意味着只能修改局部信息。
在合适的代数结构下，一个局部动作可以控制一个全局不变量。

本题的关键公式是：

$$F=P_{current}\oplus K$$

它将随机棋盘状态、钥匙位置和 Alice 的唯一一次翻转操作连接成一个完全可靠的编码协议。
