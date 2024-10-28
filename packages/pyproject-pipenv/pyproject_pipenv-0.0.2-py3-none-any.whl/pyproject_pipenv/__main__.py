import argparse
import sys
from pathlib import Path

from .converter import Converter


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--pipfile', type=Path, default='Pipfile', help='Path to Pipfile')
    p.add_argument('-t', '--pyproject', type=Path, default='pyproject.toml', help='Path to pyproject.toml')
    p.add_argument('--fix', action='store_true', help='Apply required changes')
    args = p.parse_args(argv)

    c = Converter(args.pipfile, args.pyproject)
    diff = c.diff()

    if diff is None:
        print('pyproject.toml dependecies are up to date')
        return

    extra, missing = diff
    if extra:
        for r in extra:
            print(f'- {r}')
    if missing:
        for r in missing:
            print(f'+ {r}')

    if not args.fix:
        print('pyproject.toml dependencies NEED UPDATE!')
        sys.exit(1)

    c.sync()
    print('pyproject.toml dependencies UPDATED!')


if __name__ == '__main__':
    main()
