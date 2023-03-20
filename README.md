# Split Raster

[![image](https://img.shields.io/pypi/pyversions/splitraster)](https://python.org/pypi/splitraster)
[![image](https://img.shields.io/pypi/v/splitraster?color=g)](https://python.org/pypi/splitraster)
[![CI](https://img.shields.io/github/actions/workflow/status/cuicaihao/split_raster/python-app.yml?branch=master)](https://github.com/cuicaihao/split_raster/actions/workflows/python-app.yml)
[![image](https://img.shields.io/pypi/dm/splitraster?color=blue)](https://python.org/pypi/splitraster)
[![image](https://img.shields.io/github/license/cuicaihao/split_raster?color=blue)](https://python.org/pypi/splitraster)

- Document: [split_raster](https://cuicaihao.github.io/split_raster/)
- Pypi: [splitraster](https://pypi.org/project/splitraster/)


## Introduction

Split Raster is an open-source and highly versatile Python package designed to easily break down large images into smaller, more manageable tiles. While the package is particularly useful for deep learning and computer vision tasks, it can be applied to a wide range of applications.

Initially developed by the authoer to provide optimal support for deep learning and computer vision tasks, Split Raster was specifically designed for image segmentation tasks on satellite images as well as remote sensing methods. By generating tiled output image samples from an input raster dataset, Split Raster enables more efficient and effective analysis of large images. The package also includes a random sampling function that generates a fixed number of tiles for early experimentation.

For example, let's say you have a set of RGB and GT images, each with dimensions of 1000-by-1000 pixels. Utilizing Split Raster, you can easily generate 16 tiles, each with dimensions of 256x256 pixels and automatic padding on the edges. The package also allows for customization of tile size and overlap to better suit individual project needs. Furthermore, Split Raster handles the padding and naming of output images automatically, saving time and effort (e.g., 0001.png, 0002.png, ..., 9999.png).

![Sample Image](docs/img/split_raster_sample.png)

## Tutorial to generate the above sample image

Open the notebook [SplitRaster Tutorial](notebooks/Tutorial.ipynb).

This tutorial will show you how to use the package to split a large image into small tiles. So you can use the small tiles for your deep learning and computer vision tasks.

[`pytorch`](https://pytorch.org/) is used in this tutorial. You can also use `tensorflow` or other deep learning frameworks.

## Install the packages

```bash
pip install splitraster
```

## Try Sample code

The sample image can be found in the GitHub repo.

```python

from splitraster import io

input_image_path = "./data/raw/RGB.png"
gt_image_path = "./data/raw/GT.png"

save_path = "../data/processed/RGB"
save_path_gt = "./data/processed/GT"

crop_size = 256
repetition_rate = 0.5
overwrite = False

n = io.split_image(input_image_path, save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {save_path}")


n = io.split_image(gt_image_path, save_path_gt, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {gt_image_path} are added at {save_path_gt}")


```

Possible results:

```bash
Successfully installed splitraster-0.*.*
❯ python test.py
Input Image File Shape (H, W, D):(1000, 1000, 3)
crop_size=256, stride=128
Padding Image File Shape (H, W, D):(1024, 1024, 3)
There are 49 files in the ./data/processed/RGB
New image name will start with 50
Generating: 100%|█████████████████████████████████████████████████████████████| 49/49 [00:00<00:00, 50.65img/s]
49 tiles sample of ./data/raw/RGB.png are added at ./data/processed/RGB
Input Image File Shape (H, W, D):(1000, 1000)
crop_size=256, stride=128
Padding Image File Shape (H, W, D):(1024, 1024)
There are 49 files in the ./data/processed/GT
New image name will start with 50
Generating: 100%|████████████████████████████████████████████████████████████| 49/49 [00:00<00:00, 139.72img/s]
49 tiles sample of ./data/raw/GT.png are added at ./data/processed/GT
```
 
You can also work with Remote Sensing (GeoTIFF) Satellite images such as Multispectral Images which have more bands or channels. All the codes will be the same, but with a small difference. Replace the `io` with the `geo` module.

This feature also needs you to install the `gdal` package with the following command in your python environment.
This package is not in the required packages due to many users may not use this function.

```bash
conda install -c conda-forge gdal
```

Sample Code:

```Python
from splitraster import geo
input_image_path = "./data/raw/Input.tif"
gt_image_path = "./data/raw/GT.tif"

save_path = "../data/processed/Input"
crop_size = 256
repetition_rate = 0.5
overwrite = False

n = geo.split_image(input_image_path, save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {save_path}")
```

## Random Sampling Code

The basic implementation is still the same as the above. Just replace the 'split_image' method to 'rand_crop_image'.

```python
from splitraster import io
input_image_path = "./data/raw/RGB.png"
gt_image_path = "./data/raw/GT.png"

input_save_path = "./data/processed/Rand/RGB"
gt_save_path = "./data/processed/Rand/GT"

n = io.random_crop_image(input_image_path, input_save_path,  gt_image_path, gt_save_path, crop_size=256, crop_number=20, img_ext='.png', label_ext='.png', overwrite=True)

print(f"{n} sample paris of {input_image_path, gt_image_path} are added at {input_save_path, gt_save_path}.")

```

```python
from splitraster import geo
input_tif_image_path = "./data/raw/TIF/RGB5k.tif"
gt_tif_image_path = "./data/raw/TIF/GT5k.tif"

input_save_image_path = "./data/processed/Rand/RGB_TIF"
gt_save_image_path = "./data/processed/Rand/GT_TIF"

n = geo.random_crop_image(input_tif_image_path, input_save_image_path,  gt_tif_image_path, gt_save_image_path, crop_size=500, crop_number=20, overwrite=True)

print(f"{n} sample paris of {input_tif_image_path, gt_tif_image_path} are added at {input_save_image_path, gt_save_image_path}.")

```
## Future Update:

- [x] Add Random Sampling feature.
- [ ] ~~Create a GUI with Qt and generate an executable file~~ (Not a good idea, since it is not a good practice to use GUI in a package).
- [ ] Add Sample Balancing feature, which can be used to balance the sample number of different classes, especially for the unbalanced dataset.

 
## Update Log
- 2023-Mar-19  Update github actions and add tutorial for the package.
- 2022-Dec-16  Upgrade the package to support python 3.8, 3.9, 3.10, 3.11 (https://pypi.org/project/splitraster/0.3.3).
- 2022-Jan-16  Fix bugs to make package suitable for python 3.7. Publish new version at(https://pypi.org/project/splitraster/0.3.2/) .
 
## Contribution Guidelines

If you run into issues or have questions, please [open an issue](https://github.com/cuicaihao/split_raster/issues) or [submit a pull request](https://github.com/cuicaihao/split_raster/pulls).

If you are interested in contributing to `splitraster`, please see our [contributing guidelines](../CONTRIBUTING.md).
  
 
## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
