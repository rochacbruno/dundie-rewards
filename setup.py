<<<<<<< HEAD
=======
"""setup the configuration app."""
# setuptools
# setup.py
>>>>>>> projeto-dundie-rewards/main
import os
from setuptools import setup, find_packages


def read(*paths):
<<<<<<< HEAD
    """Read the contents of a text file safely.
    >>> read("dundie", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
=======
    """Read the conmtents of a text of safely."""
    """
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
>>>>>>> projeto-dundie-rewards/main
    """
    rootpath = os.path.dirname(__file__)
    filepath = os.path.join(rootpath, *paths)
    with open(filepath) as file_:
        return file_.read().strip()


def read_requirements(path):
<<<<<<< HEAD
    """Return a list of requirements from a text file"""
=======
    """Return a list of requirements from a text file."""
>>>>>>> projeto-dundie-rewards/main
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(("#", "git+", '"', '-'))
    ]


setup(
    name="dundie",
<<<<<<< HEAD
    # Major.Minor.Patch
    # X.Y.Z
=======
>>>>>>> projeto-dundie-rewards/main
    version="0.1.1",
    description="Reward Point System for Dunder Mifflin",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
<<<<<<< HEAD
    author="Bruno Rocha",
    python_requires=">=3.8",
    packages=find_packages(exclude=["integration"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dundie = dundie.__main__:main"
=======
    author="Vinicius Telles",
    packages=find_packages(exclude="integration"),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'dundie = dundie.__main__:main',

>>>>>>> projeto-dundie-rewards/main
        ]
    },
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "test": read_requirements("requirements.test.txt"),
<<<<<<< HEAD
        "dev": read_requirements("requirements.dev.txt")
    }
)
=======
        "dev": read_requirements("requirements.dev.txt"),
    },

)

# pyproject


# external build tools (poetry, flit)
>>>>>>> projeto-dundie-rewards/main
