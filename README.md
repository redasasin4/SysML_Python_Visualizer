# SysML v2 Visualization Tools

Python package for generating authentic SVG diagrams from SysML v2 models using the official SysML Jupyter kernel infrastructure.

## ✨ Features

**Core Functionality**
- **Official SysML v2 Integration** - Direct access to the official SysML Jupyter kernel
- **Authentic Diagram Generation** - 100% compatible with SysML v2 specifications
- **Intelligent File Discovery** - Automatically processes all .sysml files in your project

**User Experience**
- **Professional CLI Interface** - Complete command-line tool with advanced options
- **Multiple Visualization Views** - Tree, Interconnection, Action, State, Sequence, Case, and Mixed views
- **Flexible Styling Options** - Standard colors, monochrome, and custom themes

**Developer Experience**
- **Smart Dependency Detection** - Automatic system kernel path discovery and setup
- **Enhanced Troubleshooting** - Comprehensive diagnostics with `--diagnose` command
- **Modern Python Packaging** - UV-compatible with proper virtual environment support

## 📋 Quick Start

```bash
# Install UV and dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
conda install -c conda-forge jupyter-sysml-kernel

# Clone and set up the project
git clone https://github.com/redasasin4/SysML_Python_Visualizer.git
cd SysML_Python_Visualizer
uv venv && source .venv/bin/activate && uv pip install -e .

# Basic usage
sysml-visualize --check-deps
sysml-visualize output.svg --element "VehicleExample::Vehicle"
```

## 🎯 SysML Kernel API

Professional SysML v2 visualization using the official kernel infrastructure with 100% authentic diagram generation.

**Features:**
- ✅ **Official Integration** - Uses SysML v2 kernel API with full syntax support
- ✅ **Rich Visualization** - Tree, Interconnection, Action, State, Sequence, Case, MIXED views
- ✅ **Intelligent Discovery** - Automatically processes all .sysml files
- ✅ **Professional CLI** - Complete command-line tool with advanced options

## 📦 Installation

### Prerequisites

1. **Python 3.8+**
2. **UV Package Manager** (recommended)
3. **SysML Kernel Dependencies**

### Step-by-Step Setup

#### 1. Install UV
```bash
# Install UV (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to your PATH (or restart terminal)
export PATH="$HOME/.local/bin:$PATH"
```

#### 2. Install SysML Kernel
```bash
# Install conda if needed
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Install SysML v2 kernel
conda install -c conda-forge jupyter-sysml-kernel

# Verify installation
jupyter kernelspec list  # Should show 'sysml' kernel
```

#### 3. Set up the Project
```bash
# Clone the repository
git clone https://github.com/redasasin4/SysML_Python_Visualizer.git
cd SysML_Python_Visualizer

# Create virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install project in editable mode
uv pip install -e .

# Install with development dependencies (optional)
uv pip install -e . --group dev
```

### **✨ Automatic Kernel Detection**

The tool now automatically detects SysML kernels installed system-wide! No manual `JUPYTER_PATH` setup needed:

```bash
# Just check if everything is detected
sysml-visualize --check-deps

# See detailed auto-detection info
sysml-visualize --diagnose
```

**Supported installation paths:**
- `/miniforge3`, `/miniconda3`, `/anaconda3`
- `~/miniconda`, `~/anaconda`, `~/miniforge`
- `/opt/conda`, `/usr/local/conda`
- User-level: `~/.local/share/jupyter`

## 🚀 Usage

### Command Line Interface

```bash
# Basic usage with auto-discovery
sysml-visualize output.svg --element "VehicleExample::Vehicle"
sysml-visualize output.svg --element "PackageName" --view Interconnection --style stdcolor

# Available views: Tree (default), Interconnection, Action, State, Sequence, Case, MIXED
sysml-visualize output.svg --view Action --element "PackageName::ElementName"

# Debugging and utilities
sysml-visualize --check-deps
sysml-visualize output.svg --verbose --element "YourElement"
```

### Python API

```python
from sysml_v2_visualizer import SysMLKernelAPI

# Basic usage
visualizer = SysMLKernelAPI()
result = visualizer.visualize_file("output.svg")

# With options
result = visualizer.visualize_file("output.svg",
                                  view="Interconnection",
                                  style="stdcolor",
                                  element="VehicleExample::Vehicle")

# Interactive usage
api = SysMLKernelAPI()
api.start_kernel()
try:
    outputs = api.visualize("package Demo { part def Vehicle; }")
finally:
    api.stop_kernel()
```

## 📖 Command Reference

### CLI Options
- `--view <VIEW>`: Tree (default), Interconnection, Action, State, Sequence, Case, MIXED
- `--style <STYLE>`: stdcolor, sysmlbw, monochrome, or custom styles
- `--element <PATH>`: Target specific elements (`"Package"` or `"Package::Element"`)
- `--verbose`: Enable detailed output
- `--check-deps`: Verify installation
- `--diagnose`: Run comprehensive diagnostics

### CI/CD Integration

#### GitHub Actions

```yaml
name: Generate SysML Diagrams
on: [push, pull_request]

jobs:
  visualize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Miniconda
        uses: conda-incubator/setup-miniconda@v2
        with:
          miniconda-version: "latest"
          python-version: "3.9"

      - name: Install SysML kernel
        shell: bash -l {0}
        run: conda install -c conda-forge jupyter-sysml-kernel

      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Set up project
        run: |
          export PATH="$HOME/.local/bin:$PATH"
          uv venv
          source .venv/bin/activate
          uv pip install -e .

      - name: Generate visualizations
        run: |
          # Auto-discovery mode - processes all .sysml files
          sysml-visualize "diagrams/all-models.svg"

      - name: Upload diagrams
        uses: actions/upload-artifact@v3
        with:
          name: sysml-diagrams
          path: diagrams/
```

## 📁 Project Structure

```
SysML_Python_Visualizer/
├── src/
│   └── sysml_v2_visualizer/    # Main package
│       ├── __init__.py         # Package exports
│       ├── kernel_api.py       # SysML Kernel API
│       ├── cli.py              # Command line interface
│       ├── utils.py            # Utility functions
│       └── sysmlbw.skin       # Authentic SysML skin file
├── examples/                   # Example SysML files and generated SVGs
│   ├── working_vehicle.sysml
│   └── *.svg                  # Generated example visualizations
├── pyproject.toml              # Modern package configuration
├── uv.lock                     # Dependency lock file
├── .venv/                      # Virtual environment (created by uv)
└── README.md                   # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/redasasin4/SysML_Python_Visualizer.git
cd SysML_Python_Visualizer

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install project with development dependencies
uv pip install -e . --group dev

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Ensure all tests pass: `pytest`
4. Format code: `black src/`
5. Submit pull request

## 🔧 Troubleshooting

### Quick Diagnostics
```bash
sysml-visualize --check-deps    # Basic dependency check
sysml-visualize --diagnose      # Comprehensive system diagnostics
```

### Common Issues

**Kernel Not Found:**
- Tool automatically detects conda installations in common paths
- If issues persist: `export PATH="$HOME/miniconda/bin:$PATH"`
- Verify: `jupyter kernelspec list` (should show 'sysml' kernel)

**Missing Dependencies:**
```bash
conda install -c conda-forge jupyter-sysml-kernel
source .venv/bin/activate && uv pip install -e .
```

**No SVG Output:**
- Ensure .sysml files exist in directory
- Check SysML syntax is valid
- Try different views: `--view Tree`, `--view Interconnection`
- Use `--verbose` for detailed debugging

### Getting Help

If issues persist, run `sysml-visualize --diagnose` and share the output along with your OS and conda version.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


**Generate professional SysML v2 diagrams with confidence!** 🚀