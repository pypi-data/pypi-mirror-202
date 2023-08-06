import os
from pathlib import Path
import sys

from datetime import datetime
from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution
from setuptools import Extension


def get_project_name_version():
    # Version
    version = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "onegpt", "version.py")) as fp:
        exec(fp.read(), version)

    project_name = "onegpt"
    return project_name, version


project_name, version = get_project_name_version()
setup(
    name=project_name,
    version=version["__version__"],
    description="OneGPT",
    long_description="SimpleGPT for everyone",
    author="Longxing Tan",
    author_email="tanlongxing888@163.com",
    packages=find_packages(),
    install_requires=Path("requirements.txt").read_text().splitlines(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    license="Apache 2.0",
    keywords="GPT NLP LLM",
)
