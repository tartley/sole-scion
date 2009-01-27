
from math import pi
from pymunk import Vec2d


def create_regular(num_faces, v1, v2):
    if num_faces < 3:
        raise ValueError('num_faces must be >=3')

    internal_angle_deg = 360 / num_faces
    wallvect = Vec2d(v2) - Vec2d(v1)

    verts = []
    vert = v1
    for _ in xrange(num_faces):
        verts.append(vert)
        _vert = (wallvect + vert)
        vert = _vert.x, _vert.y
        wallvect.rotate(-internal_angle_deg)

    return verts

