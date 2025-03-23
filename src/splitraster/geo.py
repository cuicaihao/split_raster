from tqdm import tqdm
from osgeo import gdal, gdal_array
import numpy as np
from pathlib import Path
import random
from typing import Tuple, Optional


def read_rasterArray(image_path: str) -> Tuple[np.ndarray, Tuple[float, ...], str]:
    dataset = gdal.Open(image_path, gdal.GA_ReadOnly)
    image = dataset.ReadAsArray()  # get the rasterArray
    # convert 2D raster to [1, H, W] format
    if len(image.shape) == 2:
        image = image[np.newaxis, :, :]
    proj = dataset.GetProjection()
    geotrans = dataset.GetGeoTransform()
    return image, geotrans, proj


def save_rasterGeoTIF(
    im_data: np.ndarray, im_geotrans: Tuple[float, ...], im_proj: str, file_name: str
) -> None:
    if Path(file_name).is_file():
        print(f"Overwrite existing file: {file_name}")

    if "int8" in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif "int16" in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(
        file_name, int(im_width), int(im_height), int(im_bands), datatype
    )
    if dataset is not None:
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


def save_rasterArray(im_data: np.ndarray, file_name: str) -> bool:
    if Path(file_name).is_file():
        print(f"Overwrite existing file: {file_name}")
    gdal_array.SaveArray(im_data, file_name, format="GTiff")
    return True


def count_files(folder_path: str) -> int:
    return sum(1 for path in Path(folder_path).iterdir() if path.is_file())


def padding_mul_image(img: np.ndarray, stride: int) -> np.ndarray:
    D, height, width = img.shape  # (D, H, W) format Channel First.
    # get the minimal padding image size
    H = int(np.ceil(height / stride) * stride)
    W = int(np.ceil(width / stride) * stride)

    padded_img = np.zeros((D, H, W), dtype=img.dtype)
    for d in range(D):  # padding every layer
        onelayer = img[d, :, :]
        padded_img[d, :, :] = np.pad(
            onelayer, ((0, H - height), (0, W - width)), "reflect"
        )
    return padded_img


def split_image(
    img_path: str,
    save_path: str,
    crop_size: int,
    repetition_rate: float = 0,
    overwrite: bool = True,
    ext: Optional[str] = ".",
) -> Optional[int]:
    # check input image
    img, geotrans, proj = read_rasterArray(img_path)
    if img is None:
        print("Image not found")
        return None
    # get image suffix
    ext = Path(img_path).suffix
    # check output folder, if not exists, creat it.
    Path(save_path).mkdir(parents=True, exist_ok=True)

    print(f"Input Image File Shape (D, H, W):{ img.shape}")

    stride = int(crop_size * (1 - repetition_rate))
    print(f"crop_size = {crop_size}, stride = {stride}")

    padded_img = padding_mul_image(img, stride)

    H = padded_img.shape[1]
    W = padded_img.shape[2]

    print(f"Padding Image File Shape (D, H, W):{ padded_img.shape}")

    if overwrite:
        new_name = 1
    else:
        cnt = count_files(save_path)
        new_name = cnt + 1
        print(f"There are {cnt} files in the {save_path}")
        print(f"New image name will start with {new_name}")

    n_rows = int((H - crop_size) / stride + 1)
    n_cols = int((W - crop_size) / stride + 1)

    def tile_generator():
        for idh in range(n_rows):
            h = idh * stride
            for idw in range(n_cols):
                w = idw * stride
                yield h, w

    with tqdm(
        total=n_rows * n_cols, desc="Generating", colour="green", leave=True, unit="img"
    ) as pbar:
        for n, (h, w) in enumerate(tile_generator()):
            crop_img = padded_img[:, h : h + crop_size, w : w + crop_size]
            crop_image_name = f"{new_name:04d}{ext}"
            crop_image_path = Path(save_path) / crop_image_name
            save_rasterGeoTIF(crop_img, geotrans, proj, str(crop_image_path))
            new_name += 1
            pbar.update(1)

    return n + 1


def random_crop_image(
    img_path: str,
    img_save_path: str,
    label_path: str,
    label_save_path: str,
    crop_size: int = 256,
    crop_number: int = 20,
    img_ext: str = ".tif",
    label_ext: str = ".tif",
    overwrite: bool = True,
) -> Optional[int]:
    """Generate Random cropped image pair from the input image pairs.

    Args:
        img_path (str): path of input image
        img_save_path (str): path to save cropped images
        label_path (str): path of input label
        label_save_path (str): path to save cropped labels
        crop_size (int): image tile size (H,W), i.e., 256x256
        crop_number (int): number of crops to generate
        img_ext (str): extension for image files
        label_ext (str): extension for label files
        overwrite (bool): overwrite existing files
    """
    img, geotrans, proj = read_rasterArray(label_path)
    if img is None:
        print("Input image is missing")
        return None

    label, geotrans, proj = read_rasterArray(img_path)
    if label is None:
        print("Label image is missing")
        return None

    # check output folder, if not exists, create it.
    Path(img_save_path).mkdir(parents=True, exist_ok=True)
    Path(label_save_path).mkdir(parents=True, exist_ok=True)

    # get the file formats, if none, use the same format as the source file.
    if img_ext is None:
        img_ext = Path(img_path).suffix
    if label_ext is None:
        label_ext = Path(label_path).suffix

    # find the start name of the image paris.
    if overwrite:
        new_name = 1
    else:
        img_cnt = count_files(img_path)
        label_cnt = count_files(label_path)
        new_name = img_cnt + 1
        print(f"There are {img_cnt} files in the {img_save_path}")
        print(f"There are {label_cnt} files in the {label_save_path}")
        if not img_cnt == label_cnt:
            print("Image Pair doest not match in output folders.")
            return None
        print(f"New image pairs' name will start with {new_name}")

    crop_cnt = 0
    H = img.shape[1]
    W = img.shape[2]

    with tqdm(
        total=crop_number, desc="Generating", colour="green", leave=True, unit="img"
    ) as pbar:
        while crop_cnt < crop_number:
            # Crop img_crop, label_crop paris and save them to the output folders.
            UpperLeftX = random.randint(0, H - crop_size)
            UpperLeftY = random.randint(0, W - crop_size)

            imgCrop = img[
                :,
                UpperLeftX : UpperLeftX + crop_size,
                UpperLeftY : UpperLeftY + crop_size,
            ]

            labelCrop = label[
                :,
                UpperLeftX : UpperLeftX + crop_size,
                UpperLeftY : UpperLeftY + crop_size,
            ]
            # save image pairs
            crop_image_name = f"{new_name:04d}{img_ext}"
            crop_image_path = Path(img_save_path) / crop_image_name
            save_rasterGeoTIF(imgCrop, geotrans, proj, str(crop_image_path))

            crop_image_name = f"{new_name:04d}{label_ext}"
            crop_image_path = Path(label_save_path) / crop_image_name
            save_rasterGeoTIF(labelCrop, geotrans, proj, str(crop_image_path))

            new_name += 1  # update image name
            crop_cnt += 1  # add crop count
            pbar.update(1)

    return crop_cnt  # return total crop sample pair number.
