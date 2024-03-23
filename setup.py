from setuptools import find_packages, setup
from pathlib import Path

setup(
    name="splitraster",
    version="0.3.5",
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
    packages=find_packages(
        where="src", exclude=["data", "features", "models", "visualization"]
    ),
    python_requires=">=3.7, <3.13",
    keywords="split raster tiling ",
    install_requires=[
        "tqdm>=4.40.0, <5.0.0",
        "numpy>=1.19.0, <2.0.0",
        "scikit-image>=0.18.0, <1.0.0",
        # 'gdal>=3.3.0' # too many local issues for this gdal python binding.
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
# rm -rf build dist
# python setup.py sdist bdist_wheel
# twine upload dist/*
