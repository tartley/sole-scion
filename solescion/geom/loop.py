
from pymunk import moment_for_poly, Poly


class Loop(object):

    density = 1

    def __init__(self, verts=None):
        if verts is None:
            verts = []
        self.verts = verts


    def get_area(self):
        """
        Return area of a simple (ie. non-self-intersecting) polygon.
        If poly does intersect, the actual area will be smaller than this.
        """
        print '  loop.get_area()'
        print self.verts
        accum = 0.0
        for i in range(len(self.verts)):
            j = (i + 1) % len(self.verts)
            accum += (
                self.verts[j][0] * self.verts[i][1] -
                self.verts[i][0] * self.verts[j][1])
        return abs(accum / 2)


    def is_clockwise(self):
        '''
        assume y-axis points up
        '''
        print 'is_clockwise'
        print ['%2f, %2f' % (x, y) for x, y in self.verts]

        accum = 0.0
        for i in range(len(self.verts)):
            j = (i + 1) % len(self.verts)
            accum += (
                self.verts[j][0] * self.verts[i][1] -
                self.verts[i][0] * self.verts[j][1])
        print accum > 0

        return accum > 0

        
    def get_mass(self):
        print '  loop.get_mass', self.get_area() * self.density
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
        print '  loop.get_moment', self.get_area() * self.density
        return moment_for_poly(self.get_mass(), self.verts, (0, 0))


    def offset(self, x, y):
        self.verts = [
            (self.verts[i][0] + x, self.verts[i][1] + y)
            for i in xrange(len(self.verts))
        ]


    def get_shape(self, body):
        shape = Poly(body, self.verts, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 10.0
        return shape

