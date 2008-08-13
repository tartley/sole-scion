"Module of geometry utility functions"

from __future__ import division

from pymunk.util import is_clockwise, is_convex


def poly_area(verts):
    """
    Return area of a simple (ie. non-self-intersecting) polygon.
    Will be negative for counterclockwise winding.
    """
    accum = 0.0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        accum += verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
    return accum / 2


def poly_centroid(verts):
    "Return centroid of poly defined by verts"
    x, y = 0, 0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        factor = verts[j][0] * verts[i][1] - verts[i][0] * verts[j][1]
        x += (verts[i][0] + verts[j][0]) * factor
        y += (verts[i][1] + verts[j][1]) * factor
    area = poly_area(verts)
    x /= 6 * area
    y /= 6 * area
    return (x, y)


def assert_valid_poly(verts):
    "Raise TypeError if 'verts' not a valid convex clockwise poly"

    if len(verts) < 3:
        raise TypeError('need 3 or more verts: %s' % (verts,))
    if not is_convex(verts):
        raise TypeError('not convex: %s' % (verts,))
    if poly_area(verts) == 0.0:
        raise TypeError("colinear: %s" % (verts,))
    # note: pymunk considers y-axis points down, ours points up,
    # hence we consider pymunk's 'clockwise' to be anticlockwise
    if not is_clockwise(verts):
        raise TypeError('anticlockwise winding: %s' % (verts,))

