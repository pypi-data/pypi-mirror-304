import unittest
from pathlib import Path

from pyproject_pipenv import converter

DATA = Path(__file__).parent / 'data'


class Test(unittest.TestCase):
    def test_star(self):
        # FIXME: throw warning and require "--force" when there's a "star" requirement, these are not good for packages!
        c = converter.Converter(DATA / 'Pipfile.1', DATA / 'pyproject.1.toml')
        self.assertEqual(c.diff(), None)

    def test_other(self):
        c = converter.Converter(DATA / 'Pipfile.2', DATA / 'pyproject.2.toml')
        self.assertEqual(c.diff(), ({'requests'}, {'requests>=2.0.0'}))
