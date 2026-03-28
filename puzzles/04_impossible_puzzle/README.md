# The Impossible Puzzle (Freudenthal's Puzzle)

This directory contains the mathematical deduction of the famous "Impossible Puzzle" in epistemic logic, along with an algorithmic solver built using Python set filtering.

## Problem Setup

There are two unknown integers x and y, such that $1 < x < y$ and $x + y \le 100$.
- Mr. Product (P): Only knows the product of these two numbers, $P = x \cdot y$.
- Mr. Sum (S): Only knows the sum of these two numbers, $S = x + y$.

Both are perfectly rational and extremely intelligent mathematicians. The following four-line conversation ensues:

1. P says: "I don't know what these two numbers are."
2. S says: "I already knew that you didn't know."
3. P says: "Now I know what these two numbers are!"
4. S says: "Now I know too!"

Objective: Deduce the unique values of x and y through these four statements.

## Deduction Process

We define the initial sample space as all pairs of numbers (x, y) that satisfy $1 < x < y$ and $x + y \le 100$.

### 1. P says "I don't know"
Logical Deduction: If the product P uniquely corresponds to one pair of numbers (i.e., the factorization of P has only one valid split that satisfies the conditions), P would immediately know x and y.
Space Collapse: Eliminate all pairs whose product P has only one valid factorization.

### 2. S says "I already knew that you didn't know"
Logical Deduction: S only knows the sum S. This statement means: among all pairs that sum up to S, not a single pair has a unique product. 
If the sum S could be split into the sum of two prime numbers (for example, according to Goldbach's conjecture, any even number greater than 2 can be), then S would not dare to make this statement, because the product P held by P might happen to be the product of those two primes.
Space Collapse: The sum S held by S must not be an even number, but an odd number, and S - 2 cannot be a prime number (because the product of the prime number 2 and the prime number S - 2 would definitively have a unique factorization). Through this step, we can exhaustively deduce that S can only be one of the following candidate numbers (e.g., 11, 17, 23, 27, 29, 35...). Eliminate all pairs where x + y is not in this candidate S set.

### 3. P says "Now I know"
Logical Deduction: After hearing S's statement, P also deduces the candidate S set mentioned above. P checks all possible factorizations of his confirmed product P. He discovers that among all the sums corresponding to these factorizations, there is exactly one sum that falls into this candidate S set.
Space Collapse: Eliminate all products P that have multiple sum possibilities in the candidate S set. At this point, P has locked onto the unique (x, y).

### 4. S says "Now I know too"
Logical Deduction: After hearing P's statement, S knows that P has found the unique solution through step 3. S checks all possible additive partitions of his confirmed sum S. He discovers that among these partitions, there is exactly one pair (x, y) that allows P to arrive at a unique solution in step 3 (after S and P have shared the candidate set $S$).
Space Collapse: Among the candidate sums S, find the S that possesses a uniquely surviving additive partition.

## Conclusion
After the deduction above, only one unique pair of numbers remains in the entire sample space:
x = 4, y = 13
At this point, S = 17, P = 52.

Q.E.D.