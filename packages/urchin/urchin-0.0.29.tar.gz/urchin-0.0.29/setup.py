"""
Author: Adam Fishman
"""
from setuptools import setup

requirements = [
    "lxml",  # For XML DOM Tree
    "networkx",  # For joint graph
    "numpy",  # Numpy
    "pillow",  # For texture image loading
    "pycollada>=0.6",  # COLLADA (.dae) mesh loading via trimesh
    "pyribbit>=0.1.46",  # For visualization
    "scipy",  # For trimesh, annoyingly
    "six",  # Python 2/3 compatability
    "trimesh",  # Mesh geometry loading/creation/saving
]

dev_requirements = [
    "flake8",  # Code formatting checker
    "pre-commit",  # Pre-commit hooks
    "pytest",  # Code testing
    "pytest-cov",  # Coverage testing
    "tox",  # Automatic virtualenv testing
]

docs_requirements = [
    "sphinx",  # General doc library
    "sphinx_rtd_theme",  # RTD theme for sphinx
    "sphinx-automodapi",  # For generating nice tables
]

setup(
    name="urchin",
    version="0.0.29",
    description="URDF parser and manipulator for Python",
    long_description="URDF parser and manipulator for Python. This package is a fork of urdfpy, which seems to be no longer maintained. ",
    author="Adam Fishman",
    author_email="hello@fishbotics.com",
    license="MIT License",
    url="https://github.com/fishbotics/urchin",
    keywords="robotics ros urdf robots parser",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
    ],
    packages=["urchin"],
    setup_requires=requirements,
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "docs": docs_requirements,
    },
)
