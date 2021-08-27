"""Base module to run OCR on input screenshot to identify champions within
player's shop.
"""
#!/usr/bin/python3.8

# %%
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from typing import Tuple, TypedDict

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
        (1680, 1001): (965, 990),
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
        (1680, 1001): (398, 535, 187),
    }
    resolution_wh = (resolution["width"], resolution["height"])

    if resolution_wh in resolution_width_roi_mapping:
        return resolution_width_roi_mapping[resolution_wh]
    return (
        0,
        0,
        0,
    )  # TODO(Dan): Return best estimate if resolution isn't mapped


def main():
    matplotlib.rcParams["figure.dpi"] = 300

    # Import the image
    img = plt.imread("../images/1680x1050.png")
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

    for _ in range(NUM_CHAMPS_IN_SHOP):
        roi = img[roi_lo_h:roi_hi_h, roi_lo_w:roi_hi_w]
        text = pytesseract.image_to_string(roi)
        print(text)

        # Optionally add visible rectangle
        cv2.rectangle(
            img, (roi_lo_w, roi_lo_h), (roi_hi_w, roi_hi_h), (0, 0, 255), 2
        )
        roi_lo_w += interval
        roi_hi_w += interval

    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    main()

# %%
