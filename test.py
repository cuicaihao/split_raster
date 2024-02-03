#  Test the Packages
#  Example A:
def test_rgb_gt_slide_window() -> None:
    from splitraster import io

    # Step 1: set input image file path
    input_image_path = "./data/raw/RGB.png"
    gt_image_path = "./data/raw/GT.png"

    # Step 2: prepare output directory and spliting configuration
    input_save_path = "./data/processed/RGB"
    gt_save_path = "./data/processed/GT"

    crop_size = 256
    repetition_rate = 0
    overwrite = False

    # step 3: split the RGB images
    n = io.split_image(
        input_image_path,
        input_save_path,
        crop_size,
        repetition_rate=repetition_rate,
        overwrite=overwrite,
    )
    print(f"{n} tiles sample of {input_image_path} are added at {input_save_path}")

    # step 4: split the GT images
    n = io.split_image(
        gt_image_path,
        gt_save_path,
        crop_size,
        repetition_rate=repetition_rate,
        overwrite=overwrite,
    )
    print(f"{n} tiles sample of {gt_image_path} are added at {gt_save_path}")

    # Step 5: Use the RGB and GT folders for your deep learning model.


#  Example B
def test_rgb_gt_random_crop():
    from splitraster import io

    input_image_path = "./data/raw/RGB.png"
    gt_image_path = "./data/raw/GT.png"

    save_path = "./data/processed/Rand/RGB"
    save_path_gt = "./data/processed/Rand/GT"

    n = io.random_crop_image(
        input_image_path,
        save_path,
        gt_image_path,
        save_path_gt,
        crop_size=256,
        crop_number=20,
        img_ext=".png",
        label_ext=".png",
        overwrite=True,
    )

    print(
        f"{n} sample paris of {input_image_path, gt_image_path} are added at {save_path, save_path_gt}"
    )


# #  Example C
# def test_tif_slide_window():
#     from splitraster import geo

#     input_tif_image_path = "./data/raw/TIF/RGB5k.tif"
#     gt_tif_image_path = "./data/raw/TIF/GT5k.tif"

#     input_save_image_path = "./data/processed/RGB_TIF"
#     gt_save_image_path = "./data/processed/GT_TIF"

#     crop_size = 500
#     repetition_rate = 0
#     overwrite = True

#     n = geo.split_image(
#         input_tif_image_path,
#         input_save_image_path,
#         crop_size,
#         repetition_rate,
#         overwrite,
#     )

#     print(
#         f"{n} tiles sample of {input_tif_image_path} are added at {input_save_image_path}"
#     )

#     n = geo.split_image(
#         gt_tif_image_path, gt_save_image_path, crop_size, repetition_rate, overwrite
#     )

#     print(f"{n} tiles sample of {gt_tif_image_path} are added at {gt_save_image_path}")


# #  Example D
# def test_tif_random_sample():
#     from splitraster import geo

#     input_tif_image_path = "./data/raw/TIF/RGB5k.tif"
#     gt_tif_image_path = "./data/raw/TIF/GT5k.tif"

#     input_save_image_path = "./data/processed/Rand/RGB_TIF"
#     gt_save_image_path = "./data/processed/Rand/GT_TIF"

#     n = geo.random_crop_image(
#         input_tif_image_path,
#         input_save_image_path,
#         gt_tif_image_path,
#         gt_save_image_path,
#         crop_size=500,
#         crop_number=20,
#         overwrite=True,
#     )

#     print(
#         f"{n} sample paris of {input_tif_image_path, gt_tif_image_path} are added at {input_save_image_path, gt_save_image_path}."
#     )


print("PASS")
