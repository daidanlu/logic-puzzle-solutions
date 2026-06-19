from fractions import Fraction
from itertools import combinations
from math import gcd
from random import randint, seed

Point = tuple[int, int]
Line = tuple[int, int, int]


def normalize_line(a: int, b: int, c: int) -> Line:
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g

    if a < 0 or (a == 0 and b < 0) or (a == 0 and b == 0 and c < 0):
        a, b, c = -a, -b, -c

    return a, b, c


def line_from_points(p: Point, q: Point) -> Line:
    if p == q:
        raise ValueError("duplicate points cannot define a line")

    x1, y1 = p
    x2, y2 = q

    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return normalize_line(a, b, c)


def on_line(p: Point, line: Line) -> bool:
    x, y = p
    a, b, c = line
    return a * x + b * y + c == 0


def point_line_distance_squared(p: Point, line: Line) -> Fraction:
    x, y = p
    a, b, c = line
    numerator = (a * x + b * y + c) ** 2
    denominator = a * a + b * b
    return Fraction(numerator, denominator)


def validate_points(points: list[Point]) -> None:
    if len(points) < 3:
        raise ValueError("at least 3 points are required")

    if len(set(points)) != len(points):
        raise ValueError("points must be distinct")


def all_lines(points: list[Point]) -> list[Line]:
    validate_points(points)
    return sorted({line_from_points(p, q) for p, q in combinations(points, 2)})


def incident_points(points: list[Point], line: Line) -> list[Point]:
    return [p for p in points if on_line(p, line)]


def is_non_collinear(points: list[Point]) -> bool:
    return len(all_lines(points)) > 1


def ordinary_lines(points: list[Point]) -> list[tuple[Line, list[Point]]]:
    result = []

    for line in all_lines(points):
        hits = incident_points(points, line)
        if len(hits) == 2:
            result.append((line, hits))

    return result


def extremal_point_line_pair(points: list[Point]) -> tuple[Point, Line, Fraction]:
    best_point = None
    best_line = None
    best_distance = None

    for line in all_lines(points):
        for p in points:
            if on_line(p, line):
                continue

            distance = point_line_distance_squared(p, line)

            if best_distance is None or distance < best_distance:
                best_point = p
                best_line = line
                best_distance = distance

    if best_point is None or best_line is None or best_distance is None:
        raise ValueError("no valid point-line pair found")

    return best_point, best_line, best_distance


def verify_sylvester_gallai(points: list[Point]) -> None:
    validate_points(points)

    if not is_non_collinear(points):
        raise ValueError("the point set is collinear")

    ordinary = ordinary_lines(points)
    p0, l0, d0 = extremal_point_line_pair(points)
    hits = incident_points(points, l0)

    print("=" * 72)
    print(f"Points: {points}")
    print(f"Number of points: {len(points)}")
    print(f"Number of generated lines: {len(all_lines(points))}")
    print(f"Number of ordinary lines: {len(ordinary)}")
    print()
    print(f"Extremal point P0: {p0}")
    print(f"Extremal line L0: {l0}")
    print(f"Points on L0: {hits}")
    print(f"Squared distance d(P0, L0)^2: {d0}")
    print(f"L0 is ordinary: {len(hits) == 2}")

    if not ordinary:
        raise AssertionError("no ordinary line found")

    if len(hits) != 2:
        raise AssertionError("the extremal line is not ordinary")

    print("Verification passed.")


def random_point_set(size: int, low: int = -20, high: int = 20) -> list[Point]:
    points: set[Point] = set()

    while len(points) < size:
        points.add((randint(low, high), randint(low, high)))

    return list(points)


def verify_random(samples: int = 1000, size: int = 8) -> None:
    seed(0)
    checked = 0

    while checked < samples:
        points = random_point_set(size)

        if not is_non_collinear(points):
            continue

        ordinary = ordinary_lines(points)
        p0, l0, _ = extremal_point_line_pair(points)
        hits = incident_points(points, l0)

        if not ordinary:
            raise AssertionError(f"No ordinary line found: {points}")

        if len(hits) != 2:
            raise AssertionError(
                f"Extremal line is not ordinary: points={points}, P0={p0}, L0={l0}, hits={hits}"
            )

        checked += 1

    print(f"Random verification passed: {checked} non-collinear point sets.")


if __name__ == "__main__":
    demo_points = [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 2),
        (3, 1),
        (2, 3),
    ]

    verify_sylvester_gallai(demo_points)

    print()
    verify_random(samples=1000, size=8)
