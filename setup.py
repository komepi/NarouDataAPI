import os

from setuptools import find_packages, setup

packages = find_packages()
# print(os.getcwd())
# g = {}
# with open(os.path.join(os.path.dirname(__file__),"narou_data_api","version.py"), "rt") as fp:
#    exec(fp.read(), g)
#    version = g["__version__"]

entry_points = {"console_scripts": ["narou_data=narou_data_api.cli:cmd"]}

install_requires = ["bs4", "click"]

tests_requires = ["responses", "pytest", "tox", "coverage"]

extras_require = {"tests": tests_requires}

setup(
    name="narou-data-api",
    version="1.0",
    description=__doc__,
    packages=packages,
    zip_safe=False,
    include_package_data=False,
    entry_points=entry_points,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_requires,
)
