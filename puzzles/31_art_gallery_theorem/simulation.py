"""
The theorem says that every simple polygon with n vertices can be guarded by
floor(n / 3) stationary guards. This script:

    simple polygon -> ear-clipping triangulation -> 3-coloring ->
    choose the smallest color class as guard positions -> verify coverage

This is a finite simulation that checks specific input polygons and demonstrates the constructive logic used in the proof.

To test specific polygon, edit CUSTOM_POLYGON near the bottom of the file.
Coordinates should be listed in boundary order, either clockwise or
counterclockwise, without repeated final vertex.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, isclose
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]

EPS = 1e-9
COLORS = ("red", "green", "blue")


class GeometryError(ValueError):
    """Raised when the input polygon is degenerate or cannot be triangulated."""


@dataclass(frozen=True)
class GuardingResult:
    name: str
    vertices: List[Point]
    triangles: List[Triangle]
    coloring: Dict[int, str]
    color_classes: Dict[str, List[int]]
    guard_color: str
    guards: List[int]
    graph_edges: Set[Tuple[int, int]]


def polygon_area(poly: Sequence[Point]) -> float:
    """Signed polygon area. Positive means counterclockwise order."""
    area2 = 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        area2 += x1 * y2 - x2 * y1
    return area2 / 2.0


def cross(a: Point, b: Point, c: Point) -> float:
    """2D cross product of vectors AB and AC."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_in_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """
    Return True if p is inside or on the boundary of triangle abc.

    The boundary-inclusive test makes ear clipping conservative: if another
    vertex lies on a candidate ear, we do not clip that ear.
    """
    c1 = cross(a, b, p)
    c2 = cross(b, c, p)
    c3 = cross(c, a, p)
    has_neg = c1 < -EPS or c2 < -EPS or c3 < -EPS
    has_pos = c1 > EPS or c2 > EPS or c3 > EPS
    return not (has_neg and has_pos)


def remove_repeated_last_vertex(poly: Sequence[Point]) -> List[Point]:
    """Accept either [(...), first] or no repeated final vertex."""
    vertices = list(poly)
    if len(vertices) >= 2 and vertices[0] == vertices[-1]:
        vertices.pop()
    return vertices


def ensure_counterclockwise(poly: Sequence[Point]) -> Tuple[List[Point], List[int]]:
    """
    Return vertices in counterclockwise order and a parallel list of original IDs.
    """
    vertices = remove_repeated_last_vertex(poly)
    if len(vertices) < 3:
        raise GeometryError("A polygon needs at least three vertices.")

    ids = list(range(len(vertices)))
    area = polygon_area(vertices)
    if abs(area) < EPS:
        raise GeometryError("The polygon has zero area or is degenerate.")
    if area < 0:
        vertices.reverse()
        ids.reverse()
    return vertices, ids


def ear_clip_triangulation(poly: Sequence[Point]) -> Tuple[List[Point], List[Triangle]]:
    """
    Triangulate a simple polygon using the standard ear-clipping algorithm.

    Returns vertices in the original input order and triangles as original
    vertex indices.  For clean simple polygons this should return exactly n-2
    triangles.
    """
    original_vertices = remove_repeated_last_vertex(poly)
    ccw_vertices, ccw_to_original = ensure_counterclockwise(poly)

    # active stores indices into ccw_vertices.  ccw_to_original maps them back
    # to the user's original vertex numbering.
    active = list(range(len(ccw_vertices)))
    triangles_ccw: List[Tuple[int, int, int]] = []

    safety_limit = len(active) * len(active) + 10
    scans = 0

    while len(active) > 3:
        clipped = False
        m = len(active)

        for pos in range(m):
            prev_i = active[(pos - 1) % m]
            curr_i = active[pos]
            next_i = active[(pos + 1) % m]

            a = ccw_vertices[prev_i]
            b = ccw_vertices[curr_i]
            c = ccw_vertices[next_i]

            # In counterclockwise order, an ear tip must be locally convex.
            if cross(a, b, c) <= EPS:
                continue

            # No other active vertex may lie inside the candidate ear triangle.
            contains_other_vertex = False
            for other_i in active:
                if other_i in (prev_i, curr_i, next_i):
                    continue
                if point_in_triangle(ccw_vertices[other_i], a, b, c):
                    contains_other_vertex = True
                    break

            if contains_other_vertex:
                continue

            triangles_ccw.append((prev_i, curr_i, next_i))
            del active[pos]
            clipped = True
            break

        scans += 1
        if not clipped or scans > safety_limit:
            raise GeometryError(
                "Ear clipping failed. Check that the polygon is simple, "
                "non-self-intersecting, and has no problematic duplicate vertices."
            )

    triangles_ccw.append(tuple(active))  # type: ignore[arg-type]

    triangles_original: List[Triangle] = []
    for tri in triangles_ccw:
        triangles_original.append(tuple(ccw_to_original[i] for i in tri))  # type: ignore[arg-type]

    return original_vertices, triangles_original


def build_triangulation_graph(
    n: int, triangles: Iterable[Triangle]
) -> Set[Tuple[int, int]]:
    """Build graph edges from all triangle sides."""
    edges: Set[Tuple[int, int]] = set()
    for tri in triangles:
        a, b, c = tri
        for u, v in ((a, b), (b, c), (c, a)):
            if not (0 <= u < n and 0 <= v < n):
                raise GeometryError("Triangle contains an invalid vertex index.")
            edges.add((min(u, v), max(u, v)))
    return edges


def build_adjacency(n: int, edges: Iterable[Tuple[int, int]]) -> Dict[int, Set[int]]:
    adjacency = {i: set() for i in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def three_color_graph(n: int, edges: Set[Tuple[int, int]]) -> Dict[int, str]:
    """
    Find a proper 3-coloring by backtracking.

    Fisk's proof guarantees that triangulated simple polygons are 3-colorable.The backtracking search makes the construction explicit for the demo input.
    """
    adjacency = build_adjacency(n, edges)
    order = sorted(range(n), key=lambda v: len(adjacency[v]), reverse=True)
    assignment: Dict[int, str] = {}

    def search(k: int) -> bool:
        if k == len(order):
            return True
        vertex = order[k]
        forbidden = {
            assignment[neighbor]
            for neighbor in adjacency[vertex]
            if neighbor in assignment
        }
        for color in COLORS:
            if color in forbidden:
                continue
            assignment[vertex] = color
            if search(k + 1):
                return True
            del assignment[vertex]
        return False

    if not search(0):
        raise GeometryError(
            "No 3-coloring found; input may not be a valid triangulated simple polygon."
        )

    return dict(sorted(assignment.items()))


def color_classes_from_coloring(coloring: Dict[int, str]) -> Dict[str, List[int]]:
    classes = {color: [] for color in COLORS}
    for vertex, color in coloring.items():
        classes[color].append(vertex)
    return classes


def choose_smallest_color_class(classes: Dict[str, List[int]]) -> Tuple[str, List[int]]:
    """Choose the smallest color class; ties are resolved by color order."""
    color = min(COLORS, key=lambda c: (len(classes[c]), COLORS.index(c)))
    return color, classes[color]


def verify_triangle_coloring(
    triangles: Iterable[Triangle], coloring: Dict[int, str]
) -> bool:
    """Every triangle should contain one red, one green, and one blue vertex."""
    return all({coloring[v] for v in tri} == set(COLORS) for tri in triangles)


def verify_guarded_triangles(triangles: Iterable[Triangle], guards: Set[int]) -> bool:
    """
    Coverage check used in the proof: every triangle has at least one guarded
    vertex. Since every triangle is convex, this covers the whole polygon.
    """
    return all(any(v in guards for v in tri) for tri in triangles)


def solve_gallery(name: str, polygon: Sequence[Point]) -> GuardingResult:
    vertices, triangles = ear_clip_triangulation(polygon)
    n = len(vertices)
    edges = build_triangulation_graph(n, triangles)
    coloring = three_color_graph(n, edges)
    classes = color_classes_from_coloring(coloring)
    guard_color, guards = choose_smallest_color_class(classes)

    if len(triangles) != n - 2:
        raise GeometryError(f"Expected n-2={n-2} triangles, got {len(triangles)}.")
    if not verify_triangle_coloring(triangles, coloring):
        raise GeometryError("The coloring is not valid on every triangle.")
    if not verify_guarded_triangles(triangles, set(guards)):
        raise GeometryError("At least one triangle has no guard.")

    return GuardingResult(
        name=name,
        vertices=vertices,
        triangles=triangles,
        coloring=coloring,
        color_classes=classes,
        guard_color=guard_color,
        guards=guards,
        graph_edges=edges,
    )


def print_report(result: GuardingResult) -> None:
    n = len(result.vertices)
    bound = floor(n / 3)
    guard_count = len(result.guards)

    print("=" * 72)
    print(result.name)
    print("=" * 72)
    print(f"Vertices n: {n}")
    print(f"Art Gallery bound floor(n/3): {bound}")
    print(f"Triangulation produced: {len(result.triangles)} triangle(s)")
    print()

    print("Vertices:")
    for i, point in enumerate(result.vertices):
        print(f"  v{i}: {point}")
    print()

    print("Triangles from ear clipping, using vertex indices:")
    for i, tri in enumerate(result.triangles, start=1):
        colors = tuple(result.coloring[v] for v in tri)
        guarded = any(v in set(result.guards) for v in tri)
        print(f"  T{i:02d}: {tri}, colors={colors}, guarded={guarded}")
    print()

    print("3-coloring:")
    for vertex, color in result.coloring.items():
        print(f"  v{vertex}: {color}")
    print()

    print("Color classes:")
    for color in COLORS:
        vertices = result.color_classes[color]
        print(f"  {color:5s}: size={len(vertices)}, vertices={vertices}")
    print()

    print(f"Chosen guard color class: {result.guard_color}")
    print(f"Guard vertices: {result.guards}")
    print(f"Guard count: {guard_count}")
    print(f"Guard count <= floor(n/3): {guard_count <= bound}")
    print(
        f"Every triangle has all three colors: {verify_triangle_coloring(result.triangles, result.coloring)}"
    )
    print(
        f"Every triangle has a guard: {verify_guarded_triangles(result.triangles, set(result.guards))}"
    )
    print(
        "Conclusion: the whole polygon is covered because it is the union of its guarded triangles."
    )
    print()


DEMO_POLYGONS: Dict[str, List[Point]] = {
    # n = 4, so the theorem guarantees at most 1 guard.
    "Demo 1: convex quadrilateral": [
        (0, 0),
        (4, 0),
        (5, 2),
        (0, 3),
    ],
    # A simple orthogonal gallery with two inward notches.
    "Demo 2: concave orthogonal gallery": [
        (0, 0),
        (6, 0),
        (6, 2),
        (4, 2),
        (4, 4),
        (6, 4),
        (6, 6),
        (0, 6),
        (0, 4),
        (2, 4),
        (2, 2),
        (0, 2),
    ],
    # A comb-like polygon with several narrow pockets.
    "Demo 3: comb-shaped gallery": [
        (0, 0),
        (9, 0),
        (9, 3),
        (8, 3),
        (8, 1),
        (7, 1),
        (7, 3),
        (6, 3),
        (6, 1),
        (5, 1),
        (5, 3),
        (4, 3),
        (4, 1),
        (3, 1),
        (3, 3),
        (2, 3),
        (2, 1),
        (1, 1),
        (1, 3),
        (0, 3),
    ],
}


# Edit this list to test the chosen polygon. Otherwise, leave it as None to run demos.
CUSTOM_POLYGON: Optional[List[Point]] = None
# Example:
# CUSTOM_POLYGON = [(0, 0), (5, 0), (5, 2), (3, 1), (2, 4), (0, 3)]


def main() -> None:
    for name, polygon in DEMO_POLYGONS.items():
        result = solve_gallery(name, polygon)
        print_report(result)

    if CUSTOM_POLYGON is not None:
        result = solve_gallery("Custom polygon", CUSTOM_POLYGON)
        print_report(result)


if __name__ == "__main__":
    main()
