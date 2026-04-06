# The Dining Cryptographers Problem (就餐密码学家问题)

本目录给出了就餐密码学家问题的数学推导，说明如何在去中心化环境下实现匿名广播。

## 1. 系统设定与变量定义

三位密码学家 A, B, C 围绕餐桌就座。账单已被支付，支付者要么是其中一人，要么是外部机构（NSA）。

目标是判断“是否有内部人员支付”，同时在内部人员支付的情况下不泄露具体身份。

定义支付状态向量：

$$
P = (P_A, P_B, P_C)
$$

若第 i 人支付，则：

$$
P_i = 1
$$

否则：

$$
P_i = 0
$$

由于最多只有一人支付：

$$
\sum P_i \in \{0, 1\}
$$

初始化阶段，每对相邻参与者在桌下共享一枚公平硬币。

记：

$$
c_{AB} \in \{0,1\}
$$

$$
c_{BC} \in \{0,1\}
$$

$$
c_{CA} \in \{0,1\}
$$

## 2. 局部编码与广播

每个参与者根据两枚可见硬币及自身支付状态计算广播值：

$$
M_A = c_{AB} \oplus c_{CA} \oplus P_A
$$

$$
M_B = c_{BC} \oplus c_{AB} \oplus P_B
$$

$$
M_C = c_{CA} \oplus c_{BC} \oplus P_C
$$

随后公开广播各自的 $M_i$。

## 3. 正确性证明

所有参与者计算：

$$
S = M_A \oplus M_B \oplus M_C
$$

展开：

$$
S = (c_{AB} \oplus c_{CA} \oplus P_A)
\oplus (c_{BC} \oplus c_{AB} \oplus P_B)
\oplus (c_{CA} \oplus c_{BC} \oplus P_C)
$$

整理：

$$
S = (c_{AB} \oplus c_{AB})
\oplus (c_{BC} \oplus c_{BC})
\oplus (c_{CA} \oplus c_{CA})
\oplus (P_A \oplus P_B \oplus P_C)
$$

由于：

$$
x \oplus x = 0
$$

得到：

$$
S = P_A \oplus P_B \oplus P_C
$$

因此：

- 若 NSA 支付，则：

$$
P_A = P_B = P_C = 0
$$

$$
S = 0
$$

- 若某一内部人员支付，则：

$$
\exists i: P_i = 1
$$

$$
S = 1
$$

该协议能够判断是否为内部支付。

## 4. 隐匿性证明

考虑观察者 C，且：

$$
P_C = 0,\quad S = 1
$$

C 的信息为：

$$
\{c_{CA}, c_{BC}, M_A, M_B, M_C\}
$$

未知变量为：

$$
c_{AB}
$$

### 情况 1：A 支付

$$
P_A = 1,\quad P_B = 0
$$

$$
M_A = c_{AB} \oplus c_{CA} \oplus 1
$$

$$
M_B = c_{AB} \oplus c_{BC}
$$

### 情况 2：B 支付

$$
P_A = 0,\quad P_B = 1
$$

$$
M_A = c_{AB} \oplus c_{CA}
$$

$$
M_B = c_{AB} \oplus c_{BC} \oplus 1
$$

由于：

$$
P(c_{AB} = 0) = P(c_{AB} = 1) = 0.5
$$

对于任意观测值：

$$
(M_A, M_B) = (x, y)
$$

两种情况对应的 $c_{AB}$ 取值互为相反，但概率相同，因此：

$$
P(M_A, M_B \mid P_A = 1) = P(M_A, M_B \mid P_B = 1)
$$

观察者无法区分两种情况。

该协议满足完美保密。

Q.E.D.