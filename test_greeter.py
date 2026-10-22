import unittest

from greeter import Greeter


class GreeterTest(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(Greeter().greet("World"), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
