#!/usr/bin/env python3
"""
SysML v2 Visualization Tools - Command Line Interface

Provides command-line access to SysML v2 visualization using the Kernel API method.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from .kernel_api import SysMLKernelAPI
    from .utils import validate_method_dependencies, suggest_installation_commands, print_dependency_status, find_sysml_files, combine_sysml_files
except ImportError:
    from kernel_api import SysMLKernelAPI
    from utils import validate_method_dependencies, suggest_installation_commands, print_dependency_status, find_sysml_files, combine_sysml_files


def visualize_file(
    output_file: str,
    view: Optional[str] = None,
    style: Optional[str] = None,
    element: Optional[str] = None,
    verbose: bool = False
) -> bool:
    """
    Visualize SysML files using the SysML Kernel API with auto-discovery.

    Args:
        output_file: Path to output SVG file
        view: Visualization view type
        style: Visualization style
        element: Specific element to visualize
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    try:
        visualizer = SysMLKernelAPI()

        # Auto-discover all .sysml files
        sysml_files = find_sysml_files()
        if not sysml_files:
            print("❌ No .sysml files found in current directory or subdirectories")
            return False

        if verbose:
            print(f"Auto-discovered {len(sysml_files)} .sysml files:")
            for f in sysml_files:
                print(f"  - {f}")

        # Combine all files
        combined_content = combine_sysml_files(sysml_files)

        if verbose:
            print("Using SysML Kernel API to visualize all discovered files")

        # Prepare visualization options
        kwargs = {}
        if view:
            kwargs['view'] = view
        if style:
            kwargs['style'] = style
        if element:
            kwargs['element'] = element

        # Use visualize_content instead of visualize_file
        result_path = visualizer.visualize_content(combined_content, output_file, **kwargs)

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
        description="SysML v2 Visualization Tools - Generate authentic SVG diagrams from SysML files using the official SysML Jupyter kernel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-discovery mode (finds all .sysml files in repo)
  sysml-visualize output.svg --element "VehicleExample::Vehicle"
  sysml-visualize output.svg --element "PackageName::ElementName" --view Interconnection
  sysml-visualize output.svg --element "MyPackage" --view Tree --style stdcolor

Available views: Default, Tree, State, Interconnection, Action, Sequence, Case, MIXED
Available styles: stdcolor, sysmlbw, monochrome, (and custom kernel styles)
        """
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help="Output SVG file path"
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

    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Run detailed diagnostics for troubleshooting"
    )

    # Visualization options
    parser.add_argument(
        "--view",
        choices=["Default", "Tree", "State", "Interconnection", "Action", "Sequence", "Case", "MIXED"],
        help="Visualization view type"
    )

    parser.add_argument(
        "--style",
        help="Visualization style, e.g., 'stdcolor'"
    )

    parser.add_argument(
        "--element",
        help="Specific element to visualize, e.g., 'PackageName::ElementName'"
    )

    args = parser.parse_args()

    # Check dependencies if requested
    if args.check_deps:
        available_methods = print_dependency_status()
        sys.exit(0)

    # Run detailed diagnostics if requested
    if args.diagnose:
        from .utils import get_kernel_diagnostics
        import json

        print("🔬 Detailed Diagnostics:")
        print("=" * 50)

        diagnostics = get_kernel_diagnostics()

        print(f"System Information:")
        print(f"  OS: {sys.platform}")
        print(f"  Python: {sys.version}")

        print(f"\nPath Information:")
        print(f"  jupyter in PATH: {diagnostics['jupyter_in_path']}")
        print(f"  jupyter executable: {diagnostics['jupyter_executable']}")
        print(f"  conda path: {diagnostics['conda_path']}")

        print(f"\nJupyter Environment:")
        print(f"  JUPYTER_PATH: {diagnostics['jupyter_path_env']}")
        if diagnostics['system_kernel_paths']:
            print(f"  System kernel paths found:")
            for path in diagnostics['system_kernel_paths']:
                print(f"    {path}")
        else:
            print(f"  No system kernel paths detected")

        print(f"\nKernel Information:")
        print(f"  SysML kernel found: {diagnostics['sysml_kernel_found']}")

        if diagnostics['kernel_list_output']:
            print(f"\nAvailable kernels:")
            for line in diagnostics['kernel_list_output'].split('\n'):
                line = line.strip()
                if line and not line.startswith('Available'):
                    print(f"  {line}")

        if diagnostics['error_messages']:
            print(f"\nErrors encountered:")
            for error in diagnostics['error_messages']:
                print(f"  • {error}")

        print(f"\nEnvironment Variables:")
        import os
        relevant_vars = ['PATH', 'CONDA_DEFAULT_ENV', 'CONDA_PREFIX', 'JUPYTER_PATH']
        for var in relevant_vars:
            value = os.environ.get(var, 'Not set')
            if var == 'PATH':
                # Split PATH for readability
                paths = value.split(':') if value != 'Not set' else []
                print(f"  {var}:")
                for p in paths[:10]:  # Show first 10 paths
                    print(f"    {p}")
                if len(paths) > 10:
                    print(f"    ... and {len(paths) - 10} more paths")
            else:
                print(f"  {var}: {value}")

        sys.exit(0)

    # Ensure output_file is provided for visualization operations
    if not args.output_file:
        parser.error("output_file is required for visualization operations")

    # Validate kernel dependencies
    missing_deps = validate_method_dependencies("kernel-api")
    if missing_deps:
        print(suggest_installation_commands("kernel-api"))
        sys.exit(1)

    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Perform visualization
    success = visualize_file(
        args.output_file,
        args.view,
        args.style,
        args.element,
        args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()