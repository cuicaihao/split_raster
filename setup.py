from setuptools import find_packages, setup
from pathlib import Path
setup(
    name='splitraster',
    version='0.1.0',
    author='Chris Cui',
    author_email='',
    description='Provide good support for deep learning and computer vision tasks by creating a tiled output from an input raster dataset.',
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/cuicaihao/split_raster",
    package_dir={"": "src"},
    project_urls={
    },
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        'tqdm>=4.40.0',
        'numpy>=1.19.0',
        'scikit-image>=0.18.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
