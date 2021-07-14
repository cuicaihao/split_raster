
from tqdm import tqdm

from osgeo import gdal
from osgeo import gdal_array

import numpy as np
from pathlib import Path


def read_rasterArray(image_path):
    dataset = gdal.Open(image_path, gdal.GA_ReadOnly)
    image = dataset.ReadAsArray()  # get the rasterArray
    # convert 2D raster to [1, H, W] format
    if len(image.shape) == 2:
        image = image[np.newaxis, :, :]
    proj = dataset.GetProjection()
    geotrans = dataset.GetGeoTransform()
    return image,  geotrans, proj


def save_rasterGeoTIF(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(
        im_height), int(im_bands), datatype)
    if(dataset != None):
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


# def save_rasterArray(im_data, path, image_prototype_path):

#     output = gdal_array.SaveArray(
#         im_data, path, format="GTiff",  prototype=image_prototype_path)
#     return True

def save_rasterArray(im_data, path):

    output = gdal_array.SaveArray(
        im_data, path, format="GTiff")
    return True


def count_files(folder_path):
    count = 0
    for path in Path(folder_path).iterdir():
        if path.is_file():
            count += 1
    return count


def padding_mul_image(img, crop_size, stride):

    D = img.shape[0]  # this one is for (H, W, C) format
    height = img.shape[1]
    width = img.shape[2]
    # get the minial padding image size
    H = int(np.ceil(height/stride)*stride)
    W = int(np.ceil(width/stride)*stride)

    padded_img = np.zeros((D, H, W), dtype=img.dtype)
    for d in range(D):  # padding every layer
        onelayer = img[d, :, :]
        padded_img[d, :, :] = np.pad(
            onelayer, ((0, H - height), (0, W - width)), "reflect"
        )
    # padded_img = np.squeeze(padded_img)  # Remove axes of length one
    return padded_img


def split_image(img_path, save_path, crop_size, repetition_rate=0, overwrite=True):
    # check input image
    img,  geotrans, proj = read_rasterArray(img_path)
    if img is None:
        print("Image not found")
        return None
    # get image suffix
    ext = Path(img_path).suffix
    # check output folder, if not exists, creat it.
    Path(save_path).mkdir(parents=True, exist_ok=True)

    height = img.shape[1]
    width = img.shape[2]
    print(f"Input Image File Shape (D, H, W):{ img.shape}")

    stride = int(crop_size*(1-repetition_rate))
    print(f"{crop_size=}, {stride=}")

    padded_img = padding_mul_image(img, crop_size, stride)

    H = padded_img.shape[1]
    W = padded_img.shape[2]

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
        for n, (h, w) in enumerate(tile_generator()):
            crop_img = padded_img[:, h:h+crop_size, w: w+crop_size]
            crop_image_name = f"{new_name:04d}{ext}"
            crop_image_path = Path(save_path) / crop_image_name
            # save_rasterArray(crop_img,  str(crop_image_path)) # just save the raster image
            save_rasterGeoTIF(crop_img, geotrans, proj, str(crop_image_path))
            new_name = new_name + 1
            pbar.update(1)

    return n+1
