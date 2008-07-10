import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from model.room import Room


class Room_test(MyTestCase):

    def testConstructor_needs_three_vertices(self):
        expectedMsg = '__init__() takes exactly 2 arguments (1 given)'
        self.assertRaises(lambda: Room(), TypeError, expectedMsg)

        expectedMsg = "need 3 or more verts"

        verts = []
        self.assertRaises(lambda: Room(verts), TypeError, expectedMsg)

        verts = [(0, 0)]
        self.assertRaises(lambda: Room(verts), TypeError, expectedMsg)

        verts = [(-1, 0), (1, 0)]
        self.assertRaises(lambda: Room(verts), TypeError, expectedMsg)


    def testConstructor(self):
        verts = [(-1, -2), (3, 4), (-5, 6)]
        room = Room(verts)
        self.assertEquals(room.verts, verts, "should store verts")



if __name__ == "__main__":
    run_test()
