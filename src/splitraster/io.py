# import time
# from osgeo import gdal
from tqdm import tqdm
import numpy as np
from skimage.io import imread, imsave
from pathlib import Path
import random


def read_rasterArray(image_path):
    dataset = gdal.Open(image_path, gdal.GA_ReadOnly)
    image = dataset.ReadAsArray()  # get the rasterArray
    # convert 2D raster to [1, H, W] format
    if len(image.shape) == 2:
        image = image[np.newaxis, :, :]
    [D, H, W] = image.shape
    pimg = Path(image_path)

    print(pimg.stem, image.shape, image_path)

    return image, [D, H, W]


def read_image(file_name):
    if not Path(file_name).is_file():
        print(file_name + "Can not open file!")
        return None
    img = imread(file_name)
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


def padding_image(img, stride):

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

    print(f"Input Image File Shape (H, W, D):{ img.shape}")

    stride = int(crop_size*(1-repetition_rate))
    print(f"crop_size = {crop_size}, stride = {stride}")

    padded_img = padding_image(img,   stride)
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
                pbar.update(1)
        else:
            for n, (h, w) in enumerate(tile_generator()):
                crop_img = padded_img[h:h+crop_size, w: w+crop_size, :]
                crop_image_name = f"{new_name:04d}{ext}"
                crop_image_path = Path(save_path) / crop_image_name
                save_image(crop_img, crop_image_path)
                new_name = new_name + 1
                pbar.update(1)

    return n+1


def random_crop_image(img_path, img_save_path,  label_path, label_save_path, crop_size=256, crop_number=20, img_ext='.jpg', label_ext='.png', overwrite=True):
    """Generate Random cropped image pair from the input image pairs.

    Args:
        img_path (str): path of input image
        img_save_path (str):  
        crop_size (int): image tile size (H,W), i.e., 256x256
        overwrite (bool, optional): [overwrite existing files]. Defaults to True.
    """
    img = read_image(img_path)
    if img is None:
        print("Input image is missing")
        return None
    label = read_image(label_path)
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
    H = img.shape[0]
    W = img.shape[1]

    with tqdm(total=crop_number, desc='Generating', colour='green', leave=True, unit='img') as pbar:
        while (crop_cnt < crop_number):
            # Crop img_crop, label_crop paris and save them to the output folders.
            UpperLeftX = random.randint(0, H - crop_size)
            UpperLeftY = random.randint(0, W - crop_size)
            if(len(img.shape) == 2):
                imgCrop = img[UpperLeftX: UpperLeftX + crop_size,
                              UpperLeftY: UpperLeftY + crop_size]
            else:
                imgCrop = img[UpperLeftX: UpperLeftX + crop_size,
                              UpperLeftY: UpperLeftY + crop_size, :]
            if(len(label.shape) == 2):
                labelCrop = label[UpperLeftX: UpperLeftX + crop_size,
                                  UpperLeftY: UpperLeftY + crop_size]
            else:
                labelCrop = label[UpperLeftX: UpperLeftX + crop_size,
                                  UpperLeftY: UpperLeftY + crop_size, :]
            # save image pairs
            crop_image_name = f"{new_name:04d}{img_ext}"
            crop_image_path = Path(img_save_path) / crop_image_name
            save_image(imgCrop, crop_image_path)

            crop_image_name = f"{new_name:04d}{label_ext}"
            crop_image_path = Path(label_save_path) / crop_image_name
            save_image(labelCrop, crop_image_path)

            new_name = new_name + 1  # update image name
            crop_cnt = crop_cnt + 1  # add crop count
            pbar.update(1)

    return crop_cnt  # return total crop sample pair number.
