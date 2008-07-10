import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.world import World


class World_test(MyTestCase):

    def testConstructor(self):
        world = World()
        self.assertEquals(world.entities, set(),
            "should start with no entities")

        self.assertEquals(len(world.rooms), 1,
            "should start with one room")

        room = [room for room in world.rooms][0]
        self.assertEquals(len(room.verts), 5,
            "first room should be a pentagon")


    def testSpawn(self):
        world = World()
        entity = Entity()
        world.entities.add(Entity())


if __name__ == "__main__":
    run_test()
