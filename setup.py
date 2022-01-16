from setuptools import find_packages, setup
from pathlib import Path
setup(
    name='splitraster',
    version='0.3.2',
    author='Chris Cui',
    author_email='',
    description='Provide good support for deep learning and computer vision tasks by creating a tiled output from an input raster dataset.',
    long_description=Path("PyPi.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/cuicaihao/split_raster",
    package_dir={"": "src"},
    project_urls={
    },
    packages=find_packages(where="src", exclude=[
                           "data", "features", "models", "visualization"]),
    python_requires=">=3.7",
    install_requires=[
        'tqdm>=4.40.0',
        'numpy>=1.19.0',
        'scikit-image>=0.18.0',
        # 'gdal>=3.3.0' # too many local issues for this gdal python binding.
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# rm -rf build dist
# python setup.py sdist bdist_wheel
# twine upload dist/*
