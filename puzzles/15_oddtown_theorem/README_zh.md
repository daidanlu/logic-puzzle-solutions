# 奇数镇定理的线性代数证明

本文给出奇数镇定理（Oddtown Theorem）的一个简洁线性代数证明。

---

## 1. 问题设定

设一个小镇有 $N$ 名居民。现在有 $M$ 个不同的俱乐部，记为：

$$C_1, C_2, \dots, C_M$$

这些俱乐部满足以下两个条件：

1. 每个俱乐部的人数都是奇数；
2. 任意两个不同俱乐部的共同成员数都是偶数。

问题是：在这些条件下，最多能有多少个俱乐部？

奇数镇定理说明：

$$M \le N$$

也就是说，满足上述条件的俱乐部数量不可能超过居民数量。

---

## 2. 向量表示

对每个俱乐部 $C_i$，定义它的关联向量：

$$\mathbf{v}_i=(x_1,x_2,\dots,x_N) \in \mathbb{F}_2^N$$

其中：

- 若第 $k$ 名居民属于 $C_i$，则 $x_k=1$；
- 若第 $k$ 名居民不属于 $C_i$，则 $x_k=0$。

这里所有计算都在有限域 $\mathbb{F}_2$ 中进行，也就是只关心奇偶性。

---

## 3. 条件的代数翻译

首先，俱乐部 $C_i$ 的人数模 $2$ 后等于向量自身的点积：

$$\mathbf{v}_i \cdot \mathbf{v}_i = |C_i| \pmod 2$$

因为每个俱乐部的人数都是奇数，所以：

$$\mathbf{v}_i \cdot \mathbf{v}_i = 1$$

其次，两个不同俱乐部 $C_i$ 和 $C_j$ 的共同成员数模 $2$ 后等于两个关联向量的点积：

$$\mathbf{v}_i \cdot \mathbf{v}_j = |C_i \cap C_j| \pmod 2$$

因为任意两个不同俱乐部的交集大小都是偶数，所以当 $i \ne j$ 时：

$$\mathbf{v}_i \cdot \mathbf{v}_j = 0$$

因此，这些向量满足：

$$\mathbf{v}_i \cdot \mathbf{v}_j =
\begin{cases}
1, & i=j,\\
0, & i \ne j.
\end{cases}$$

---

## 4. 构造关联矩阵

将 $M$ 个关联向量作为行向量，构造一个 $M \times N$ 矩阵：

$$A=
\begin{pmatrix}
\mathbf{v}_1 \\
\mathbf{v}_2 \\
\vdots \\
\mathbf{v}_M
\end{pmatrix}$$

考虑矩阵乘积 $AA^T$。它是一个 $M \times M$ 矩阵，并且第 $i$ 行第 $j$ 列的元素为：

$$\left(AA^T\right)_{ij}=\mathbf{v}_i \cdot \mathbf{v}_j$$

由上一节得到的点积关系可知：

$$AA^T=I_M$$

其中 $I_M$ 是 $M \times M$ 的单位矩阵。

---

## 5. 秩的不等式

因为 $AA^T=I_M$，所以：

$$\operatorname{rank}(AA^T)=\operatorname{rank}(I_M)=M$$

另一方面，矩阵乘积的秩不超过其中任一因子的秩，因此：

$$\operatorname{rank}(AA^T) \le \operatorname{rank}(A)$$

而 $A$ 是一个 $M \times N$ 矩阵，所以它的秩不超过列数 $N$：

$$\operatorname{rank}(A) \le N$$

将这些关系合并，得到：

$$M=\operatorname{rank}(I_M)=\operatorname{rank}(AA^T) \le \operatorname{rank}(A) \le N$$

因此：

$$M \le N$$

$$\blacksquare$$

---

## 6. 结论

奇数镇定理说明，在 $N$ 名居民组成的集合上，如果每个俱乐部大小为奇数，并且任意两个不同俱乐部的交集大小为偶数，那么俱乐部总数最多为 $N$。

这个证明的关键是把俱乐部看作 $\mathbb{F}_2^N$ 中的向量。题目中的奇偶条件转化为点积条件，而这些点积条件进一步说明关联矩阵满足：

$$AA^T=I_M$$

于是，秩的不等式直接给出：

$$M \le N$$

这说明该组合问题可以通过有限域上的线性代数自然解决。
