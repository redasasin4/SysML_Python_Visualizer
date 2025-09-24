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
    verbose: bool = False
) -> bool:
    """
    Visualize a SysML file using the specified method.

    Args:
        input_file: Path to input SysML file
        output_file: Path to output SVG file
        method: Visualization method ('kernel-integration', 'kernel-api', 'standalone')
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

        result_path = visualizer.visualize_file(input_file, output_file)

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
  sysml-visualize model.sysml output.svg
  sysml-visualize model.sysml output.svg --method standalone
  sysml-visualize model.sysml output.svg --method kernel-api --verbose
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

    # Perform visualization
    success = visualize_file(
        args.input_file,
        args.output_file,
        args.method,
        args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()