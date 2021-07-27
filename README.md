# Split Raster

Provide good support for deep learning and computer vision tasks by creating a tiled output from an input raster dataset.'

Here is a sample image pairs, the size of RGB and GT are 1000-by-1000 large. The `SplitRaster` package successfully generate 16 256x256 images tiles with automatic padding on the edges. You can adjust the tile size and the overlap of the tiles for your own applications.

![Sample Image](docs/split_raster_sample.png)

## Use the packages

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
