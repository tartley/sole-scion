import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.world import World


class World_test(MyTestCase):

    def testConstructor(self):
        world = World()
        self.assertEquals(world.rooms, set(),
            "should have empty room collection")


    def testPopulate(self):
        world = World()
        world.populate()
        self.assertEquals(len(world.rooms), 1, "should create one room")
        room = world.rooms.pop()
        self.assertEquals(len(room.verts), 5, "room should be a pentagon")


if __name__ == "__main__":
    run_test()
