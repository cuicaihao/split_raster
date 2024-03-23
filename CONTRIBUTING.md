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

This project is developed using Python 3.9.16. The following packages are required:

- pipev
- tqdm
- numpy
- scikit-image
- (optional) gdal (for GeoTiff support)

Please use the `pipenv` to manage the virtual environment. The following commands will help you set up the development environment.

```bash
# install pipenv
pip install pipenv
# install the required packages
pipenv install
# activate the virtual environment
pipenv shell
```

Then if you run the following command in your shell, you will seee the following output. This means that you have successfully set up the development environment.

```python
❯ pipenv graph
pytest==7.2.0
  - attrs [required: >=19.2.0, installed: 22.1.0]
  - exceptiongroup [required: >=1.0.0rc8, installed: 1.0.4]
  - iniconfig [required: Any, installed: 1.1.1]
  - packaging [required: Any, installed: 22.0]
  - pluggy [required: >=0.12,<2.0, installed: 1.0.0]
  - tomli [required: >=1.0.0, installed: 2.0.1]
splitraster==0.3.3
  - numpy [required: >=1.19.0, installed: 1.24.0]
  - scikit-image [required: >=0.18.0, installed: 0.19.3]
    - imageio [required: >=2.4.1, installed: 2.22.4]
      - numpy [required: Any, installed: 1.24.0]
      - pillow [required: >=8.3.2, installed: 9.3.0]
    - networkx [required: >=2.2, installed: 2.8.8]
    - numpy [required: >=1.17.0, installed: 1.24.0]
    - packaging [required: >=20.0, installed: 22.0]
    - pillow [required: >=6.1.0,!=8.3.0,!=7.1.1,!=7.1.0, installed: 9.3.0]
    - PyWavelets [required: >=1.1.1, installed: 1.4.1]
      - numpy [required: >=1.17.3, installed: 1.24.0]
    - scipy [required: >=1.4.1, installed: 1.9.3]
      - numpy [required: >=1.18.5,<1.26.0, installed: 1.24.0]
    - tifffile [required: >=2019.7.26, installed: 2022.10.10]
      - numpy [required: >=1.19.2, installed: 1.24.0]
  - tqdm [required: >=4.40.0, installed: 4.64.1]
  ```

## Testing
To test your changes, please run the following command:

```bash
❯ pytest test.py -v 
cachedir: .pytest_cache
rootdir: /Users/caihaocui/Documents/GitHub/split_raster
collected 2 items                                                                        

test.py::test_rgb_gt_slide_window PASSED                                           [ 50%]
test.py::test_rgb_gt_random_crop PASSED                                            [100%]
```

If you see the above output, it means that you have successfully passed the test.


## END


