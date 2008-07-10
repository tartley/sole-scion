import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from model.entity import Entity


class Entity_test(MyTestCase):

    def testConstructor_assigns_ids(self):
        entity1 = Entity()
        self.assertEquals(type(entity1.id), int,
            "should assign an integer id")
        self.assertTrue(entity1.id > 0, "should assign positive id")

        entity2 = Entity()
        self.assertEquals(entity2.id, entity1.id + 1,
            "should increment to get next unique id")


if __name__ == "__main__":
    run_test()
