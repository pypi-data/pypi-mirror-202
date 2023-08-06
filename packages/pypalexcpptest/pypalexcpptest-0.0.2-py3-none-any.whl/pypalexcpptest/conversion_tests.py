import numpy
import multiprocessing

from . import conversion_utils as convert


def python_convert_rgb_to_hsv(rgb_img_matrix_2d):
    # Split image array into multiple arrays and remove empty arrays.
    split_rgb_img_arrays = numpy.array_split(rgb_img_matrix_2d, multiprocessing.cpu_count())
    split_rgb_img_arrays = [x for x in split_rgb_img_arrays if x.size > 0]

    # Multi-thread the conversion process from [r,g,b] to [h,s,v].
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    async_result = pool.map_async(process_helper, split_rgb_img_arrays)
    pool.close()
    pool.join()

    converted_hsv_results = []
    for value in async_result.get():
        converted_hsv_results.append(value)

    # Combine and sort all the individual [h,s,v] arrays by 3rd(v), 2nd(s), and then 1st(h) column.
    hsv_matrix_2d = numpy.concatenate(converted_hsv_results)
    hsv_matrix_2d = hsv_matrix_2d[numpy.lexsort((hsv_matrix_2d[:, 2], hsv_matrix_2d[:, 1], hsv_matrix_2d[:, 0]))]

    return hsv_matrix_2d


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Helper function for multiprocessing conversion operations.
#   @details    Helps convert from [r,g,b] to [h,s,v].
#
#   @param  rgb_matrix_2d   A 2D matrix of rgb values.
#
#   @return A numpy array/2D matrix of converted [h,s,v] values.
def process_helper(rgb_matrix_2d):
    return numpy.apply_along_axis(convert.rgb_to_hsv, 1, rgb_matrix_2d)
