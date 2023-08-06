"""`wring `: A tool to compress multiple CSV data files into parquet"""

__author__ = "Jeff Newman <jeff@newman.me>"
from ._version import __version__, __version_tuple__  # noqa
from ._app import app  # noqa
from .tar_zst import tarzst, untarzst  # noqa
from .csv import csv  # noqa
