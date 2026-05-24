import importlib
import sys
import types
from pathlib import Path

import numpy as np
import pytest

BASE_DIR = Path(__file__).resolve().parent


def test_rgb_gt_slide_window(tmp_path) -> None:
    from splitraster import io

    input_image_path = BASE_DIR / "data/raw/RGB.png"
    gt_image_path = BASE_DIR / "data/raw/GT.png"
    input_save_path = tmp_path / "RGB"
    gt_save_path = tmp_path / "GT"

    n = io.split_image(
        input_image_path,
        input_save_path,
        crop_size=256,
        repetition_rate=0,
        overwrite=False,
    )
    assert n == 16
    assert len(list(input_save_path.iterdir())) == 16

    n = io.split_image(
        gt_image_path,
        gt_save_path,
        crop_size=256,
        repetition_rate=0,
        overwrite=False,
    )
    assert n == 16
    assert len(list(gt_save_path.iterdir())) == 16


def test_rgb_gt_random_crop_uses_output_folder_count(tmp_path):
    from splitraster import io

    input_image_path = BASE_DIR / "data/raw/RGB.png"
    gt_image_path = BASE_DIR / "data/raw/GT.png"
    save_path = tmp_path / "Rand/RGB"
    save_path_gt = tmp_path / "Rand/GT"
    save_path.mkdir(parents=True)
    save_path_gt.mkdir(parents=True)
    (save_path / "0001.png").touch()
    (save_path_gt / "0001.png").touch()

    n = io.random_crop_image(
        input_image_path,
        save_path,
        gt_image_path,
        save_path_gt,
        crop_size=256,
        crop_number=1,
        img_ext=".png",
        label_ext=".png",
        overwrite=False,
    )

    assert n == 1
    assert (save_path / "0002.png").is_file()
    assert (save_path_gt / "0002.png").is_file()


def test_invalid_repetition_rate_raises(tmp_path):
    from splitraster import io

    input_image_path = BASE_DIR / "data/raw/RGB.png"

    with pytest.raises(ValueError, match="repetition_rate"):
        io.split_image(input_image_path, tmp_path / "RGB", crop_size=256, repetition_rate=1)


def import_geo_with_fake_gdal(monkeypatch):
    fake_gdal = types.SimpleNamespace(
        GA_ReadOnly=0,
        GDT_Byte=1,
        GDT_UInt16=2,
        GDT_Float32=3,
        Open=lambda *args, **kwargs: None,
    )
    fake_gdal_array = types.SimpleNamespace(SaveArray=lambda *args, **kwargs: True)
    fake_osgeo = types.SimpleNamespace(gdal=fake_gdal, gdal_array=fake_gdal_array)

    monkeypatch.setitem(sys.modules, "osgeo", fake_osgeo)
    monkeypatch.setitem(sys.modules, "osgeo.gdal", fake_gdal)
    monkeypatch.setitem(sys.modules, "osgeo.gdal_array", fake_gdal_array)
    sys.modules.pop("splitraster.geo", None)

    return importlib.import_module("splitraster.geo")


def test_geo_read_raster_array_raises_for_missing_file(monkeypatch):
    geo = import_geo_with_fake_gdal(monkeypatch)
    monkeypatch.setattr(geo.gdal, "Open", lambda *args, **kwargs: None)

    with pytest.raises(FileNotFoundError, match="Can not open raster file"):
        geo.read_rasterArray("missing.tif")


def test_geo_random_crop_keeps_image_and_label_order(monkeypatch, tmp_path):
    geo = import_geo_with_fake_gdal(monkeypatch)
    img = np.ones((1, 2, 2), dtype=np.uint8)
    label = np.full((1, 2, 2), 2, dtype=np.uint8)
    saved = []

    def fake_read(path):
        if path == "img.tif":
            return img, ("img-geotrans",), "img-proj"
        if path == "label.tif":
            return label, ("label-geotrans",), "label-proj"
        raise AssertionError(f"unexpected path: {path}")

    def fake_save(data, geotrans, proj, file_name):
        saved.append((data.copy(), geotrans, proj, Path(file_name).name))

    monkeypatch.setattr(geo, "read_rasterArray", fake_read)
    monkeypatch.setattr(geo, "save_rasterGeoTIF", fake_save)

    n = geo.random_crop_image(
        "img.tif",
        tmp_path / "img",
        "label.tif",
        tmp_path / "label",
        crop_size=2,
        crop_number=1,
        overwrite=True,
    )

    assert n == 1
    assert saved[0][1:] == (("img-geotrans",), "img-proj", "0001.tif")
    assert saved[1][1:] == (("label-geotrans",), "label-proj", "0001.tif")
    assert np.array_equal(saved[0][0], img)
    assert np.array_equal(saved[1][0], label)
