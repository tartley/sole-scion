
from pymunk import moment_for_poly


class Loop(object):

    def __init__(self, verts=None):
        print 'Loop', type(verts)
        if verts is None:
            verts = []
        self.verts = verts
        self.density = 1


    def get_area(self):
        """
        Return area of a simple (ie. non-self-intersecting) polygon.
        If poly does intersect, the actual area will be smaller than this.
        Will return negative for counterclockwise winding.
        """
        accum = 0.0
        for i in range(len(self.verts)):
            j = (i + 1) % len(self.verts)
            accum += (
                self.verts[j][0] * self.verts[i][1] -
                self.verts[i][0] * self.verts[j][1])
        return accum / 2


    def get_mass(self):
        return self.get_area() * self.density


    def get_centroid(self):
        x, y = 0, 0
        for i in xrange(len(self.verts)):
            j = (i + 1) % len(self.verts)
            factor = (
                self.verts[j][0] * self.verts[i][1] -
                self.verts[i][0] * self.verts[j][1])
            x += (self.verts[i][0] + self.verts[j][0]) * factor
            y += (self.verts[i][1] + self.verts[j][1]) * factor
        polyarea = self.get_area()
        x /= 6 * polyarea
        y /= 6 * polyarea
        return (x, y) 


    def get_moment(self):
        return moment_for_poly(self.get_mass(), self.verts, (0, 0))


    def offset(self, x, y):
        self.verts = [
            (self.verts[i][0] + x, self.verts[i][1] + y)
            for i in xrange(len(self.verts))
        ]


    def offset_to_origin(self):
        x, y = self.get_centroid()
        self.offset(-x, -y)

