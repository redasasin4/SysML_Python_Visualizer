"""
SysML v2 Visualization Tools

Professional Python package for generating authentic SVG diagrams from SysML v2 models
using the official SysML Jupyter kernel infrastructure.
"""

__version__ = "1.0.0"
__author__ = "SysML v2 Visualization Project"

from .kernel_api import SysMLKernelAPI

# Alias for consistency
SysMLKernelVisualizer = SysMLKernelAPI

__all__ = [
    "SysMLKernelAPI",
    "SysMLKernelVisualizer",
]