---
title: "On Spheres, Shadows, and Certainty"
date: 2025-07-07
tags: ["math", "essay"]
---

A good mathematical puzzle often begins not with a question, but with a statement—one so elegant it feels both obvious and impossible. For me, this moment arrived during a commute, watching a 3Blue1Brown video featuring Terence Tao[^1]. At one point, a theorem was presented (somewhat casually): *if every possible 2D projection of a convex 3D body is a perfect disk, that body must be a sphere.*

[^1]: I highly encourage you to watch the video that sparked this inquiry: [Terence Tao on measuring the cosmos | The Distance Ladder Part 1](https://www.youtube.com/watch?v=YdOXS_9_P4U).

We see it with balls and flashlights, but how can we be certain that the shadow of a sphere is *always* a perfect disk? Not just for a sphere at the origin, or a shadow on a horizontal plane, but for *any* sphere and *any* plane?

Can we prove, with rigorous certainty, that the orthogonal projection of a sphere onto a plane is always a disk? I set out to answer it for myself, in hot pursuit of two distinct mathematical paths.

## A Crucial Distinction: Intersection vs. Projection

Before diving into a proof, it's essential to distinguish between two related concepts:

*   **Intersection**: This is the one-dimensional *slice* created when a plane cuts through a sphere. It is the curve where the two surfaces meet.

*   **Projection**: This is the two-dimensional *shadow* the sphere casts on a plane from a light source at an infinite distance, where all the incident light rays are parallel and perpendicular to the plane[^2].

[^2]: This "infinitely far" condition is crucial. A nearby light source would cast a shadow that is a different conic section—typically an ellipse. The assumption of parallel rays is the basis for an *orthographic* projection.

Understanding the shape of the slice is the logical first step. If we can define the intersection, we can understand the projection.

## The Vector Algebra Approach

I wanted to sidestep purely intuitive "it's symmetric" arguments and construct a proof that holds for a plane of any orientation. The language of vector algebra is perfectly suited for this task.

### The Setup

We can define our objects with two simple conditions:

1.  **The Sphere**: A sphere centered at the origin is the set of all points $P$ in 3D space whose distance from the origin is a constant radius $r$. In vector terms:
    $$
    |P|^2 = P \cdot P = r^2
    $$
2.  **The Plane**: An arbitrary plane[^3] passing through the origin is the set of all points $P$ whose position vectors are orthogonal to a fixed unit normal vector $n$. The condition is:
    $$
    P \cdot n = 0
    $$

[^3]: This proof assumes the plane passes through the sphere's center. For a non-central plane at a distance $d$ from the origin, the intersection is still a circle, but with a smaller radius of $\sqrt{r^2 - d^2}$. Remarkably, the projection's shadow remains a disk of radius $r$.

The intersection is simply the set of all points $P$ that satisfy both conditions simultaneously.

### Building a Coordinate System in the Plane

To analyze the shape of the intersection, we need a coordinate system that lies *within* the arbitrary plane. We can construct one using two perpendicular unit vectors, $u$ and $v$, that span the plane.

*   Let $u$ be any unit vector orthogonal to $n$.

*   Let $v$ be the cross product $v = n \times u$.

This guarantees $v$ is a unit vector orthogonal to both $n$ and $u$. Since both $u$ and $v$ are orthogonal to the plane's normal $n$, they form a basis for the plane. Any point $P$ in the plane can be written as a combination of these vectors:
$$
P = au + bv
$$
where $(a, b)$ are the 2D coordinates of the point within the plane's own coordinate system.

### The Final Step

Now, we enforce the sphere condition, $|P|^2 = r^2$, on our point in the plane:
$$
|au+bv|^2 = r^2
$$
$$
(au+bv) \cdot (au+bv) = r^2
$$
Expanding the dot product yields:
$$
a^2(u \cdot u) + 2ab(u \cdot v) + b^2(v \cdot v) = r^2
$$
By our construction, $u$ and $v$ are orthonormal, meaning:
$$
u \cdot u = |u|^2 = 1
$$
$$
v \cdot v = |v|^2 = 1
$$
$$
u \cdot v = 0
$$

Substituting these values gives us the simple result:
$$
a^2(1) + 2ab(0) + b^2(1) = r^2
$$
$$
a^2 + b^2 = r^2
$$
This is the unmistakable equation of a circle of radius $r$. We have proven that the intersection of a sphere with any central plane is a perfect circle.

## From Slice to Shadow: Proving the Projection

With the geometry of the slice confirmed, we can now tackle the shadow itself.

### The Projection Formula

The orthogonal projection of any vector $P$ from the sphere's surface onto the plane is found by subtracting the component of $P$ that is parallel to the normal vector $n$:
$$
P_{\text{proj}} = P - (P \cdot n)n
$$
We want to find the shape traced by $P_{\text{proj}}$ as $P$ moves over the entire sphere. We can do this by calculating the squared distance of any projected point from the origin:
$$
|P_{\text{proj}}|^2 = (P - (P \cdot n)n) \cdot (P - (P \cdot n)n)
$$
Using the distributive property of the dot product and the facts that $P \cdot P = r^2$ and $n \cdot n = 1$, the expression simplifies wonderfully:
$$
|P_{\text{proj}}|^2 = r^2 - (P \cdot n)^2
$$

In simple terms, this equation says that the squared distance of the shadow from the center is the sphere's squared radius minus the point's squared height above the plane. This is the Pythagorean theorem in disguise.

### The Conclusion
This final equation is powerfully conclusive. The term $(P \cdot n)^2$ is a squared value, so it must be positive or zero. This implies a critical inequality:
$$
|P_{\text{proj}}|^2 \le r^2
$$
This states that the squared distance of any point in the shadow is *less than or equal to* the squared radius of the sphere. The set of all points on a plane satisfying this condition is, by definition, a disk—a filled circle. The boundary of this disk, a circle of radius $r$, is formed by points on the sphere's "equator" relative to the plane, where $P \cdot n = 0$.

## An Alternate Path: The View from Spherical Coordinates

Despite the ordering of this article, my first instinct was not vector algebra, but to describe the geometry using angles. This approach, using spherical coordinates, offers a different but equally compelling perspective.

### The Setup

We define our point and plane using angles. The intuition is that since a plane is given by its normal vector, we can parametrize its "tilt" using spherical coordinates.

1.  **A point on a sphere $P$**: Its location is given by spherical coordinates $(r, \theta, \phi)$.
    $$
    P = \langle r\sin\phi\cos\theta, r\sin\phi\sin\theta, r\cos\phi \rangle
    $$
2.  **A plane through the origin**: Its orientation is defined by the fixed angles $(\theta_0, \phi_0)$ of its unit normal vector $n$.
    $$
    n = \langle \sin\phi_0\cos\theta_0, \sin\phi_0\sin\theta_0, \cos\phi_0 \rangle
    $$
Again, the condition for a point to lie on the intersection is that its position vector is orthogonal to the normal vector:
$$
P \cdot n = 0
$$

### The Calculation and Conclusion

Computing the dot product with coordinates yields a complicated expression. After factoring and applying the cosine angle-subtraction identity, we arrive at:
$$
\sin\phi\sin\phi_0\cos(\theta - \theta_0) + \cos\phi\cos\phi_0 = 0
$$
This equation is a special case of the **Spherical Law of Cosines**[^4]. It is a more complex way of stating that $\cos(\gamma) = 0$, where $\gamma$ is the angle between the vector $P$ and the normal vector $n$.

We could also recall a geometric definition of the dot product:

$$
P \cdot n = |P| |n| \cos\gamma
$$

[^4]: The realization that this formula was a known identity came during my exploration of the problem.

Since $|P||n| = r > 0$, the only way for the above expression to be zero is for $\cos(\gamma)$ to be zero; that is, the angle $\gamma$ must be a constant 90 degrees.

This forces every point $P$ on the intersection to lie at a fixed 90° angle from the axis defined by $n$. On the surface of a sphere, the set of all points at a constant 90° angle from a central axis is, by definition, a **great circle**[^5].

[^5]: A **great circle** is a circle on a sphere's surface whose center coincides with the sphere's center. If the plane does not pass through the center, the intersection is a **small circle**, like the Earth's lines of latitude.

## Certainty in a Shadow

My curiosity has now been put to rest.