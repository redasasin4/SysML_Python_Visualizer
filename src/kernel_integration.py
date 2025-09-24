"""
SysML Kernel Integration - Option 1 Implementation

This module uses the SysML kernel API to achieve 100% authentic
SysML visualization with official kernel processing.
"""

import subprocess
import shutil
import os
import re
from pathlib import Path
from typing import Optional, Union


def find_conda_path() -> Optional[str]:
    """Find conda installation path."""
    # Check common conda paths
    possible_paths = [
        Path.home() / "miniconda" / "bin",
        Path.home() / "anaconda" / "bin",
        Path.home() / "miniforge" / "bin",
        Path.home() / "mambaforge" / "bin",
        Path("/opt/conda/bin"),
        Path("/usr/local/conda/bin")
    ]

    for path in possible_paths:
        if path.exists() and (path / "conda").exists():
            return str(path)

    # Check if conda is already in PATH
    try:
        result = subprocess.run(["which", "conda"], capture_output=True, text=True)
        if result.returncode == 0:
            conda_path = Path(result.stdout.strip()).parent
            return str(conda_path)
    except:
        pass

    return None


class KernelIntegratedSysMLVisualizer:
    """SysML visualizer using authentic kernel API integration."""

    def __init__(self, kernel_api_module: Optional[str] = None):
        """
        Initialize the kernel integrated visualizer.

        Args:
            kernel_api_module: Path to kernel API module. If None, will search for it.
        """
        # Find kernel API module
        if kernel_api_module:
            self.kernel_api_path = Path(kernel_api_module)
        else:
            # Look for kernel_api module in same package
            possible_locations = [
                Path(__file__).parent / "kernel_api.py",
                Path.cwd() / "src" / "kernel_api.py"
            ]

            self.kernel_api_path = None
            for path in possible_locations:
                if path.exists():
                    self.kernel_api_path = path
                    break

            if not self.kernel_api_path:
                raise RuntimeError(
                    "Kernel API module not found. Please install the full sysml-visualizer package "
                    "or provide the path to the kernel API module."
                )

    def visualize_file(self, sysml_file: Union[str, Path], output_file: Union[str, Path],
                      view: str = "Tree", style: str = None, element: str = None) -> str:
        """
        Visualize SysML file using authentic kernel API integration.

        Args:
            sysml_file: Path to SysML source file
            output_file: Path for output SVG file
            view: Visualization view type ('Tree', 'Interconnection', 'Graph', 'Dependencies')
            style: Visualization style (e.g., 'stdcolor')
            element: Specific element to visualize (e.g., 'Package::Element')

        Returns:
            Path to generated SVG file

        Raises:
            FileNotFoundError: If SysML file doesn't exist
            RuntimeError: If visualization fails
        """
        sysml_path = Path(sysml_file)
        output_path = Path(output_file)

        if not sysml_path.exists():
            raise FileNotFoundError(f"SysML file not found: {sysml_file}")

        print(f"🔧 Using authentic kernel API integration...")
        return self._render_via_kernel_api(str(sysml_path), str(output_path), view, style, element)

    def _render_via_kernel_api(self, sysml_file_path: str, output_path: str,
                              view: str = "Tree", style: str = None, element: str = None) -> str:
        """Render SysML using authentic kernel API with specified visualization options."""

        try:
            print(f"   Reading SysML file: {sysml_file_path}")
            with open(sysml_file_path, 'r') as f:
                original_sysml = f.read()

            # Extract package name from original content
            package_pattern = r'package\s+(\w+)'
            match = re.search(package_pattern, original_sysml)

            if match:
                package_name = match.group(1)
                print(f"   Found package: {package_name}")
            else:
                print(f"   No package found, proceeding anyway...")

            # Prepare kernel API command
            kernel_api_cmd = [
                "python", str(self.kernel_api_path), "viz_file", sysml_file_path, output_path
            ]

            # Add view option
            kernel_api_cmd.extend(["--view", view])

            # Add style option if specified
            if style:
                kernel_api_cmd.extend(["--style", style])

            # Add element option if specified
            if element:
                kernel_api_cmd.extend(["--element", element])

            print(f"   Command: {' '.join(kernel_api_cmd)}")

            # Set up environment with conda path
            env = os.environ.copy()
            conda_path = find_conda_path()
            if conda_path:
                env['PATH'] = f"{conda_path}:{env.get('PATH', '')}"
                print(f"   Using conda from: {conda_path}")
            else:
                print(f"   Warning: conda not found, using system PATH")

            print(f"   Executing kernel API command...")
            result = subprocess.run(
                kernel_api_cmd,
                capture_output=True,
                text=True,
                timeout=60,
                env=env,
                cwd=str(self.kernel_api_path.parent)
            )

            if result.returncode == 0:
                # Check if kernel_output.svg was created
                kernel_svg = self.kernel_api_path.parent / "kernel_output.svg"
                if kernel_svg.exists():
                    # Copy to our output path
                    shutil.copy(str(kernel_svg), output_path)
                    svg_size = Path(output_path).stat().st_size
                    print(f"✅ Success with kernel API integration! Generated {svg_size} byte SVG")
                    return output_path
                else:
                    raise RuntimeError("Kernel API succeeded but no SVG output found")
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                raise RuntimeError(f"Kernel API failed: {error_msg}")

        except Exception as e:
            raise RuntimeError(f"Kernel integration failed: {e}")


def test_kernel_integration():
    """Test the kernel-integrated visualizer."""
    print("🧪 Testing Kernel-Integrated SysML Visualizer")
    print("=" * 60)

    try:
        visualizer = KernelIntegratedSysMLVisualizer()

        # Test with our working example file
        sysml_file = "examples/working_vehicle.sysml"
        output_file = "kernel_integrated_output.svg"

        result_path = visualizer.visualize_file(sysml_file, output_file)

        if Path(result_path).exists():
            svg_size = Path(result_path).stat().st_size
            print(f"🎯 Success! Generated {svg_size} byte SVG")
            print(f"📁 Output: {result_path}")
        else:
            print(f"❌ Failed to generate SVG")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_kernel_integration()