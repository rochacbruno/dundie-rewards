# setuptools
# setup.py
from setuptools import setup, find_packages


setup(
    name="dundie",
    version="0.1.0",
    description="Reward Point System for Dunder Mifflin",
    author="Vinicius Telles",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dundie1 = dundie.__main__:main"
        ]
    }
)

# pyproject


# external build tools (poetry, flit)
