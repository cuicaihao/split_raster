import time
from tqdm import tqdm
import os
# from osgeo import gdal
import numpy as np
from skimage.io import imread, imsave
from pathlib import Path
import random


def read_image(fileName):
    if not Path(fileName).is_file():
        print(fileName + "Can not open file!")
        return None
    img = imread(fileName)
    # #     The different color bands/channels are stored in the third dimension,
    # such that a gray-image is MxN,
    # an RGB-image HxWx3 and
    # an RGBA-image HxWx4.
    return img


def save_image(img_arr, file_name):
    if Path(file_name).is_file():
        print(f"Overwrite existing file: {file_name}")
    imsave(file_name, img_arr)
    return file_name


def count_files(folder_path):
    count = 0
    for path in Path(folder_path).iterdir():
        if path.is_file():
            count += 1
    return count


def padding_image(img, crop_size, stride):

    if len(img.shape) == 2:
        img = img[:, :, np.newaxis]
    height = img.shape[0]
    width = img.shape[1]
    D = img.shape[2]  # this one is for (H, W, C) format
    # get the minial padding image size
    H = int(np.ceil(height/stride)*stride)
    W = int(np.ceil(width/stride)*stride)

    padded_img = np.zeros([H, W, D], dtype=img.dtype)
    for d in range(D):  # padding every layer
        onelayer = img[:, :, d]
        padded_img[:, :, d] = np.pad(
            onelayer, ((0, H - height), (0, W - width)), "reflect"
        )
    padded_img = np.squeeze(padded_img)  # Remove axes of length one
    return padded_img


def split_image(img_path, save_path, crop_size, repetition_rate=0, overwrite=True):
    # check input image
    img = read_image(img_path)
    if img is None:
        return None
    # get image suffix
    ext = Path(img_path).suffix
    # check output folder, if not exists, creat it.
    Path(save_path).mkdir(parents=True, exist_ok=True)

    height = img.shape[0]
    width = img.shape[1]
    print(f"Input Image File Shape (H, W, D):{ img.shape}")

    stride = int(crop_size*(1-repetition_rate))
    print(f"{crop_size=}, {stride=}")

    padded_img = padding_image(img, crop_size, stride)
    H = padded_img.shape[0]
    W = padded_img.shape[1]
    print(f"Padding Image File Shape (H, W, D):{ padded_img.shape}")

    if overwrite:
        new_name = 1
    else:
        cnt = count_files(save_path)
        new_name = cnt + 1
        print(f"There are {cnt} files in the {save_path}")
        print(f"New image name will start with {new_name}")

    n_rows = int((H - crop_size)/stride + 1)
    n_cols = int((W - crop_size)/stride + 1)

    def tile_generator():
        for idh in range(n_rows):
            h = idh*stride
            for idw in range(n_cols):
                w = idw*stride
                yield h, w

    with tqdm(total=n_rows*n_cols, desc='Generating', colour='green', leave=True, unit='img') as pbar:
        if(len(img.shape) == 2):
            for n, (h, w) in enumerate(tile_generator()):
                crop_img = padded_img[h:h+crop_size, w: w+crop_size]
                crop_image_name = f"{new_name:04d}{ext}"
                crop_image_path = Path(save_path) / crop_image_name
                save_image(crop_img, crop_image_path)
                new_name = new_name + 1
                # time.sleep(0.1)
                pbar.update(1)
        else:
            for n, (h, w) in enumerate(tile_generator()):
                crop_img = padded_img[h:h+crop_size, w: w+crop_size, :]
                crop_image_name = f"{new_name:04d}{ext}"
                crop_image_path = Path(save_path) / crop_image_name
                save_image(crop_img, crop_image_path)
                new_name = new_name + 1
                # time.sleep(0.1)
                pbar.update(1)

    return n+1
