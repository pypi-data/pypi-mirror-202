import os
import sys
from setuptools import setup, find_packages

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

setup(
    name='xlsmloader',
    version="1.0.2",
    author="Paulo Rogerio Sales Santos",
    author_email="paulosales@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
    ),
    url="https://xlsmloader.pypa.io/",
    entry_points={
        "console_scripts": [
            "xlsmloader=loader.loader:load",
        ],
    },
    python_requires=">=3.7",
)
