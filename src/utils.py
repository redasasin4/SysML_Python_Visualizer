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
    # Check for plantuml command
    if shutil.which('plantuml'):
        return True

    # Check for plantuml.jar in common locations
    possible_paths = [
        Path.cwd() / "plantuml.jar",
        Path("/usr/share/plantuml/plantuml.jar"),
        Path("/opt/plantuml/plantuml.jar")
    ]

    return any(path.exists() for path in possible_paths)


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

    if method == "kernel-integration":
        if not deps['jupyter_client']:
            missing.append("jupyter_client (pip install jupyter-client)")
        if not deps['sysml_kernel']:
            missing.append("SysML kernel (conda install -c conda-forge sysml)")

    elif method == "kernel-api":
        if not deps['jupyter_client']:
            missing.append("jupyter_client (pip install jupyter-client)")
        if not deps['sysml_kernel']:
            missing.append("SysML kernel (conda install -c conda-forge sysml)")

    elif method == "standalone":
        if not deps['graphviz']:
            missing.append("GraphViz (apt install graphviz / brew install graphviz)")
        if not deps['plantuml']:
            missing.append("PlantUML (apt install plantuml / brew install plantuml)")

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

    # Standalone dependencies
    print("\nStandalone Method Dependencies:")
    status = "✅" if deps['graphviz'] else "❌"
    print(f"  {status} graphviz")
    status = "✅" if deps['plantuml'] else "❌"
    print(f"  {status} plantuml")

    print("\n" + "=" * 50)

    # Recommendations
    available_methods = []
    if deps['jupyter_client'] and deps['sysml_kernel']:
        available_methods.extend(["kernel-integration", "kernel-api"])
    if deps['graphviz'] and deps['plantuml']:
        available_methods.append("standalone")

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

    if "GraphViz" in str(missing):
        suggestions.extend([
            "Install GraphViz:",
            "  # Ubuntu/Debian:",
            "  sudo apt install graphviz",
            "  # macOS:",
            "  brew install graphviz",
            ""
        ])

    if "PlantUML" in str(missing):
        suggestions.extend([
            "Install PlantUML:",
            "  # Ubuntu/Debian:",
            "  sudo apt install plantuml",
            "  # macOS:",
            "  brew install plantuml",
            ""
        ])

    return "\n".join(suggestions)


def ensure_output_directory(output_path: str) -> None:
    """Ensure output directory exists."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    print_dependency_status()