"Module for class 'RigidBody'"

from pymunk import Body

class RigidBody(object):
    """
    Represents an in-game rigid body, that has a position, orientation, and a
    collection of shapes, which provide geometry and mass.
    """

    def __init__(self, *shapes):
        self.body = Body(0, 0)
        self.shapes = []
        for shape in shapes:
            self.add_shape(shape)


    position = property(lambda self: self.body.position)
    angle = property(lambda self: self.body.angle)


    def _center_of_gravity(self):
        "return center of gravity as (x, y)"
        x, y = 0, 0
        for shape in self.shapes:
            x += shape.offset[0] * shape.mass
            y += shape.offset[1] * shape.mass
        x /= self.body.mass
        y /= self.body.mass
        return (x, y)


    def _offset_position(self, offset):
        """
        Move body position by given amount, and move all shape offsets in
        opposite direction to compensate.
        """
        self.body.position.x += offset[0]
        self.body.position.y += offset[1]
        for shape in self.shapes:
            shape.offset = (
                shape.offset[0] - offset[0],
                shape.offset[1] - offset[1])


    def get_moment(self):
        "Calculate this rigidbody's moment, the sum of its shape's moments"
        moment = 0.0
        for shape in self.shapes:
            moment += shape.get_moment()
        return moment


    def add_shape(self, shape):
        """
        Add given shape to this RigidBody's collection, recalculating the
        resulting center of gravity and updating body mass and moment.
        """
        self.shapes.append(shape)
        self.body.mass += shape.mass
        self._offset_position(self._center_of_gravity())
        self.body.moment = self.get_moment()


    def add_to_space(self, space, position, angle):
        """
        Add this RigidBody to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it.
        """
        self.body.position = position
        self.body.angle = angle
        space.add(self.body)
        for shape in self.shapes:
            shape.add_to_body(space, self.body)

