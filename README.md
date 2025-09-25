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
pip install sysml-v2-visualizer
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
import sys
sys.path.insert(0, 'src')
from kernel_api import SysMLKernelAPI

visualizer = SysMLKernelAPI()
result = visualizer.visualize_file("model.sysml", "output.svg")
print(f"Generated: {result}")
```

## 🎯 SysML Kernel API

**Professional SysML v2 visualization using the official kernel infrastructure**

```python
from sysml_visualizer import SysMLKernelAPI

visualizer = SysMLKernelAPI()
result = visualizer.visualize_file("model.sysml", "output.svg")
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
2. **Choose your method dependencies:**

#### For SysML Kernel API:
```bash
# Install conda if needed
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Install SysML v2 kernel
conda install -c conda-forge sysml

# Verify installation
jupyter kernelspec list  # Should show 'sysml' kernel
```

### Package Installation

```bash
# Install base package
pip install sysml-v2-visualizer

# Install with optional dependencies
pip install sysml-v2-visualizer[kernel]     # For kernel API
pip install sysml-v2-visualizer[dev]        # For development
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
# Kernel API (Recommended)
import sys
sys.path.insert(0, 'src')
from kernel_api import SysMLKernelAPI

visualizer = SysMLKernelAPI()

# Basic file visualization
result = visualizer.visualize_file("model.sysml", "output.svg")
print(f"Generated {Path(result).stat().st_size} byte SVG")

# With view and style options
result = visualizer.visualize_file("model.sysml", "output.svg",
                                  view="Interconnection", style="stdcolor")

# Visualize specific element
result = visualizer.visualize_file("model.sysml", "output.svg",
                                  view="Tree", element="VehicleExample::Vehicle")

# Direct SysML code visualization (interactive)
result = visualizer.visualize("package Demo { part def Vehicle; }",
                             view="Action", style="stdcolor")
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

      - name: Install visualizer
        run: pip install sysml-v2-visualizer[kernel]

      - name: Generate visualizations
        run: |
          for file in models/*.sysml; do
            sysml-visualize "$file" "diagrams/$(basename "$file" .sysml).svg"
          done

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
│   ├── __init__.py              # Package exports
│   ├── kernel_api.py           # SysML Kernel API
│   ├── cli.py                  # Command line interface
│   ├── utils.py                # Utility functions
│   └── sysmlbw.skin           # Authentic SysML skin file
├── examples/                   # Example SysML files and generated SVGs
│   ├── working_vehicle.sysml
│   └── *.svg                  # Generated example visualizations
├── setup.py                    # Package configuration
└── README.md                   # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/redasasin4/SysML_Python_Visualizer.git
cd SysML_Python_Visualizer

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Ensure all tests pass: `pytest`
4. Format code: `black src/`
5. Submit pull request

## 🔧 Troubleshooting

### Common Issues

1. **Kernel Not Found**
   ```bash
   # Verify SysML kernel installation
   jupyter kernelspec list
   conda list sysml

   # Reinstall if needed
   conda install -c conda-forge sysml
   ```

2. **Dependency Check**
   ```bash
   # Check what's available
   sysml-visualize --check-deps

   # Use with verbose output for troubleshooting
   sysml-visualize model.sysml output.svg --verbose
   ```

3. **No SVG Output**
   - Ensure your SysML code defines packages/elements
   - Check that SysML syntax is valid
   - Try the working example first: `sysml-visualizer/examples/working_vehicle.sysml`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


**Generate professional SysML v2 diagrams with confidence!** 🚀