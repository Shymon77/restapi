import unittest
from repository import SomeClass, some_function


class TestRepository(unittest.TestCase):

    def setUp(self):
        # инициализация, если нужна
        self.obj = SomeClass()

    def test_some_function(self):
        result = some_function(2, 3)
        self.assertEqual(result, 5)

    def test_some_class_method(self):
        self.assertTrue(self.obj.method())


if __name__ == "__main__":
    unittest.main()
