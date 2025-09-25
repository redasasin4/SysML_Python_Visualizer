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


def check_sysml_kernel() -> bool:
    """Check if SysML kernel is installed."""
    try:
        result = subprocess.run(
            ["jupyter", "kernelspec", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "sysml" in result.stdout
    except:
        return False


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
            missing.append("SysML kernel (conda install -c conda-forge sysml)")


    return missing


def print_dependency_status():
    """Print a summary of dependency status."""
    deps = check_dependencies()

    print("📋 Dependency Status:")
    print("=" * 50)

    # Core dependencies
    print("Core Dependencies:")
    status = "✅" if deps['jupyter_client'] else "❌"
    print(f"  {status} jupyter_client")

    # Kernel dependencies
    print("\nKernel Method Dependencies:")
    status = "✅" if deps['conda'] else "❌"
    print(f"  {status} conda")
    status = "✅" if deps['sysml_kernel'] else "❌"
    print(f"  {status} sysml kernel")


    print("\n" + "=" * 50)

    # Recommendations
    available_methods = []
    if deps['jupyter_client'] and deps['sysml_kernel']:
        available_methods.append("kernel-api")

    if available_methods:
        print(f"✅ Available methods: {', '.join(available_methods)}")
    else:
        print("❌ No visualization methods available. Please install dependencies.")

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
            "  conda install -c conda-forge sysml",
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