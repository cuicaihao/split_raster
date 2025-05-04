from setuptools import find_packages, setup
from pathlib import Path


def read_requirements():
    with open("requirements.txt", "r") as req_file:
        requirements = req_file.read().splitlines()
    return requirements


setup(
    name="splitraster",
    version="0.3.7",
    author="Chris Cui",
    license="MIT",
    platforms="any",
    author_email="",
    description="Provide good support for deep learning and computer vision tasks by creating a tiled output from an input raster dataset.",
    long_description=Path("PyPi.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/cuicaihao/split_raster",
    package_dir={"": "src"},
    project_urls={},
    packages=find_packages(where="src", exclude=["data"]),
    python_requires=">=3.7, <3.14",
    keywords="split raster tiling ",
    install_requires=read_requirements(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
# rm -rf build dist
# python setup.py sdist bdist_wheel
# twine upload dist/*
