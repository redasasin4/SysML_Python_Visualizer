#!/usr/bin/env python3
"""
SysML v2 Visualization Tools - Command Line Interface

Provides command-line access to all three visualization options:
1. Kernel Integration (--method kernel-integration)
2. Kernel API (--method kernel-api)
3. Enhanced Standalone (--method standalone)
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .kernel_integration import KernelIntegratedSysMLVisualizer
from .kernel_api import SysMLKernelAPI
from .standalone import StandaloneSysMLVisualizer
from .utils import validate_method_dependencies, suggest_installation_commands, print_dependency_status


def visualize_file(
    input_file: str,
    output_file: str,
    method: str = "kernel-integration",
    view: Optional[str] = None,
    style: Optional[str] = None,
    element: Optional[str] = None,
    verbose: bool = False
) -> bool:
    """
    Visualize a SysML file using the specified method.

    Args:
        input_file: Path to input SysML file
        output_file: Path to output SVG file
        method: Visualization method ('kernel-integration', 'kernel-api', 'standalone')
        view: Visualization view type (kernel methods only)
        style: Visualization style (kernel methods only)
        element: Specific element to visualize (kernel methods only)
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    try:
        if method == "kernel-integration":
            visualizer = KernelIntegratedSysMLVisualizer()
        elif method == "kernel-api":
            visualizer = SysMLKernelAPI()
        elif method == "standalone":
            visualizer = StandaloneSysMLVisualizer()
        else:
            print(f"Error: Unknown method '{method}'")
            return False

        if verbose:
            print(f"Using {method} method to visualize {input_file}")

        # Prepare kwargs for kernel methods
        kwargs = {}
        if method in ["kernel-integration", "kernel-api"]:
            if view:
                kwargs['view'] = view
            if style:
                kwargs['style'] = style
            if element:
                kwargs['element'] = element

        result_path = visualizer.visualize_file(input_file, output_file, **kwargs)

        if Path(result_path).exists():
            file_size = Path(result_path).stat().st_size
            print(f"✅ Success! Generated {file_size} byte SVG: {result_path}")
            return True
        else:
            print(f"❌ Failed to generate SVG file")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SysML v2 Visualization Tools - Generate SVG diagrams from SysML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available methods:
  kernel-integration  Uses authentic SysML kernel API (recommended)
  kernel-api         Direct access to SysML Jupyter kernel
  standalone         Pure Python implementation (no dependencies)

Examples:
  # Basic usage
  sysml-visualize model.sysml output.svg
  sysml-visualize model.sysml output.svg --method standalone

  # Advanced visualization options (kernel methods only)
  sysml-visualize model.sysml output.svg --method kernel-api --view Interconnection
  sysml-visualize model.sysml output.svg --method kernel-integration --view Tree --style stdcolor
  sysml-visualize model.sysml output.svg --method kernel-api --element "VehicleExample::Vehicle"
  sysml-visualize model.sysml output.svg --view Action --style stdcolor --element "PackageName"

Available views (kernel methods): Default, Tree, State, Interconnection, Action, Sequence, Case, MIXED
Available styles (kernel methods): stdcolor, sysmlbw, monochrome, (and custom kernel styles)
        """
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input SysML file path"
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help="Output SVG file path"
    )

    parser.add_argument(
        "--method", "-m",
        choices=["kernel-integration", "kernel-api", "standalone"],
        default="kernel-integration",
        help="Visualization method (default: kernel-integration)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="SysML v2 Visualizer 1.0.0"
    )

    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check dependency status and exit"
    )

    # Advanced visualization options (kernel methods only)
    parser.add_argument(
        "--view",
        choices=["Default", "Tree", "State", "Interconnection", "Action", "Sequence", "Case", "MIXED"],
        help="Visualization view type (kernel methods only)"
    )

    parser.add_argument(
        "--style",
        help="Visualization style, e.g., 'stdcolor' (kernel methods only)"
    )

    parser.add_argument(
        "--element",
        help="Specific element to visualize, e.g., 'PackageName::ElementName' (kernel methods only)"
    )

    args = parser.parse_args()

    # Check dependencies if requested
    if args.check_deps:
        available_methods = print_dependency_status()
        sys.exit(0)

    # Validate required arguments for visualization
    if not args.input_file or not args.output_file:
        print("Error: Both input_file and output_file are required for visualization")
        parser.print_help()
        sys.exit(1)

    # Validate method dependencies
    missing_deps = validate_method_dependencies(args.method)
    if missing_deps:
        print(suggest_installation_commands(args.method))
        sys.exit(1)

    # Validate input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file does not exist: {args.input_file}")
        sys.exit(1)

    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Validate advanced options are only used with kernel methods
    if (args.view or args.style or args.element) and args.method == "standalone":
        print("Warning: --view, --style, and --element options are ignored for standalone method")

    # Perform visualization
    success = visualize_file(
        args.input_file,
        args.output_file,
        args.method,
        args.view,
        args.style,
        args.element,
        args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()