# SysML v2 Visualization Tools

Python package for generating authentic SVG diagrams from SysML v2 models using the official SysML Jupyter kernel infrastructure.

## 🎯 Features

- **🔥 Official SysML Kernel API** - Direct integration with the SysML v2 kernel
- **✨ 100% Authentic Output** - Uses official SysML v2 kernel infrastructure
- **🚀 Auto-Discovery Mode** - Automatically finds and processes all .sysml files in your repository
- **📦 Professional Package** - Easy installation with `pip install`
- **🖥️ Advanced CLI Interface** - Full kernel view types, styles, and element selection
- **🎨 Rich Visualization Options** - Tree, Interconnection, Action, State, Sequence, Case, MIXED views
- **🔧 Dependency Management** - Automatic dependency checking and guidance
- **📚 Comprehensive Documentation** - Examples and usage guides included

## 📋 Quick Start

### Installation

```bash
# Install UV (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up the project
git clone <your-repo-url>
cd sysml-v2-visualizer

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Basic Usage

```bash
# Check dependencies
sysml-visualize --check-deps

# Auto-discovery mode - Finds all .sysml files automatically
sysml-visualize output.svg --element "VehicleExample::Vehicle"
sysml-visualize output.svg --element "PackageName::ElementName" --view Interconnection
sysml-visualize output.svg --element "MyPackage" --view Tree --style stdcolor
```

### Python API

```python
from sysml_v2_visualizer import SysMLKernelAPI

visualizer = SysMLKernelAPI()
result = visualizer.visualize_file("output.svg")  # Auto-discovers all .sysml files
print(f"Generated: {result}")
```

## 🎯 SysML Kernel API

**Professional SysML v2 visualization using the official kernel infrastructure**

```python
from sysml_v2_visualizer import SysMLKernelAPI

visualizer = SysMLKernelAPI()
result = visualizer.visualize_file("output.svg")  # Auto-discovers all .sysml files
```

**Features:**
- ✅ **100% Authentic** - Uses official SysML v2 kernel API
- ✅ **Complete SysML syntax** - Full `comp def`, `comp usage`, `skin sysmlbw` support
- ✅ **PSysML protocol** - Full UUID linking support
- ✅ **Full CLI support** - All kernel view types, styles, and element selection
- ✅ **Interactive development** - Direct Jupyter kernel access
- ✅ **Rich visualization** - Tree, Interconnection, Action, State, Sequence, Case, MIXED views

**Requirements:**
- SysML conda kernel (`conda install -c conda-forge sysml`)
- jupyter-client (`pip install jupyter-client`)

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
conda install -c conda-forge sysml

# Verify installation
jupyter kernelspec list  # Should show 'sysml' kernel
```

#### 3. Set up the Project
```bash
# Clone the repository
git clone <your-repo-url>
cd sysml-v2-visualizer

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

## 🚀 Usage Examples

### Command Line Interface

```bash
# Check dependencies
sysml-visualize --check-deps

# Auto-discovery mode (finds all .sysml files in repo)
sysml-visualize output.svg --element "VehicleExample::Vehicle"
sysml-visualize output.svg --element "PackageName::ElementName" --view Interconnection
sysml-visualize output.svg --element "MyPackage" --view Tree --style stdcolor

# With different views and styles
sysml-visualize output.svg --view Action --style stdcolor --element "PackageName::ElementName"

# Verbose output for debugging
sysml-visualize output.svg --element "VehicleExample::Vehicle" --verbose

# Show help
sysml-visualize --help
```

### Advanced Visualization Options

The SysML kernel API supports the full range of official SysML v2 visualization options:

#### Available Views
```bash
# Tree view (default) - Hierarchical structure
sysml-visualize output.svg --view Tree

# Interconnection view - Shows relationships and connections
sysml-visualize output.svg --view Interconnection

# Action view - Focuses on action elements and flows
sysml-visualize output.svg --view Action

# State view - State-based diagrams
sysml-visualize output.svg --view State

# Sequence view - Sequence diagrams
sysml-visualize output.svg --view Sequence

# Case view - Use case scenarios
sysml-visualize output.svg --view Case

# Mixed view - Combination of multiple views
sysml-visualize output.svg --view MIXED
```

#### Styling Options
```bash
# Standard color scheme
sysml-visualize output.svg --view Tree --style stdcolor

# Custom styles (as supported by kernel)
sysml-visualize output.svg --view Interconnection --style custom
```

#### Element-Specific Visualization
```bash
# Visualize entire package
sysml-visualize output.svg --element "VehicleExample"

# Visualize specific part definition
sysml-visualize output.svg --element "VehicleExample::Vehicle"

# Combine with views and styles
sysml-visualize output.svg --view Action --style stdcolor --element "VehicleExample::Vehicle"
```

### Python API Examples

```python
# Import from the package
from sysml_v2_visualizer import SysMLKernelAPI
from pathlib import Path

visualizer = SysMLKernelAPI()

# Auto-discovery visualization (finds all .sysml files)
result = visualizer.visualize_file("output.svg")
print(f"Generated {Path(result).stat().st_size} byte SVG")

# With view and style options
result = visualizer.visualize_file("output.svg",
                                  view="Interconnection", style="stdcolor")

# Visualize specific element
result = visualizer.visualize_file("output.svg",
                                  view="Tree", element="VehicleExample::Vehicle")

# Direct SysML code visualization (interactive)
api = SysMLKernelAPI()
api.start_kernel()
try:
    outputs = api.visualize("package Demo { part def Vehicle; }",
                           view="Action", style="stdcolor")
finally:
    api.stop_kernel()
```

## 📖 Command Reference

### Available View Types

The SysML Kernel API supports the full range of official SysML v2 visualization views:

- **Default**: Default kernel view
- **Tree** (default): Hierarchical structure view showing element relationships
- **Interconnection**: Relationship and connection diagrams
- **Action**: Behavioral elements and action flows
- **State**: State machine diagrams and state transitions
- **Sequence**: Sequence diagrams showing interactions over time
- **Case**: Use case scenarios and case-based views
- **MIXED**: Combined view types for comprehensive visualization

### Available Styles

The SysML Kernel API supports various styling options to enhance visual presentation:

- **stdcolor**: Standard color scheme for improved readability
- **sysmlbw**: Black and white SysML styling (built-in)
- **monochrome**: Monochrome styling option
- **Custom styles**: Any style supported by the underlying PlantUML/SysML kernel


### CLI Options Reference

#### Visualization Options
- `--view <VIEW_TYPE>`: Specify visualization view type (see Available View Types)
- `--style <STYLE>`: Apply styling options (see Available Styles)
- `--element <ELEMENT_PATH>`: Target specific model element
  - Package level: `"VehicleExample"`
  - Element level: `"VehicleExample::Vehicle"`
  - Nested elements: `"VehicleExample::Vehicle::Engine"`

#### Utility Options
- `--verbose`: Enable verbose output for debugging
- `--check-deps`: Verify dependencies and show available methods
- `--help`: Display help information

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
        run: conda install -c conda-forge sysml

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
sysml-v2-visualizer/
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
git clone <your-repo-url>
cd sysml-v2-visualizer

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

### Common Issues

#### 1. **Kernel Not Found / Path Issues**

The most common issue is that the SysML kernel is installed but not accessible due to PATH or environment issues.

**Diagnostic commands:**
```bash
# Check dependency status (basic)
sysml-visualize --check-deps

# Run comprehensive diagnostics (advanced)
sysml-visualize --diagnose

# Manual checks
which jupyter
which conda
jupyter kernelspec list

# Try different paths if jupyter not in PATH
~/miniconda/bin/jupyter kernelspec list
~/anaconda/bin/jupyter kernelspec list
```

**Common solutions:**

a) **Add conda to PATH:**
```bash
# Find your conda installation
ls ~/miniconda/bin/conda || ls ~/anaconda/bin/conda

# Add to PATH (replace with your actual path)
export PATH="$HOME/miniconda/bin:$PATH"
# or
export PATH="$HOME/anaconda/bin:$PATH"

# Make permanent by adding to ~/.bashrc or ~/.zshrc
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
```

b) **Activate conda environment:**
```bash
# Activate base conda environment
conda activate base
# or use full path
~/miniconda/bin/conda activate base

# Then verify kernel
jupyter kernelspec list
```

c) **Reinstall kernel with full paths:**
```bash
# Use full conda path if conda not in PATH
~/miniconda/bin/conda install -c conda-forge sysml
# or
~/anaconda/bin/conda install -c conda-forge sysml
```

#### 2. **SysML Kernel Installation Issues**

```bash
# Verify SysML kernel installation
jupyter kernelspec list  # Should show 'sysml' kernel
conda list sysml          # Should show sysml package

# If kernel missing, reinstall
conda install -c conda-forge sysml

# If conda missing, install miniconda/miniforge first
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

#### 3. **Environment/Virtual Environment Issues**

```bash
# Make sure you're in the UV virtual environment
source .venv/bin/activate

# Verify package installation
python -c "from sysml_v2_visualizer import SysMLKernelAPI; print('✅ Package works')"

# Check dependency status with enhanced diagnostics
sysml-visualize --check-deps
```

#### 4. **Permission/Access Issues**

```bash
# Check file permissions on conda installation
ls -la ~/miniconda/bin/jupyter ~/miniconda/bin/conda

# If permission issues, try:
chmod +x ~/miniconda/bin/jupyter ~/miniconda/bin/conda

# Or reinstall with proper permissions
bash Miniforge3-$(uname)-$(uname -m).sh
```

#### 5. **Multiple Conda/Python Installations**

```bash
# Check which python/conda you're using
which python
which conda
which jupyter

# List all python installations
ls -la /usr/bin/python* ~/miniconda/bin/python* ~/anaconda/bin/python*

# Ensure consistency - all should point to same conda installation
```

#### 6. **Debugging with Verbose Output**

```bash
# Run comprehensive system diagnostics
sysml-visualize --diagnose

# Run with verbose output for troubleshooting
sysml-visualize output.svg --verbose --element "YourPackage::YourElement"

# Check if .sysml files are found
ls -la *.sysml **/*.sysml
```

#### 7. **No SVG Output**
   - Ensure your SysML code defines packages/elements
   - Check that SysML syntax is valid
   - Verify .sysml files exist in current directory or subdirectories
   - Try different view types: `--view Tree`, `--view Interconnection`

### Getting Help

If issues persist:
1. Run `sysml-visualize --diagnose` and share the output
2. Include your OS, conda version, and installation method
3. Check if the issue exists in a fresh conda environment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


**Generate professional SysML v2 diagrams with confidence!** 🚀