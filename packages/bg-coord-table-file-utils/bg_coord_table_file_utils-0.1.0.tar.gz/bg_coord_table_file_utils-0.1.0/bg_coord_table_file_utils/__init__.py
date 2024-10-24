"""Top-level package for BG Coordinate Table File Utils."""

__author__ = """Jaideep Sundaram"""
__email__ = 'sundaram.baylorgenetics@gmail.com'
__version__ = '0.1.0'

from .parser import Parser as CoordTableFileParser
from .record import Record as CoordTableRecord
from .writer import Writer as CoordTableFileWriter
