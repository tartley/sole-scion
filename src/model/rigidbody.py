"Module for class 'RigidBody'"

from pymunk import Body

class RigidBody(object):
    """
    Represents an in-game rigid body, that has a position, orientation, and a
    collection of shapes, which provide geometry and mass.
    """

    def __init__(self, *shapes):
        self.body = None
        self.shapes = []
        self.set_shapes(*shapes)


    position = property(lambda self: self.body and self.body.position)
    angle = property(lambda self: self.body and self.body.angle)


    def get_mass(self):
        "Calculate this rigidbody's mass, the sum of its shape's masses"
        mass = 0.0
        for shape in self.shapes:
            mass += shape.mass
        return mass


    def get_moment(self):
        "Calculate this rigidbody's moment, the sum of its shape's moments"
        moment = 0.0
        for shape in self.shapes:
            moment += shape.get_moment()
        return moment


    def _center_of_gravity(self):
        "return center of gravity as (x, y)"
        x, y = 0, 0
        mass = self.get_mass()
        for shape in self.shapes:
            offset = shape.get_offset()
            x += offset[0] * shape.mass
            y += offset[1] * shape.mass
        if len(self.shapes) > 0:
            x /= mass
            y /= mass
        return (x, y)


    def _offset_shapes(self, offset):
        "Move all shapes by the given offset."
        for shape in self.shapes:
            shape.offset(offset)


    def set_shapes(self, *shapes):
        """
        Add shapes to this RigidBody's collection, recalculating the
        resulting center of gravity and updating each shapes offset.
        """
        self.shapes = shapes
        cog = self._center_of_gravity()
        self._offset_shapes((-cog[0], -cog[1]))


    def add_to_space(self, space, position, angle):
        """
        Add this RigidBody to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it.
        """
        self.body = Body(self.get_mass(), self.get_moment())
        self.body.position = position
        self.body.angle = angle
        space.add(self.body)
        for shape in self.shapes:
            shape.add_to_body(space, self.body)

