# Contribution Guideline

## How to Contribute

First of all, thank you for your interest in contributing to this project. This project is still in its early stage and there are many things to do. If you are interested in contributing to this project, please follow the steps below:

1. Fork the repository
2. Make your changes
3. Submit a pull request
4. and wait for the review

### Clone the repository

```bash
# make sure you have the latest version of the code
git clone "https://github.com/cuicaihao/split_raster.git"
# make sure you are in the master branch
git checkout master
# pull the latest code
git pull
# create a new branch for your changes
git checkout -b <your_branch_name>
# make your changes
# add your changes
git add .
# commit your changes
git commit -m "your commit message"
# push your changes
git push origin <your_branch_name>
# submit a pull request
```

## Setting up the development environment

This project is developed using Python >= 3.10. The following packages are required:

- uv
- tqdm
- numpy
- scikit-image
- (optional) gdal (for GeoTiff support)

Please use `uv` to manage the virtual environment and dependencies. The following commands will help you set up the development environment.

```bash
# install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# sync the environment
uv sync

# run tests
uv run pytest tests/ -v
```

Then if you run the following command in your shell, you will see the installed packages.

```bash
❯ uv pip list
...
splitraster (at /path/to/split_raster)
numpy
scikit-image
tqdm
...
```

## Testing

To test your changes, please run the following command:

```bash
❯ pytest tests/ -v 
cachedir: .pytest_cache
rootdir: /Users/caihaocui/GitHub/split_raster
collected 2 items                                                                        

tests/test_splitraster.py::test_rgb_gt_slide_window PASSED                         [ 50%]
tests/test_splitraster.py::test_rgb_gt_random_crop PASSED                          [100%]
```

If you see the above output, it means that you have successfully passed the test.

## END
