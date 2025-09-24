"""
SysML v2 Visualization Tools

Three standalone options for visualizing SysML v2 models as SVG diagrams:
1. Kernel Integration - Uses authentic SysML kernel API for 100% accurate visualization
2. Kernel API - Direct access to SysML Jupyter kernel for real-time visualization
3. Enhanced Standalone - Pure Python implementation with no external dependencies
"""

__version__ = "1.0.0"
__author__ = "SysML v2 Visualization Project"

from .kernel_integration import KernelIntegratedSysMLVisualizer
from .kernel_api import SysMLKernelAPI
from .standalone import StandaloneSysMLVisualizer

# Alias for consistency
SysMLKernelVisualizer = SysMLKernelAPI

__all__ = [
    "KernelIntegratedSysMLVisualizer",
    "SysMLKernelAPI",
    "SysMLKernelVisualizer",
    "StandaloneSysMLVisualizer"
]