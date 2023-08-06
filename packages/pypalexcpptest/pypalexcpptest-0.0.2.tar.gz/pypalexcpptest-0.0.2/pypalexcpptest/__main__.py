# ---- IMPORTS ----
import sys
import os
import time
import argparse
import filetype
from PIL import Image

from .settings import __version__, CONF_DIR
from . import image_utils as imutils
from . import arg_messages as argmsg
from . import conversion_tests as tests


# ---- GLOBAL VARIABLES ----
## List of Extractor class objects for each individual image.
EXTRACTORS = []
## List of real/existing image file path(s).
PROPER_IMAGES = []
## List of image filenames.
FILENAMES = []


##  Main script function.
def main():
    handle_args()

    for index, image_dir in enumerate(PROPER_IMAGES):
        print("Processing ", FILENAMES[index], " : ",  sep='', end='')
        image = Image.open(image_dir)
        rgb_img_matrix_2d = imutils.process_image(image)
        print("COMPLETED")
        print("Running python test : ", sep='', end='')
        start = time.time()
        # python conversion test here
        python_hsv_array = tests.python_convert_rgb_to_hsv(rgb_img_matrix_2d)
        end = time.time()
        print("COMPLETED \t Time Elapsed:", (end-start))
        print("Running cpp test : ", sep='', end='')
        start = time.time()
        # cpp conversion test here
        end = time.time()
        print("COMPLETED \t Time Elapsed:", (end - start))


# **************************************************************************
# **************************************************************************

##  Handles the arguments passed to PyPalEx.
def handle_args():
    # Converts arguments into a dictionary: {'files': None, 'path': None, 'output': None}
    argument_parser = setup_argument_parser()
    args = vars(argument_parser.parse_args())

    # Check if pypalex version was requested.
    if args['version']:
        print("pypalexcpptest ", __version__, sep="")
        sys.exit()

    # Exit if no files/paths were provided.
    if (args['files'] is None or args['files'] == []) and args['path'] is None:
        sys.exit(argmsg.no_args_help_message())

    # Check either the file(s) or the file(s) in the path
    # to make sure there are valid images to work with.
    if args['files']:
        if not check_sources(args['files'], args['path']):
            sys.exit(argmsg.bad_source_message())
    elif args['path'] is not None:
        if not check_path(args['path']):
            sys.exit(argmsg.bad_path_message())
        args['files'] = os.listdir(args['path'])
        if not check_sources(args['files'], args['path']):
            sys.exit(argmsg.bad_source_message())

    set_global_args(args)


# **************************************************************************
# **************************************************************************

##  Sets up the argument parser for command line arguments.
#
#   @return A command line argument parsing object.
def setup_argument_parser():
    desc = "PyPalEx is a color palette extraction tool "
    desc += "for extracting light, normal and dark color "
    desc += "palettes from images into json files.\n"

    argument_parser = argparse.ArgumentParser(description=desc, usage="palex [options][arguments]")

    argument_parser.add_argument("-f", "--files", metavar="FILES", type=str, nargs="*",
                                 help="Specify the absolute file path(s). "
                                      "If used with -p --path option, you only need to specify the relative file path(s).")
    argument_parser.add_argument("-p", "--path", metavar="", type=str,
                                 help="Specify the path from where to use images. "
                                      "Absolute path is preferred, but relative path can also be used.")
    argument_parser.add_argument("-v", "--version", action="store_true",
                                 help="Prints the PyPalEx version.")

    return argument_parser


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Checks each of the sources provided and removes any bad sources.
#   @details    Any filepaths or source files that are not images or
#               do not exist get removed.
#
#   @param  filepaths   List of file paths.
#   @param  path        A path to the images, if it is provided.
#
#   @return True if all/some sources are good, False if all sources are bad.
def check_sources(filepaths, path=None):
    bad_source_paths = []
    for filepath in filepaths:
        source_filepath = filepath
        if path is not None:
            source_filepath = os.path.join(path, filepath)
        if not check_source(source_filepath):
            bad_source_paths.append(filepath)

    # Remove all the bad source paths from filepaths.
    for bad_source in bad_source_paths:
        filepaths.remove(bad_source)

    if len(filepaths) == 0:
        return False

    bad_source_paths.clear()

    # Check to make sure the remaining files are images.
    for filepath in filepaths:
        image_filepath = filepath
        if path is not None:
            image_filepath = os.path.join(path, filepath)
        if not filetype.is_image(image_filepath):
            bad_source_paths.append(filepath)
        else:
            try:
                Image.open(image_filepath)
            except IOError:
                bad_source_paths.append(filepath)

    # Remove all the bad images from filepaths.
    for bad_source in bad_source_paths:
        filepaths.remove(bad_source)

    # Return true if there are proper images that can be used.
    return len(filepaths) != 0


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Check the path to make sure it exists.
#
#   @param  path    The path to a directory.
#
#   @return True if the path exists and is not a file, False otherwise.
def check_path(path):
    return os.path.exists(path) and not os.path.isfile(path)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Sets the global variables using the arguments.
#
#   @param  args    User-supplied arguments.
def set_global_args(args):
    global PROPER_IMAGES
    global FILENAMES

    args_path = args['path']

    for image_path in args['files']:
        filepath, filename = os.path.split(image_path)
        filename, extension = filename.split('.')
        if args_path is not None:
            if filepath == '':
                filepath = args_path
            else:
                filepath = os.path.join(args_path, filepath)
        FILENAMES.append(filename)
        PROPER_IMAGES.append(os.path.join(filepath, filename) + "." + extension)


# **************************************************************************
# **************************************************************************

##  Checks to make sure the path leads to a file.
#
#   @param  filepath    Path to file with filename and file extension.
#
#   @return True if file exists, False otherwise.
def check_source(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


# **************************************************************************
# ************** MAIN ************** MAIN ************** MAIN **************
# **************************************************************************
if __name__ == '__main__':
    main()
