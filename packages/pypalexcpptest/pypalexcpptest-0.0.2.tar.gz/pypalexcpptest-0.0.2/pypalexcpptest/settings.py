##  @file   settings.py
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 11, 2023


import os
import platform

__version__ = "0.0.2"
__cache_version__ = "1.0.0"

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
XDG_CACHE_DIR = os.getenv("XDG_CACHE_HOME", os.path.join(HOME, ".cache"))
XDG_CONF_DIR = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))

CACHE_DIR = os.getenv("PYPALEXCPPTEST_CACHE_DIR", os.path.join(XDG_CACHE_DIR, "palexcpptest"))
CONF_DIR = os.getenv("PYPALEXCPPTEST_CONFIG_DIR", os.path.join(XDG_CONF_DIR, "palexcpptest"))
MODULE_DIR = os.path.dirname(__file__)

OS = platform.uname()[0]
