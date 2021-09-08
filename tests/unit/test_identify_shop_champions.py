"""Unit tests to cover functionality of identify_shop_champions, which uses
OCR to identify the five champions within the shop of a TFT screenshot.
"""
import os
from typing import List, Tuple

import pytest
import src.readtft.services.identify_shop_champions as sut
from src.readtft.services.identify_shop_champions import Resolution
from src.readtft.utils import ROOT_DIR


@pytest.fixture(name="images_dir")
def fixture_images_dir() -> os.PathLike:
    return os.path.join(ROOT_DIR, "images")


@pytest.mark.parametrize(
    "height,expected", [(768, (740, 758)), (1001, (965, 991))]
)
def test_get_shop_champs_roi_height(height: int, expected: Tuple[int, int]):
    assert sut._get_shop_champs_roi_height(height) == expected


@pytest.mark.parametrize(
    "height,expected",
    [(720, (694, 710)), (900, (867, 890)), (1440, (1388, 1430))],
)
def test_get_shop_champs_roi_height_w_h_not_mapped(
    height: int, expected: Tuple[int, int]
):
    assert sut._get_shop_champs_roi_height(height) == expected


@pytest.mark.parametrize(
    "w_h,expected",
    [((1024, 768), (174, 276, 141)), ((1904, 1001), (511, 647, 186))],
)
def test_get_shop_champs_roi_width_interval(
    w_h: Tuple[int, int], expected: Tuple[int, int]
):
    resolution: Resolution = {"width": w_h[0], "height": w_h[1]}
    assert sut._get_shop_champs_roi_width_interval(resolution) == expected


@pytest.mark.skip(reason="Estimation not currently implemented")
@pytest.mark.parametrize(
    "w_h,expected",
    [((2560, 1440), (640, 831, 266)), ((3840, 2160), (960, 1247, 398))],
)
def test_get_shop_champs_roi_width_interval_not_mapped(
    w_h: Tuple[int, int], expected: Tuple[int, int]
):
    resolution: Resolution = {"width": w_h[0], "height": w_h[1]}
    assert sut._get_shop_champs_roi_width_interval(resolution) == expected


@pytest.mark.parametrize(
    "screenshot_name,expected",
    [
        ("1600x1024.png", ["Vayne", "Olaf", "Nautilus", "Kha'Zix", "Udyr"]),
        ("1920x1080.png", ["Udyr", "Udyr", "Leona", "Kled", "Vayne"]),
    ],
)
def test_identify_shop_champions(
    screenshot_name: str, expected: List[str], images_dir: os.PathLike
):
    image_path = os.path.join(images_dir, screenshot_name)
    assert sut.identify_shop_champions(str(image_path)) == expected
