"""Base module to run OCR on input screenshot to identify champions within
player's shop.
"""
# %%
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from typing import List, Tuple, TypedDict

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract

NUM_CHAMPS_IN_SHOP = 5


class Resolution(TypedDict):
    width: int
    height: int


def _get_shop_champs_roi_height(resolution: Resolution) -> Tuple[int, int]:
    """Returns shop's champion names ROI height based on resolution.

    Height is assumed to be uniform, so output tuple contains the lower/upper
    bounds of all champions' name heights.

    Args:
        resolution: Resolution object containing source width/height of image.

    Returns:
        Tuple containing the lower, then upper boundaries of the image's
        region of interest, i.e. champions' names only, excluding gold value.
    """
    resolution_height_roi_mapping = {
        (1024, 768): (740, 758),
        (1152, 864): (833, 854),
        (1280, 720): (694, 710),
        (1280, 768): (740, 758),
        (1280, 800): (771, 790),
        (1280, 960): (925, 950),
        (1280, 1001): (965, 991),
        (1360, 768): (740, 758),
        (1366, 768): (740, 758),
        (1440, 900): (867, 890),
        (1600, 900): (867, 890),
        (1600, 1001): (965, 991),
        (1680, 1001): (965, 991),
        (1904, 1001): (965, 991),
    }
    resolution_wh = (resolution["width"], resolution["height"])

    if resolution_wh in resolution_height_roi_mapping:
        return resolution_height_roi_mapping[resolution_wh]
    return (0, 0)  # TODO(Dan): Return best estimate if resolution isn't mapped


def _get_shop_champs_roi_width_interval(
    resolution: Resolution,
) -> Tuple[int, int, int]:
    """Returns shop's champion names ROI width/interval based on resolution.

    Function will specifically return the left/right bounds of the first
    champion name in the shop, with the interval being the distance between
    the left bound of the first champion name, and the left bound of the second
    champion name.

    Args:
        resolution: Resolution object containing source width/height of image.

    Returns:
        Tuple containing the left, then right bounds of the first champion name
        in the shop, followed by the distance between the start of the first
        champion name and the second champion name.
    """
    resolution_width_roi_mapping = {
        (1024, 768): (174, 276, 141),
        (1152, 864): (195, 311, 160),
        (1280, 720): (322, 418, 134),
        (1280, 768): (301, 405, 142),
        (1280, 800): (287, 394, 150),
        (1280, 960): (217, 346, 179),
        (1280, 1001): (199, 333, 186),
        (1360, 768): (340, 446, 143),
        (1366, 768): (340, 446, 143),
        (1440, 900): (324, 446, 166),
        (1600, 900): (404, 524, 166),
        (1600, 1001): (359, 494, 186),
        (1680, 1001): (398, 535, 186),
        (1904, 1001): (511, 647, 186),
    }
    resolution_wh = (resolution["width"], resolution["height"])

    if resolution_wh in resolution_width_roi_mapping:
        return resolution_width_roi_mapping[resolution_wh]
    return (
        0,
        0,
        0,
    )  # TODO(Dan): Return best estimate if resolution isn't mapped


def identify_shop_champions(img_path: str) -> List[str]:
    """Identifies the names of the five champions presented in the shop.

    Args:
        img_path: Path of image to identify champions within.

    Returns:
        List of names for the five champions identified within the shop.
    """
    matplotlib.rcParams["figure.dpi"] = 300

    # Import the image
    img = plt.imread(img_path)
    img_h, img_w, _ = img.shape
    # >>> print(img_h, img_w)
    # 1001 1680

    img = (img * 255).astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(
        img,
        150,
        255,
        cv2.THRESH_BINARY_INV,
    )

    resolution: Resolution = {"width": img_w, "height": img_h}
    roi_lo_h, roi_hi_h = _get_shop_champs_roi_height(resolution)
    roi_lo_w, roi_hi_w, interval = _get_shop_champs_roi_width_interval(
        resolution
    )

    champion_names = []

    for _ in range(NUM_CHAMPS_IN_SHOP):
        roi = img[roi_lo_h:roi_hi_h, roi_lo_w:roi_hi_w]
        text = pytesseract.image_to_string(roi)
        champion_names.append(text)

        # Optionally add visible rectangle
        cv2.rectangle(
            img, (roi_lo_w, roi_lo_h), (roi_hi_w, roi_hi_h), (0, 0, 255), 2
        )
        roi_lo_w += interval
        roi_hi_w += interval

    plt.imshow(img)
    plt.show()

    return champion_names


# %%
