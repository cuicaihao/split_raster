from splitraster import geo
from splitraster import io

input_image_path = "./data/raw/RGB.png"
gt_image_path = "./data/raw/GT.png"

save_path = "./data/processed/RGB"
crop_size = 256
repetition_rate = 0
overwrite = True

n = io.split_image(input_image_path, save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {save_path}")

save_path_gt = "./data/processed/GT"
n = io.split_image(gt_image_path, save_path_gt, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {gt_image_path} are added at {save_path_gt}")


tif_image_path = "./data/processed/MUL.tif"
save_tif_image_path = "./data/processed/MUL"
crop_size = 100
repetition_rate = 0
overwrite = True


n = geo.split_image(tif_image_path, save_tif_image_path,
                    crop_size, repetition_rate, overwrite)

print(f"{n} tiles sample of {tif_image_path} are added at {save_tif_image_path}")
