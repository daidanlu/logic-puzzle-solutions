# 俄罗斯卡牌问题与法诺平面协议

本文给出俄罗斯卡牌问题（Russian Cards Problem）的一个简洁组合数学证明。证明使用法诺平面构造一个公开通信协议，使 Bob 能唯一确定 Alice 的手牌，而 Eve 不能确定任何一张非自己手牌的归属。

---

## 1. 问题设定

共有 7 张牌：

$$V=\lbrace 0,1,2,3,4,5,6 \rbrace$$

三个人分别持有这些牌：

- Alice 持有 3 张牌；
- Bob 持有 3 张牌；
- Eve 持有 1 张牌。

假设真实发牌为：

$$A=\lbrace 0,1,2 \rbrace$$

$$B=\lbrace 3,4,6 \rbrace$$

$$E=\lbrace 5 \rbrace$$

Alice 希望通过一次公开喊话达到两个目标：

1. Bob 能够唯一确定 Alice 的真实手牌；
2. Eve 不能确定除自己手牌以外任何一张牌属于 Alice 还是 Bob。

这是一种不依赖计算困难性的安全通信。它的安全性来自组合结构，而不是来自大整数分解、椭圆曲线或其他现代密码学假设。

---

## 2. 候选集公告

Alice 公开宣布：她的手牌是下面 7 个三元组中的一个：

$$\mathcal{H}=
\lbrace
\lbrace 0,1,2 \rbrace,
\lbrace 0,3,4 \rbrace,
\lbrace 0,5,6 \rbrace,
\lbrace 1,3,5 \rbrace,
\lbrace 1,4,6 \rbrace,
\lbrace 2,3,6 \rbrace,
\lbrace 2,4,5 \rbrace
\rbrace$$

其中真实手牌是：

$$\lbrace 0,1,2 \rbrace$$

其余 6 个三元组都是烟雾弹。

上述 7 个三元组正是法诺平面的 7 条直线。它们满足两个关键性质：

1. 任意两个不同三元组恰好有一个公共元素；
2. 每一张牌恰好出现在 3 个三元组中。

这两个性质正是协议能够同时满足“Bob 可解”和“Eve 安全”的原因。

---

## 3. Bob 为什么能唯一确定 Alice 的手牌

Bob 知道自己的手牌是：

$$B=\lbrace 3,4,6 \rbrace$$

因为 Alice 不可能持有 Bob 已经持有的牌，所以 Bob 可以排除所有与自己手牌有交集的候选三元组。

首先，真实候选集与 Bob 的手牌没有交集：

$$\lbrace 0,1,2 \rbrace \cap \lbrace 3,4,6 \rbrace=\varnothing$$

其余每个候选集都与 Bob 的手牌有交集：

$$\lbrace 0,3,4 \rbrace \cap B=\lbrace 3,4 \rbrace$$

$$\lbrace 0,5,6 \rbrace \cap B=\lbrace 6 \rbrace$$

$$\lbrace 1,3,5 \rbrace \cap B=\lbrace 3 \rbrace$$

$$\lbrace 1,4,6 \rbrace \cap B=\lbrace 4,6 \rbrace$$

$$\lbrace 2,3,6 \rbrace \cap B=\lbrace 3,6 \rbrace$$

$$\lbrace 2,4,5 \rbrace \cap B=\lbrace 4 \rbrace$$

因此，在 Alice 公告的 7 个候选三元组中，唯一不与 Bob 的手牌冲突的是：

$$\lbrace 0,1,2 \rbrace$$

所以 Bob 可以唯一确定 Alice 的手牌。

---

## 4. Eve 为什么不能确定任何其他牌的归属

Eve 知道自己的手牌是：

$$E=\lbrace 5 \rbrace$$

因此，Eve 可以排除所有包含 5 的候选三元组：

$$\lbrace 0,5,6 \rbrace$$

$$\lbrace 1,3,5 \rbrace$$

$$\lbrace 2,4,5 \rbrace$$

从 Eve 的视角看，剩下的可能手牌为：

$$\mathcal{H}_E=
\lbrace
\lbrace 0,1,2 \rbrace,
\lbrace 0,3,4 \rbrace,
\lbrace 1,4,6 \rbrace,
\lbrace 2,3,6 \rbrace
\rbrace$$

现在考虑 Eve 没有持有的 6 张牌：

$$0,1,2,3,4,6$$

它们在剩下的 4 个候选三元组中出现次数如下：

| 牌 | 包含它的剩余候选三元组 | 出现次数 |
|---|---|---|
| 0 | $\lbrace 0,1,2 \rbrace$, $\lbrace 0,3,4 \rbrace$ | 2 |
| 1 | $\lbrace 0,1,2 \rbrace$, $\lbrace 1,4,6 \rbrace$ | 2 |
| 2 | $\lbrace 0,1,2 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |
| 3 | $\lbrace 0,3,4 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |
| 4 | $\lbrace 0,3,4 \rbrace$, $\lbrace 1,4,6 \rbrace$ | 2 |
| 6 | $\lbrace 1,4,6 \rbrace$, $\lbrace 2,3,6 \rbrace$ | 2 |

因此，对于任意一张 $x \ne 5$ 的牌，Eve 都看到两个可能世界使得 $x$ 在 Alice 手中，也看到两个可能世界使得 $x$ 不在 Alice 手中。

所以 Eve 无法确定任何一张非自己手牌的归属。

---

## 5. 抽象组合解释

这个协议的关键不在于 Alice 随便列出了 7 个候选集，而在于她列出的 7 个候选集构成了一个特殊的块设计：法诺平面。

因为法诺平面中任意两条直线恰好相交于一个点，所以 Alice 的真实手牌与任何一个假的候选三元组都恰好共享一张牌。于是每个假的候选三元组都包含两张不属于 Alice 的牌。

由于 Eve 只有一张牌，每个假的候选三元组不可能只靠 Eve 的一张牌来解释掉这两张非 Alice 的牌。因此，每个假的候选三元组都至少包含一张 Bob 的牌。Bob 看到自己的 3 张牌后，就可以排除所有假的候选集。

另一方面，因为法诺平面中每个点恰好出现在 3 条直线上，所以 Eve 的一张牌只会排除 3 个候选三元组。剩下 4 个候选三元组仍然保持平衡：每一张 Eve 未持有的牌都恰好出现 2 次。

这种平衡性使 Eve 无法对任何一张非自己手牌的归属作出确定判断。

---

## 6. 结论

法诺平面协议解决了这个版本的俄罗斯卡牌问题。

Alice 公开宣布 7 个可能手牌。Bob 使用自己的 3 张牌排除所有假的候选项，从而唯一恢复 Alice 的真实手牌。Eve 虽然也能用自己的一张牌排除一部分候选项，但剩余候选项仍然对每一张未知牌保持完全平衡。

最终结果是：

$$
\text{Bob 得到唯一信息，而 Eve 无法确定任何其他牌的归属。}
$$

这说明，有限几何与组合设计可以构造出信息论意义上的安全通信协议。

$$
\blacksquare
$$
