"Module for class 'RigidBody'"

from pymunk import Body

class RigidBody(object):
    """
    Represents an in-game rigid body, that has a position, orientation, and a
    collection of shards, which provide geometry and mass.
    """

    def __init__(self, *shards):
        self.body = None
        self.shards = []
        self.set_shards(*shards)


    position = property(lambda self: self.body and self.body.position)
    angle = property(lambda self: self.body and self.body.angle)


    def get_mass(self):
        "Calculate this rigidbody's mass, the sum of its shard's masses"
        mass = 0.0
        for shard in self.shards:
            mass += shard.mass
        return mass


    def get_moment(self):
        "Calculate this rigidbody's moment, the sum of its shard's moments"
        moment = 0.0
        for shard in self.shards:
            moment += shard.get_moment()
        return moment


    def _center_of_gravity(self):
        "return center of gravity as (x, y)"
        x, y = 0, 0
        mass = self.get_mass()
        for shard in self.shards:
            offset = shard.get_offset()
            x += offset[0] * shard.mass
            y += offset[1] * shard.mass
        if len(self.shards) > 0:
            x /= mass
            y /= mass
        return (x, y)


    def _offset_shards(self, offset):
        "Move all shards by the given offset."
        for shard in self.shards:
            shard.offset(offset)


    def set_shards(self, *shards):
        """
        Set this RigidBody's collection of shards, updating the offset of
        each shard so that they are centered around the collective
        center of gravity.
        """
        self.shards = shards
        cog = self._center_of_gravity()
        self._offset_shards((-cog[0], -cog[1]))


    def add_to_space(self, space, position, angle):
        """
        Add this RigidBody to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it.
        """
        self.body = Body(self.get_mass(), self.get_moment())
        self.body.position = position
        self.body.angle = angle
        space.add(self.body)
        for shard in self.shards:
            shard.add_to_body(space, self.body)

