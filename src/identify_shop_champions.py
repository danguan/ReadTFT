"""Base module to run OCR on input screenshot to identify players/HP totals.
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
    return (0, 0)  # TODO(Dan): Return best estimate if resolution isn't mapped


def main():
    matplotlib.rcParams["figure.dpi"] = 300

    base_resolution_h = 1011
    base_resolution_w = 1680

    # Manually defined tuples for low and high values for height and width
    # Used to substitute cropping
    # Height/width calculated for base resolution
    roi_height = (975, 1000)
    # TODO: Use first width tuple as a starting point to find spacing between
    # boxes, based on screenshot size or screen resolution
    roi_widths = (390, 530), (580, 720), (770, 910), (960, 1100), (1150, 1290)

    # Import the image
    img = plt.imread("../images/Screen19.png")
    img_h, img_w, _ = img.shape

    img = (img * 255).astype(np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(
        img,
        150,
        255,
        cv2.THRESH_BINARY_INV,
    )
    for (roi_lo_w, roi_hi_w) in roi_widths:
        lo_h = img_h * roi_height[0] // base_resolution_h
        hi_h = img_h * roi_height[1] // base_resolution_h
        lo_w = img_w * roi_lo_w // base_resolution_w
        hi_w = img_w * roi_hi_w // base_resolution_w
        roi = img[lo_h:hi_h, lo_w:hi_w]
        text = pytesseract.image_to_string(roi)
        print(text)
        cv2.rectangle(img, (lo_w, lo_h), (hi_w, hi_h), (0, 0, 255), 2)

    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    main()

# %%
