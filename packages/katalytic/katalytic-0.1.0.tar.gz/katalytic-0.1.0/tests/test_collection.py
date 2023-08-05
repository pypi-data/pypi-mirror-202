import re
from glob import glob

from katalytic import pkg, katalytic


def test_versions():
    modules = {m.__name__: m for m in pkg.get_modules()}
    modules['katalytic'] = katalytic
    for toml in glob('../../**/pyproject.toml', recursive=True):
        module, toml_version = _get_pkg_and_version(toml)
        installed_version = modules[module].__version__
        assert installed_version == toml_version, module


def _get_pkg_and_version(toml):
    with open(toml, 'r') as f:
        text = f.readlines()

    pkg = None
    version = None
    for line in text:
        if line.startswith('name'):
            pkg = re.search(r'\=\s*(\'|")(.*)\1', line)[2]
            pkg = pkg.replace('-', '.')

        if line.startswith('version'):
            version = re.search(r'=\s*([\'"])(.*)\1', line)[2]

        if pkg and version:
            return (pkg, version)
