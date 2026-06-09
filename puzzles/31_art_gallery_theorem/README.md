# The Art Gallery Theorem

## Mathematical Modeling

Suppose an art gallery has the shape of a simple polygon with $n$ vertices in the plane.

A polygon is simple if its boundary is a closed polygonal chain that does not cross itself. The polygon has no holes, but it may be non-convex and may contain many reflex vertices.

We want to place stationary guards inside the polygon or on its boundary. The visibility rules are:

1. Each guard has $360^\circ$ vision.
2. A guard can see a point $p$ if and only if the line segment from the guard to $p$ lies entirely inside the polygon or on its boundary.
3. A line of sight cannot pass through a wall.

The question is:

$$\text{For every simple polygon with } n \text{ vertices, how many guards are always sufficient?}$$

The Art Gallery Theorem states that

$$\left\lfloor \frac{n}{3} \right\rfloor$$

guards are always sufficient. Moreover, this number is sometimes necessary.

---

## Theorem

For every simple polygon with $n$ vertices, at most

$$\left\lfloor \frac{n}{3} \right\rfloor$$

guards are sufficient to cover the entire polygon.

Equivalently:

$$\text{every simple } n\text{-gon can be guarded by } \left\lfloor \frac{n}{3} \right\rfloor \text{ guards}$$

This bound is tight in the worst case.

---

## Proof Overview

Fisk's proof converts a continuous geometric visibility problem into a discrete graph-theoretic problem. The main idea is:

$$\text{triangulation} \to \text{3-coloring} \to \text{choose the smallest color class}$$

---

## Step 1: Triangulation

Every simple polygon with $n$ vertices can be decomposed into

$$n-2$$

triangles by adding non-crossing internal diagonals.

This triangulation uses only the original vertices of the polygon and introduces no new vertices. After the triangulation, the polygon is the union of these triangles.

The key geometric fact is that every triangle is convex. Therefore, if a guard is placed at one vertex of a triangle, then the guard can see every point inside that triangle.

Indeed, for a triangle vertex $v$ and any point $p$ inside the triangle, the segment $vp$ lies completely inside the triangle. Since the triangle itself lies inside the original polygon, this line of sight does not cross any wall.

Thus, if every triangle has at least one guarded vertex, then the whole polygon is guarded.

---

## Step 2: 3-Coloring the Triangulation Graph

View the triangulated polygon as a planar graph:

- the vertices are the $n$ original polygon vertices;
- the edges are the polygon boundary edges together with the added diagonals.

We need to prove that this graph can always be colored with three colors, say red, green, and blue, so that adjacent vertices receive different colors.

Since each face of the triangulation is a triangle and the three vertices of a triangle are pairwise adjacent, every triangle must contain one red vertex, one green vertex, and one blue vertex in any proper 3-coloring.

It remains to prove that such a 3-coloring always exists.

---

## Inductive Proof of 3-Colorability

When $n=3$, the polygon itself is a triangle. We can color its three vertices red, green, and blue.

Now assume that every triangulated simple polygon with $n-1$ vertices can be properly 3-colored.

Consider a triangulated simple polygon with $n$ vertices.

Define the dual graph of the triangulation as follows:

- each triangle becomes a node in the dual graph;
- two dual nodes are connected if the corresponding triangles share an internal diagonal.

For a triangulation of a simple polygon, this dual graph is a tree. The reason is:

1. The triangulation has $n-2$ triangles, so the dual graph has $n-2$ nodes.
2. The triangulation has $n-3$ internal diagonals, and each internal diagonal corresponds to exactly one adjacency between two triangles. Hence the dual graph has $n-3$ edges.
3. The triangulated region is connected, so the dual graph is connected.
4. A connected graph with $m$ nodes and $m-1$ edges is a tree.

Therefore:

$$\text{connected dual graph with } (n-2) \text{ nodes and } (n-3) \text{ edges} \implies \text{tree}$$

Every tree has a leaf. In the triangulation, a leaf of the dual graph corresponds to a leaf triangle. This triangle shares exactly one internal diagonal with the rest of the triangulation, and its other two edges lie on the polygon boundary. Such a triangle is often called an ear.

Let the vertices of this leaf triangle be $a,b,v$, where $v$ is the ear tip. Remove the ear tip $v$ and the two boundary edges incident to it. The remaining region is a simple polygon with $n-1$ vertices, and it inherits the remaining triangulation.

By the induction hypothesis, the remaining $n-1$ vertices can be properly 3-colored. The vertices $a$ and $b$ are still adjacent, so they have different colors. Therefore, exactly one of the three colors is not used by $a$ and $b$. Assign this remaining color to $v$.

Now the triangle $a,b,v$ has three distinct colors, and the coloring of all other triangles remains valid. Hence the original triangulated $n$-gon is also 3-colorable.

By induction, every triangulation of a simple polygon is 3-colorable, and every triangle has exactly one vertex of each color.

---

## Step 3: Choosing the Smallest Color Class

After the 3-coloring, the $n$ polygon vertices are partitioned into three disjoint color classes:

$$R,\quad G,\quad B$$

They satisfy:

$$|R|+|G|+|B|=n$$

By the pigeonhole principle, at least one of these three sets has size at most the average:

$$\min(|R|,|G|,|B|) \le \left\lfloor \frac{n}{3} \right\rfloor$$

Choose the smallest color class. Suppose it is the red class $R$. Place one guard at every red vertex.

---

## Step 4: Coverage Proof

Every triangle in the triangulation has exactly one red vertex. Therefore, after placing guards at all red vertices, every triangle has a guard at one of its vertices.

Since every triangle is convex, a guard placed at a vertex of a triangle can see every point inside that triangle.

The original polygon is exactly the union of all triangles in the triangulation:

$$P = T_1 \cup T_2 \cup \cdots \cup T_{n-2}$$

Every triangle is covered, so the entire polygon is covered.

Therefore, every simple polygon with $n$ vertices can be guarded by at most

$$\left\lfloor \frac{n}{3} \right\rfloor$$

guards.

---

## Tightness

The upper bound is not only sufficient; it is also best possible in the worst case.

For every positive integer $k$, one can construct a comb-shaped polygon with $k$ narrow pockets. Each pocket contains a deep point that can only be seen by a guard placed near that pocket. If the pockets are made sufficiently deep and narrow, and if they are separated by walls, then no single guard can see the deep points of two different pockets.

Therefore, such a polygon requires at least $k$ guards.

When the number of vertices is approximately $3k$, this gives:

$$k = \left\lfloor \frac{n}{3} \right\rfloor$$

Thus, in the worst case, the number of necessary guards can be exactly

$$\left\lfloor \frac{n}{3} \right\rfloor$$

Hence the Art Gallery Theorem gives a tight worst-case bound:

$$\left\lfloor \frac{n}{3} \right\rfloor \text{ guards are sometimes necessary and always sufficient}$$

---

## Conclusion

The Art Gallery Theorem states that:

$$\text{Every simple } n\text{-gon can be guarded by } \left\lfloor \frac{n}{3} \right\rfloor \text{ guards}.$$

Fisk's proof works by:

1. triangulating the simple polygon;
2. proving that the triangulation graph is 3-colorable;
3. choosing the smallest color class as the guard locations.

The proof does not rely on calculus. It uses triangulation, graph coloring, induction, and the pigeonhole principle.

$$\blacksquare$$
