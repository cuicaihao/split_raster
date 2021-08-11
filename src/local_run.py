# %% Example A: General image seg dataset
from splitraster import geo, io


# %% Example A: General image seg dataset - Slide Window Method
input_image_path = "../data/raw/RGB.png"
gt_image_path = "../data/raw/GT.png"

input_save_path = "../data/processed/RGB"
gt_save_path = "../data/processed/GT"

crop_size = 256
repetition_rate = 0
overwrite = True

n = io.split_image(input_image_path, input_save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {input_save_path}")

n = io.split_image(gt_image_path, gt_save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {gt_image_path} are added at {gt_save_path}")


# %% Example AA: General image seg dataset: Random Sampling Method
input_image_path = "../data/raw/RGB.png"
gt_image_path = "../data/raw/GT.png"

input_save_path = "../data/processed/Rand/RGB"
gt_save_path = "../data/processed/Rand/GT"

n = io.random_crop_image(input_image_path, input_save_path,  gt_image_path, gt_save_path,
                         crop_size=256, crop_number=20, img_ext='.png', label_ext='.png', overwrite=True)

print(f"{n} sample paris of {input_image_path, gt_image_path} are added at {input_save_path, gt_save_path}.")


# %% Example B: Remote Sensing image seg dataset - Slide Window Method

input_tif_image_path = "../data/raw/TIF/RGB5k.tif"
gt_tif_image_path = "../data/raw/TIF/GT5k.tif"

input_save_image_path = "../data/processed/RGB_TIF"
gt_save_image_path = "../data/processed/GT_TIF"

crop_size = 500
repetition_rate = 0
overwrite = True

n = geo.split_image(input_tif_image_path, input_save_image_path,
                    crop_size, repetition_rate, overwrite)

print(f"{n} tiles sample of {input_tif_image_path} are added at {input_save_image_path}")

n = geo.split_image(gt_tif_image_path, gt_save_image_path,
                    crop_size, repetition_rate, overwrite)

print(f"{n} tiles sample of {gt_tif_image_path} are added at {gt_save_image_path}")

# %% Example B: Remote Sensing image seg dataset - Random Sampling Method
input_tif_image_path = "../data/raw/TIF/RGB5k.tif"
gt_tif_image_path = "../data/raw/TIF/GT5k.tif"

input_save_image_path = "../data/processed/Rand/RGB_TIF"
gt_save_image_path = "../data/processed/Rand/GT_TIF"

n = geo.random_crop_image(input_tif_image_path, input_save_image_path,  gt_tif_image_path, gt_save_image_path,
                          crop_size=500, crop_number=20, overwrite=True)

print(f"{n} sample paris of {input_tif_image_path, gt_tif_image_path} are added at {input_save_image_path, gt_save_image_path}.")


# %%


print("PASS")
