from __future__ import division
from math import cos, pi, sin

from pymunk import Vec2d
from pymunk.util import is_clockwise, is_convex


def circle(radius, num_segments):
    verts = []
    for idx in xrange(num_segments):
        theta = 2*pi / num_segments * idx
        verts.append((radius * sin(theta), radius * cos(theta)))
    return verts


def regular(num_faces, first, second):
    if num_faces < 3:
        raise ValueError('num_faces must be >=3')

    internal_angle_deg = 360 / num_faces
    wallvect = Vec2d(second) - Vec2d(first)

    verts = []
    vert = first
    for _ in xrange(num_faces):
        verts.append(vert)
        _vert = (wallvect + vert)
        vert = _vert.x, _vert.y
        wallvect.rotate(-internal_angle_deg)

    return verts


def assert_valid(verts):
    if len(verts) < 3:
        raise TypeError('need 3 or more verts: %s' % (verts,))
    if not is_convex(verts):
        raise TypeError('not convex: %s' % (verts,))
    if area(verts) == 0.0:
        raise TypeError("colinear: %s" % (verts,))
    # note: pymunk considers y-axis points down, ours points up,
    # hence we consider pymunk's 'clockwise' to be anticlockwise
    if not is_clockwise(verts):
        raise TypeError('anticlockwise winding: %s' % (verts,))


def offset_verts(verts, offset):
    return type(verts)(
        (verts[i][0] + offset[0], verts[i][1] + offset[1])
        for i in range(len(verts))
    )


def area(verts):
    """
    Return area of a simple (ie. non-self-intersecting) polygon.
    Will be negative for counterclockwise winding.
    """
    accum = 0.0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        accum += verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
    return accum / 2


def centroid(verts):
    x, y = 0, 0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        factor = verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
        x += (verts[i][0] + verts[j][0]) * factor
        y += (verts[i][1] + verts[j][1]) * factor
    polyarea = area(verts)
    x /= 6 * polyarea
    y /= 6 * polyarea
    return (x, y)

