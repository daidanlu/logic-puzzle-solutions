import random
from itertools import product


def conway_counter(a):
    # Build Bob's countersequence.
    flip = {"H": "T", "T": "H"}
    return flip[a[1]] + a[0] + a[1]


def play(a, b):
    # Toss until one pattern appears.
    stream = ""

    while True:
        stream += random.choice("HT")
        last = stream[-3:]

        if last == a:
            return "Alice"
        if last == b:
            return "Bob"


def simulate(a, trials=100000):
    # Estimate Bob's win rate.
    b = conway_counter(a)
    bob_wins = 0

    for _ in range(trials):
        if play(a, b) == "Bob":
            bob_wins += 1

    return b, bob_wins / trials


patterns = ["".join(p) for p in product("HT", repeat=3)]

for a in patterns:
    b, rate = simulate(a)
    print(f"Alice: {a}, Bob: {b}, Bob win rate: {rate:.4f}")
