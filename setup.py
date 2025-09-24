"""
SysML v2 Visualization Tools - Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="sysml-v2-visualizer",
    version="1.0.0",
    author="SysML v2 Visualization Project",
    author_email="",
    description="Three standalone options for visualizing SysML v2 models as SVG diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/sysml-v2-visualizer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "kernel": ["jupyter-client", "ipykernel"],
        "standalone": ["graphviz"],
        "dev": ["pytest", "black", "flake8", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "sysml-visualize=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.skin"],
    },
    keywords="sysml, visualization, systems modeling, plantuml, svg, jupyter",
    project_urls={
        "Bug Reports": "https://github.com/your-org/sysml-v2-visualizer/issues",
        "Source": "https://github.com/your-org/sysml-v2-visualizer",
        "Documentation": "https://github.com/your-org/sysml-v2-visualizer/blob/main/README.md",
    },
)