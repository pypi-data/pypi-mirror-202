##  @file   setup.py
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 11, 2023

import sys
import setuptools

try:
    import pypalexcpptest
except ImportError:
    print("error: pypalexcpptest requires Python 3.6 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pypalexcpptest.__version__
DOWNLOAD = "https://github.com/AlTimofeyev/pypalex_cpp_test/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="pypalexcpptest",
    version=VERSION,
    author="Al Timofeyev",
    author_email="al.timofeyev@outlook.com",
    description="Testing out pypalex with cpp code.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    install_requires=['Pillow', 'numpy', 'filetype'],
    # keywords="python palex color-palette colorscheme extract-colorscheme extract-palette extractor",
    keywords=['python', 'pypalexcpptest'],
    license="MIT",
    url="https://github.com/AlTimofeyev/pypalex_cpp_test",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pypalexcpptest"],
    entry_points={"console_scripts": ["palexcpptest=pypalexcpptest.__main__:main"]},
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False)
