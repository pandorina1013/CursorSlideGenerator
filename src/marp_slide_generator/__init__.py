"""Marp Slide Generator - A tool for creating well-organized Marp presentations"""

from .page_splitter import PageSplitter
from .marp_formatter import MarpFormatter
from .slide_generator import SlideGenerator

__version__ = "0.1.0"
__all__ = ["PageSplitter", "MarpFormatter", "SlideGenerator"] 