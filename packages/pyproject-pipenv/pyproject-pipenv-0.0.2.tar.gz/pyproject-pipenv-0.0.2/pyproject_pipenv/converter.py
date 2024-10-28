# tomlkit over toml because it preserves format/comments
from pathlib import Path

import tomlkit


class Converter:
    def __init__(self, pipfile_path: Path, pyproject_path: Path):
        self.pipfile_path = pipfile_path
        self.pyproject_path = pyproject_path
        self.pipfile_content = None
        self.pyproject_content = None
        self.load()

    def load(self):
        with open(self.pipfile_path, 'r') as f:
            self.pipfile_content = tomlkit.parse(f.read())
        with open(self.pyproject_path, 'r') as f:
            self.pyproject_content = tomlkit.parse(f.read())

    def pipfile_list(self):
        packages = []
        for name, version_dict in self.pipfile_content.get('packages', {}).items():
            if isinstance(version_dict, dict):
                version = version_dict['version']
            else:
                version = version_dict
            if version == '*':
                version = ''
            packages.append(f'{name}{version}')
        return packages

    def pyproject_list(self):
        return self.pyproject_content['project']['dependencies']

    def diff(self):
        pp = set(self.pyproject_list())
        pf = set(self.pipfile_list())
        extra = pp - pf
        missing = pf - pp
        if not extra and not missing:
            return None
        return extra, missing

    def sync(self):
        self.pyproject_content['project']['dependencies'] = self.pipfile_list()
        with open(self.pyproject_path, 'w') as f:
            f.write(tomlkit.dumps(self.pyproject_content))
