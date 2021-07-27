from splitraster import geo
from splitraster import io

# Example A:
# Step 1: set input image file path
input_image_path = "./data/raw/RGB.png"
gt_image_path = "./data/raw/GT.png"

# Step 2: prepare output directory and spliting configuration
save_path = "./data/processed/RGB"
save_path_gt = "./data/processed/GT"

crop_size = 256
repetition_rate = 0
overwrite = False

# step 3: split the RGB images
n = io.split_image(input_image_path, save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {save_path}")

# step 3: split the GT images

n = io.split_image(gt_image_path, save_path_gt, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {gt_image_path} are added at {save_path_gt}")

# Use the RGB and GT folders for your deep learning model.

# Example B:

# Split TIF RGB image
tif_image_path = "./data/raw/TIF/RGB5k.tif"
save_tif_image_path = "./data/processed/RGB_TIF"

n = geo.split_image(tif_image_path, save_tif_image_path,
                    crop_size, repetition_rate, overwrite)

print(f"{n} tiles sample of {tif_image_path} are added at {save_tif_image_path}")

# Split TIF GT image
tif_image_path = "./data/raw/TIF/GT5k.tif"
save_tif_image_path = "./data/processed/GT_TIF"
crop_size = 500
repetition_rate = 0
overwrite = True
n = geo.split_image(tif_image_path, save_tif_image_path,
                    crop_size, repetition_rate, overwrite)

print(f"{n} tiles sample of {tif_image_path} are added at {save_tif_image_path}")
