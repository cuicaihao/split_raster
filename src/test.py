import matplotlib.pyplot as plt
from splitraster import io
import numpy as np
# Test read file
input_image_path = "../data/raw/RGB.png"
gt_image_path = "../data/raw/GT.png"

# img_rgb = io.read_image(input_image_path)
# img_gt = io.read_image(gt_image_path)


# img_gt = img_gt.astype(np.bool)
# img_gt = img_gt.astype(np.uint8)*255

# io.save_image(img_rgb, '../data/processed/RGB.Copy.png')
# io.save_image(img_gt, '../data/processed/GT.Copy.png')

# plt.subplot(1, 2, 1)
# plt.imshow(img_rgb)
# plt.subplot(1, 2, 2)
# plt.imshow(img_gt, cmap='gray')
# plt.show()

# print(img_rgb.min(), img_rgb.max(), img_rgb.dtype)
# print(img_gt.min(), img_gt.max(), img_gt.dtype)

# img_path, save_path, crop_size, repetition_rate=0, overwrite=True

save_path = "../data/processed/RGB"
crop_size = 256
repetition_rate = 0.5
overwrite = False


n = io.split_image(input_image_path, save_path, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {input_image_path} are added at {save_path}")

save_path_gt = "../data/processed/GT"
n = io.split_image(gt_image_path, save_path_gt, crop_size,
                   repetition_rate=repetition_rate, overwrite=overwrite)
print(f"{n} tiles sample of {gt_image_path} are added at {save_path_gt}")
