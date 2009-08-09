
from pymunk import Body


class Chunk(object):
    """
    Represents an in-game rigid body, that has a position, orientation, and a
    collection of shards (Blocks and Discs), which provide geometry and mass.
    """

    def __init__(self, *shards):
        self.body = None
        self.shards = []
        self.set_shards(*shards)


    position = property(lambda self: self.body and self.body.position)
    angle = property(lambda self: self.body and self.body.angle)


    def get_mass(self):
        return sum(shard.mass for shard in self.shards)


    def get_moment(self):
        return sum(shard.get_moment() for shard in self.shards)


    def _center_of_gravity(self):
        x, y = 0, 0
        mass = self.get_mass()
        for shard in self.shards:
            offset = shard.get_centroid()
            x += offset[0] * shard.mass
            y += offset[1] * shard.mass
        if len(self.shards) > 0:
            x /= mass
            y /= mass
        return (x, y)


    def _offset_shards(self, offset):
        for shard in self.shards:
            shard.offset(offset)


    def set_shards(self, *shards):
        self.shards = shards
        cog = self._center_of_gravity()
        self._offset_shards((-cog[0], -cog[1]))


    def add_to_space(self, space, position, angle):
        self.body = Body(self.get_mass(), self.get_moment())
        self.body.position = position
        self.body.angle = angle
        space.add(self.body)
        for shard in self.shards:
            shard.add_to_body(space, self.body)

