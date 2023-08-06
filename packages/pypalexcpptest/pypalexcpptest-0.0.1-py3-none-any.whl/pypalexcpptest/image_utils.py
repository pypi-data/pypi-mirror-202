##  @file   image_utils.py
#   @brief  Utilities for processing image and file handling.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 27, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on April 5, 2023.


# ---- IMPORTS ----
import numpy
from PIL import Image


##  Processes PIL Image object.
#   @details    Multiprocessing example from: https://stackoverflow.com/a/45555516
#
#   @param  image   PIL Image object.
#
#   @return 2D numpy array of [h,s,v] arrays (pixels) from image.
def process_image(image):
    # Make sure image is in [r,g,b] format.
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Rescale image to reduce data sample.
    new_size = rescale_image(image)
    resized_img = image.resize(new_size, Image.LANCZOS)
    img_matrix_3d = numpy.array(resized_img)

    # Flatten image matrix into 2D.
    rgb_img_matrix_2d = img_matrix_3d.reshape(-1, 3)

    return rgb_img_matrix_2d


# **************************************************************************
# **************************************************************************

##  Rescales image to a smaller sampling size.
#
#   @param  image   PIL Image object.
#
#   @return Tuple of the new width and height of image.
def rescale_image(image):
    width, height = image.size
    default_480p = [854, 480]   # 480p SD resolution with 16:9 ratio.
    default_360p = [640, 360]   # 360p SD resolution with 16:9 ratio.

    # Try scaling images down to 480p with 16:9 ratio.
    if height < width:      # ---- Landscape, 16:9 ratio.
        percent_change_width = default_480p[0] / width
        percent_change_height = default_480p[1] / height
    elif width < height:    # ---- Portrait, 9:16 ratio.
        percent_change_width = default_480p[1] / width
        percent_change_height = default_480p[0] / height
    else:                   # ---- Square, 1:1 ratio.
        percent_change_width = default_360p[0] / width
        percent_change_height = default_360p[0] / height

    width *= percent_change_width
    height *= percent_change_height

    return round(width), round(height)
