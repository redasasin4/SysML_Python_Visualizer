"""
Utility functions for SysML v2 Visualization Tools
"""

import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional, Dict, List


class DependencyError(Exception):
    """Raised when a required dependency is not found."""
    pass


def check_dependencies() -> Dict[str, bool]:
    """
    Check for required and optional dependencies.

    Returns:
        Dictionary with dependency names as keys and availability as boolean values
    """
    dependencies = {}

    # Check Python packages
    try:
        import jupyter_client
        dependencies['jupyter_client'] = True
    except ImportError:
        dependencies['jupyter_client'] = False

    # Check for conda
    dependencies['conda'] = bool(find_conda_path())

    # Check for SysML kernel
    dependencies['sysml_kernel'] = check_sysml_kernel()

    # Check for graphviz executable
    dependencies['graphviz'] = shutil.which('dot') is not None

    # Check for PlantUML
    dependencies['plantuml'] = check_plantuml()

    return dependencies


def find_conda_path() -> Optional[str]:
    """Find conda installation path."""
    import platform

    # Check if conda is already in PATH first (most reliable)
    conda_executable = shutil.which("conda")
    if conda_executable:
        return str(Path(conda_executable).parent)

    # Check common conda paths based on platform
    possible_paths = []

    # Cross-platform user directories
    possible_paths.extend([
        Path.home() / "miniconda" / "bin",
        Path.home() / "anaconda" / "bin",
        Path.home() / "miniforge" / "bin",
        Path.home() / "mambaforge" / "bin",
    ])

    # Platform-specific system paths
    system = platform.system().lower()
    if system == "linux":
        possible_paths.extend([
            Path("/opt/conda/bin"),
            Path("/usr/local/conda/bin"),
            Path("/usr/local/miniconda/bin"),
            Path("/usr/local/anaconda/bin")
        ])
    elif system == "darwin":  # macOS
        possible_paths.extend([
            Path("/opt/conda/bin"),
            Path("/usr/local/conda/bin"),
            Path("/usr/local/miniconda/bin"),
            Path("/usr/local/anaconda/bin")
        ])
    elif system == "windows":
        # Windows conda installations
        possible_paths.extend([
            Path.home() / "miniconda" / "Scripts",
            Path.home() / "anaconda" / "Scripts",
            Path.home() / "miniforge" / "Scripts",
            Path.home() / "mambaforge" / "Scripts",
        ])
        # Add potential system-wide installations
        for drive in ['C:', 'D:']:
            possible_paths.extend([
                Path(f"{drive}/miniconda/Scripts"),
                Path(f"{drive}/anaconda/Scripts"),
                Path(f"{drive}/ProgramData/miniconda/Scripts"),
                Path(f"{drive}/ProgramData/anaconda/Scripts")
            ])

    for path in possible_paths:
        conda_exe = "conda.exe" if system == "windows" else "conda"
        if path.exists() and (path / conda_exe).exists():
            return str(path)

    return None


def find_jupyter_executable() -> Optional[str]:
    """Find jupyter executable, checking both PATH and conda installations."""
    import platform

    # First check if jupyter is in PATH
    jupyter_exe = shutil.which("jupyter")
    if jupyter_exe:
        return jupyter_exe

    # If not in PATH, check conda installations
    conda_path = find_conda_path()
    if conda_path:
        system = platform.system().lower()
        jupyter_exe = "jupyter.exe" if system == "windows" else "jupyter"
        jupyter_path = Path(conda_path) / jupyter_exe
        if jupyter_path.exists():
            return str(jupyter_path)

    # Check common conda environment paths
    possible_jupyter_paths = []
    system = platform.system().lower()
    jupyter_exe = "jupyter.exe" if system == "windows" else "jupyter"

    # Check user conda environments
    conda_envs = [
        Path.home() / "miniconda" / "envs",
        Path.home() / "anaconda" / "envs",
        Path.home() / "miniforge" / "envs",
        Path.home() / "mambaforge" / "envs",
    ]

    for env_base in conda_envs:
        if env_base.exists():
            for env_dir in env_base.iterdir():
                if env_dir.is_dir():
                    bin_dir = env_dir / ("Scripts" if system == "windows" else "bin")
                    jupyter_path = bin_dir / jupyter_exe
                    if jupyter_path.exists():
                        possible_jupyter_paths.append(str(jupyter_path))

    # Return first found jupyter executable
    if possible_jupyter_paths:
        return possible_jupyter_paths[0]

    return None


def find_system_kernel_paths() -> List[str]:
    """Find common system kernel installation paths."""
    import platform

    potential_paths = []
    system = platform.system().lower()

    # Common conda installation paths
    conda_bases = [
        Path.home() / "miniconda",
        Path.home() / "miniconda3",
        Path.home() / "anaconda",
        Path.home() / "anaconda3",
        Path.home() / "miniforge",
        Path.home() / "miniforge3",
        Path.home() / "mambaforge",
        Path.home() / "mambaforge3",
        Path("/opt/conda"),
        Path("/usr/local/conda"),
        Path("/opt/miniconda"),
        Path("/opt/miniconda3"),
        Path("/opt/anaconda"),
        Path("/opt/anaconda3"),
        Path("/opt/miniforge"),
        Path("/opt/miniforge3"),
        Path("/opt/mambaforge"),
        Path("/opt/mambaforge3"),
    ]

    # Add system-wide paths
    if system == "linux":
        conda_bases.extend([
            Path("/usr/share/miniconda"),
            Path("/usr/share/anaconda"),
            Path("/usr/local/miniconda"),
            Path("/usr/local/anaconda"),
        ])
    elif system == "darwin":  # macOS
        conda_bases.extend([
            Path("/usr/local/miniconda"),
            Path("/usr/local/anaconda"),
            Path("/Applications/miniconda"),
            Path("/Applications/anaconda"),
        ])

    # Also check for absolute paths like /miniforge3
    absolute_conda_paths = [
        Path("/miniforge3"),
        Path("/miniconda3"),
        Path("/anaconda3"),
        Path("/opt/miniforge3"),
        Path("/opt/miniconda3"),
        Path("/opt/anaconda3"),
    ]
    conda_bases.extend(absolute_conda_paths)

    # Look for jupyter kernel directories in each conda installation
    for conda_base in conda_bases:
        if conda_base.exists():
            kernel_path = conda_base / "share" / "jupyter"
            if kernel_path.exists():
                potential_paths.append(str(kernel_path))

    # Also use the conda path we already discovered via find_conda_path()
    conda_path = find_conda_path()
    if conda_path:
        # conda_path is like "/home/user/miniforge3/bin", we want "/home/user/miniforge3/share/jupyter"
        conda_base = Path(conda_path).parent
        kernel_path = conda_base / "share" / "jupyter"
        if kernel_path.exists() and str(kernel_path) not in potential_paths:
            potential_paths.append(str(kernel_path))

    # Also check user-level jupyter paths
    user_jupyter_paths = [
        Path.home() / ".local" / "share" / "jupyter",
        Path.home() / ".jupyter",
    ]

    for user_path in user_jupyter_paths:
        if user_path.exists():
            potential_paths.append(str(user_path))

    return potential_paths


def setup_jupyter_environment():
    """Automatically set up JUPYTER_PATH to include system kernels."""
    import os

    system_paths = find_system_kernel_paths()
    if not system_paths:
        return

    # Get current JUPYTER_PATH
    current_path = os.environ.get('JUPYTER_PATH', '')

    # Build new JUPYTER_PATH with system paths
    new_paths = []
    for path in system_paths:
        if path not in current_path:
            new_paths.append(path)

    if new_paths:
        if current_path:
            new_jupyter_path = ':'.join(new_paths) + ':' + current_path
        else:
            new_jupyter_path = ':'.join(new_paths)

        os.environ['JUPYTER_PATH'] = new_jupyter_path


def check_sysml_kernel() -> bool:
    """Check if SysML kernel is installed using various jupyter paths and auto-setup."""
    # First, try to set up jupyter environment automatically
    setup_jupyter_environment()

    jupyter_paths = []

    # Try jupyter in PATH first
    if shutil.which("jupyter"):
        jupyter_paths.append("jupyter")

    # Try finding jupyter in conda installations
    jupyter_exe = find_jupyter_executable()
    if jupyter_exe and jupyter_exe not in jupyter_paths:
        jupyter_paths.append(jupyter_exe)

    # Try each jupyter executable
    for jupyter_path in jupyter_paths:
        try:
            result = subprocess.run(
                [jupyter_path, "kernelspec", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "sysml" in result.stdout:
                return True
        except (subprocess.SubprocessError, FileNotFoundError, PermissionError):
            continue

    return False


def get_kernel_diagnostics() -> Dict[str, any]:
    """Get detailed diagnostics about kernel detection."""
    import os

    # Set up jupyter environment first
    setup_jupyter_environment()

    diagnostics = {
        'jupyter_in_path': shutil.which("jupyter") is not None,
        'jupyter_executable': find_jupyter_executable(),
        'conda_path': find_conda_path(),
        'system_kernel_paths': find_system_kernel_paths(),
        'jupyter_path_env': os.environ.get('JUPYTER_PATH', 'Not set'),
        'sysml_kernel_found': False,
        'kernel_list_output': None,
        'error_messages': []
    }

    jupyter_paths = []
    if diagnostics['jupyter_in_path']:
        jupyter_paths.append("jupyter")
    if diagnostics['jupyter_executable']:
        jupyter_paths.append(diagnostics['jupyter_executable'])

    for jupyter_path in jupyter_paths:
        try:
            result = subprocess.run(
                [jupyter_path, "kernelspec", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                diagnostics['kernel_list_output'] = result.stdout
                if "sysml" in result.stdout:
                    diagnostics['sysml_kernel_found'] = True
                    break
            else:
                diagnostics['error_messages'].append(f"Error with {jupyter_path}: {result.stderr}")
        except Exception as e:
            diagnostics['error_messages'].append(f"Exception with {jupyter_path}: {str(e)}")

    return diagnostics


def check_plantuml() -> bool:
    """Check if PlantUML is available."""
    import platform

    # Check for plantuml command in PATH first (most reliable)
    if shutil.which('plantuml'):
        return True

    # Check for plantuml.jar in common locations based on platform
    possible_paths = []

    # Current working directory (universal)
    possible_paths.append(Path.cwd() / "plantuml.jar")

    # Platform-specific paths
    system = platform.system().lower()
    if system == "linux":
        possible_paths.extend([
            Path("/usr/share/plantuml/plantuml.jar"),
            Path("/opt/plantuml/plantuml.jar"),
            Path("/usr/local/share/plantuml/plantuml.jar"),
            Path("/usr/local/plantuml/plantuml.jar")
        ])
    elif system == "darwin":  # macOS
        possible_paths.extend([
            Path("/usr/local/share/plantuml/plantuml.jar"),
            Path("/opt/plantuml/plantuml.jar"),
            Path("/usr/local/plantuml/plantuml.jar"),
            # Homebrew locations
            Path("/usr/local/Cellar/plantuml"),  # Will need to check subdirs
            Path("/opt/homebrew/Cellar/plantuml")  # Apple Silicon
        ])
    elif system == "windows":
        # Common Windows installation directories
        for drive in ['C:', 'D:']:
            possible_paths.extend([
                Path(f"{drive}/plantuml/plantuml.jar"),
                Path(f"{drive}/Program Files/plantuml/plantuml.jar"),
                Path(f"{drive}/Program Files (x86)/plantuml/plantuml.jar")
            ])

    # Check each path
    for path in possible_paths:
        if path.exists():
            return True
        # For directories like Homebrew Cellar, check for plantuml.jar in subdirectories
        if path.is_dir() and "Cellar" in str(path):
            for jar_file in path.rglob("plantuml.jar"):
                if jar_file.exists():
                    return True

    return False


def validate_method_dependencies(method: str) -> List[str]:
    """
    Validate dependencies for a specific visualization method.

    Args:
        method: Visualization method name

    Returns:
        List of missing dependencies (empty if all satisfied)
    """
    deps = check_dependencies()
    missing = []

    if method == "kernel-api":
        if not deps['jupyter_client']:
            missing.append("jupyter_client (pip install jupyter-client)")
        if not deps['sysml_kernel']:
            missing.append("SysML kernel (conda install -c conda-forge jupyter-sysml-kernel)")


    return missing


def print_dependency_status():
    """Print a comprehensive summary of dependency status with diagnostics."""
    deps = check_dependencies()
    diagnostics = get_kernel_diagnostics()

    print("📋 Dependency Status:")
    print("=" * 50)

    # Core dependencies
    print("Core Dependencies:")
    status = "✅" if deps['jupyter_client'] else "❌"
    print(f"  {status} jupyter_client")

    # Kernel dependencies with enhanced diagnostics
    print("\nKernel Method Dependencies:")
    status = "✅" if deps['conda'] else "❌"
    conda_path = diagnostics['conda_path']
    if conda_path:
        print(f"  {status} conda (found at: {conda_path})")
    else:
        print(f"  {status} conda")

    # Jupyter executable status
    status = "✅" if diagnostics['jupyter_in_path'] else "❌"
    print(f"  {status} jupyter in PATH")

    if diagnostics['jupyter_executable']:
        if not diagnostics['jupyter_in_path']:
            print(f"      ℹ️  jupyter found at: {diagnostics['jupyter_executable']}")

    # SysML kernel status with detailed diagnostics
    status = "✅" if deps['sysml_kernel'] else "❌"
    print(f"  {status} sysml kernel")

    # If kernel not found, provide detailed diagnostics
    if not deps['sysml_kernel']:
        print("\n🔍 Kernel Diagnostics:")
        if not diagnostics['jupyter_executable'] and not diagnostics['jupyter_in_path']:
            print("  ❌ No jupyter executable found")
            print("     💡 Try: conda install -c conda-forge jupyter")
        else:
            if diagnostics['error_messages']:
                print("  ❌ Errors encountered:")
                for error in diagnostics['error_messages']:
                    print(f"     • {error}")

            if diagnostics['kernel_list_output']:
                print("  📋 Available kernels:")
                for line in diagnostics['kernel_list_output'].split('\n'):
                    line = line.strip()
                    if line and not line.startswith('Available kernels'):
                        print(f"     • {line}")

                if 'sysml' not in diagnostics['kernel_list_output'].lower():
                    print("  ❌ SysML kernel not found in available kernels")
                    print("     💡 Try: conda install -c conda-forge jupyter-sysml-kernel")

    print("\n" + "=" * 50)

    # Recommendations with enhanced suggestions
    available_methods = []
    if deps['jupyter_client'] and deps['sysml_kernel']:
        available_methods.append("kernel-api")

    if available_methods:
        print(f"✅ Available methods: {', '.join(available_methods)}")
    else:
        print("❌ No visualization methods available.")
        print("\n💡 Troubleshooting suggestions:")

        if not deps['conda']:
            print("  1. Install conda/miniconda:")
            print("     curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh")
            print("     bash Miniforge3-$(uname)-$(uname -m).sh")

        if not deps['sysml_kernel']:
            if deps['conda'] or conda_path:
                print("  2. Install SysML kernel:")
                print("     conda install -c conda-forge jupyter-sysml-kernel")
                if conda_path and not diagnostics['jupyter_in_path']:
                    print(f"     # Or use full path: {conda_path}/conda install -c conda-forge jupyter-sysml-kernel")

            if not diagnostics['jupyter_in_path'] and conda_path:
                print("  3. Add conda to PATH or activate environment:")
                print(f"     export PATH=\"{conda_path}:$PATH\"")
                print("     # Or activate base environment: conda activate base")

    return available_methods


def suggest_installation_commands(method: str) -> str:
    """
    Suggest installation commands for missing dependencies.

    Args:
        method: Visualization method name

    Returns:
        String with installation suggestions
    """
    missing = validate_method_dependencies(method)

    if not missing:
        return f"✅ All dependencies for {method} are satisfied!"

    suggestions = [
        f"❌ Missing dependencies for {method}:",
        ""
    ]

    if "jupyter_client" in str(missing):
        suggestions.extend([
            "Install Jupyter Client:",
            "  pip install jupyter-client",
            ""
        ])

    if "SysML kernel" in str(missing):
        suggestions.extend([
            "Install SysML Kernel:",
            "  conda install -c conda-forge jupyter-sysml-kernel",
            ""
        ])


    return "\n".join(suggestions)


def ensure_output_directory(output_path: str) -> None:
    """Ensure output directory exists."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def find_sysml_files() -> List[str]:
    """
    Find all .sysml files in the current directory and subdirectories.

    Returns:
        List of absolute paths to .sysml files
    """
    sysml_files = []
    for sysml_file in Path.cwd().rglob("*.sysml"):
        sysml_files.append(str(sysml_file.absolute()))
    return sorted(sysml_files)


def combine_sysml_files(file_paths: List[str]) -> str:
    """
    Read and combine multiple SysML files into a single string.

    Args:
        file_paths: List of paths to SysML files

    Returns:
        Combined SysML content
    """
    combined_content = []
    for file_path in file_paths:
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            combined_content.append(f"// From file: {file_path}")
            combined_content.append(content)
            combined_content.append("")  # Add blank line between files
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")

    return "\n".join(combined_content)


if __name__ == "__main__":
    print_dependency_status()