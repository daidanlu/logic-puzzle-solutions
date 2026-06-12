from itertools import product
from collections import deque


DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(seq):
    if max(seq, default=0) >= len(DIGITS):
        return " ".join(map(str, seq))
    return "".join(DIGITS[x] for x in seq)


def build_graph(k, n):
    if k <= 0 or n <= 0:
        raise ValueError("k and n must be positive integers.")

    m = n - 1
    vertices = list(product(range(k), repeat=m))
    graph = {v: [] for v in vertices}

    for v in vertices:
        for x in reversed(range(k)):
            nxt = v[1:] + (x,) if m else ()
            graph[v].append((nxt, x))

    return graph


def graph_stats(graph, k):
    indeg = {v: 0 for v in graph}
    rev = {v: [] for v in graph}

    for v, edges in graph.items():
        for nxt, _ in edges:
            indeg[nxt] += 1
            rev[nxt].append((v, None))

    balanced = all(len(graph[v]) == k and indeg[v] == k for v in graph)
    strong = reachable_count(graph) == len(graph) and reachable_count(rev) == len(graph)

    return {
        "vertices": len(graph),
        "edges": sum(len(edges) for edges in graph.values()),
        "balanced": balanced,
        "strongly_connected": strong,
    }


def reachable_count(graph):
    start = next(iter(graph))
    seen = {start}
    q = deque([start])

    while q:
        v = q.popleft()
        for edge in graph[v]:
            nxt = edge[0] if isinstance(edge, tuple) and len(edge) == 2 else edge
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)

    return len(seen)


def eulerian_labels(graph, start):
    graph = {v: edges[:] for v, edges in graph.items()}
    stack = [(start, None)]
    circuit = []

    while stack:
        v, label = stack[-1]
        if graph[v]:
            nxt, x = graph[v].pop()
            stack.append((nxt, x))
        else:
            circuit.append(stack.pop())

    circuit.reverse()
    return [label for _, label in circuit[1:]]


def de_bruijn_input(k, n):
    graph = build_graph(k, n)
    start = tuple(0 for _ in range(n - 1))
    labels = eulerian_labels(graph, start)
    return start + tuple(labels)


def verify_sequence(seq, k, n):
    windows = [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]
    all_passwords = set(product(range(k), repeat=n))

    return {
        "length": len(seq),
        "minimum_length": k ** n + n - 1,
        "naive_length": n * (k ** n),
        "windows": len(windows),
        "unique_windows": len(set(windows)),
        "covers_all": set(windows) == all_passwords,
        "exactly_once": len(windows) == len(set(windows)) == k ** n,
    }


def preview(seq, width=70):
    s = encode(seq)
    if len(s) <= 2 * width + 5:
        return s
    return f"{s[:width]} ... {s[-width:]}"


def run_demo(k, n):
    graph = build_graph(k, n)
    stats = graph_stats(graph, k)
    seq = de_bruijn_input(k, n)
    check = verify_sequence(seq, k, n)

    print("=" * 72)
    print(f"Demo: k={k}, n={n}")
    print(f"Vertices k^(n-1): {stats['vertices']}")
    print(f"Edges / passwords k^n: {stats['edges']}")
    print(f"In-degree = out-degree = k for every vertex: {stats['balanced']}")
    print(f"Strongly connected: {stats['strongly_connected']}")
    print()
    print(f"Generated input length: {check['length']}")
    print(f"Theoretical minimum: {check['minimum_length']}")
    print(f"Naive enumeration length: {check['naive_length']}")
    print(f"Sliding windows: {check['windows']}")
    print(f"Unique windows: {check['unique_windows']}")
    print(f"Covers every password exactly once: {check['covers_all'] and check['exactly_once']}")
    print()
    print("Input preview:")
    print(preview(seq))

    if not (stats["balanced"] and stats["strongly_connected"] and check["covers_all"] and check["exactly_once"]):
        raise RuntimeError("Verification failed.")


if __name__ == "__main__":
    run_demo(2, 3)
    run_demo(10, 4)
