"Module of geometry utility functions"

from __future__ import division

from shapely.geometry import Polygon


def poly_area(verts):
    """
    Return area of a simple (ie. non-self-intersecting) polygon.
    Will be negative for counterclockwise winding.
    """
    accum = 0.0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        accum += verts[i][0] * verts[j][1] - verts[j][0] * verts[i][1]
    return -accum / 2


def assert_valid_poly(verts):
    "Raise TypeError if 'verts' not a valid convex clockwise poly"

    if len(verts) < 3:
        raise TypeError('need 3 or more verts: %s' % (verts,))
    poly = Polygon(verts)
    if poly.area == 0:
        raise TypeError('verts are colinear: %s' % (verts,))
    hull = poly.convex_hull
    diff = hull.difference(poly)
    if not diff.is_empty:
        raise TypeError('not convex: %s' % (verts,))
    if poly_area(verts) < 0:
        raise TypeError('clockwise winding: %s' % (verts,))

