import unittest

from pyproject_pipenv import __main__ as ppmain


class Test(unittest.TestCase):
    def test_echo(self):
        self.assertEqual(ppmain.main(), None)
