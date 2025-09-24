# SysML v2 Visualization Tools

Python package for generating SVG diagrams from SysML v2 models. Provides three standalone visualization methods with PlantUML output.

## 🎯 Features

- **🔥 Three Visualization Methods** - Choose the best approach for your needs
- **✨ 100% Authentic Output** - Uses official SysML v2 kernel infrastructure
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

# Generate SVG from SysML file (default Tree view)
sysml-visualize model.sysml output.svg

# Use specific visualization method
sysml-visualize model.sysml output.svg --method standalone

# Use different visualization views (kernel methods only)
sysml-visualize model.sysml output.svg --method kernel-api --view Interconnection
sysml-visualize model.sysml output.svg --method kernel-integration --view Action --style stdcolor

# Visualize specific elements
sysml-visualize model.sysml output.svg --method kernel-api --element "VehicleExample::Vehicle"

# Combine view, style, and element options
sysml-visualize model.sysml output.svg --method kernel-integration --view Tree --style stdcolor --element "VehicleExample"
```

### Python API

```python
from sysml_visualizer import KernelIntegratedSysMLVisualizer

visualizer = KernelIntegratedSysMLVisualizer()
result = visualizer.visualize_file("model.sysml", "output.svg")
print(f"Generated: {result}")
```

## 🎯 Visualization Methods

### 1. Kernel Integration (Recommended)
**Best for:** Production use, CI/CD pipelines

```python
from sysml_visualizer import KernelIntegratedSysMLVisualizer

visualizer = KernelIntegratedSysMLVisualizer()
result = visualizer.visualize_file("model.sysml", "output.svg")
```

**Features:**
- ✅ **100% Authentic** - Uses official SysML kernel API
- ✅ **Complete SysML syntax** - `comp def`, `comp usage`, `skin sysmlbw`
- ✅ **PSysML protocol** - Full UUID linking support
- ✅ **Full CLI support** - All kernel view types, styles, and element selection

**Requirements:**
- SysML conda kernel (`conda install -c conda-forge sysml`)
- jupyter-client (`pip install jupyter-client`)

### 2. Kernel API
**Best for:** Development, interactive exploration

```python
from sysml_visualizer import SysMLKernelVisualizer

visualizer = SysMLKernelVisualizer()
result = visualizer.visualize_file("model.sysml")
```

**Features:**
- ✅ **Real kernel execution** - Direct Jupyter kernel access
- ✅ **Authentic %viz commands** - Native SysML visualization with all options
- ✅ **Package detection** - Automatic model analysis
- ✅ **Live kernel session** - Interactive development
- ✅ **Full view support** - Tree, Interconnection, Action, State, Sequence, Case, MIXED
- ✅ **Style options** - stdcolor and custom kernel-supported styles

**Requirements:**
- SysML conda kernel (`conda install -c conda-forge sysml`)
- jupyter-client (`pip install jupyter-client`)

### 3. Enhanced Standalone
**Best for:** Minimal dependencies, air-gapped environments

```python
from sysml_visualizer import StandaloneSysMLVisualizer

visualizer = StandaloneSysMLVisualizer()
result = visualizer.visualize_file("model.sysml", "output.svg")
```

**Features:**
- ✅ **Zero Python dependencies** - Pure Python implementation
- ✅ **Complete SysML parsing** - Parts, attributes, actions, relationships
- ✅ **Standard PlantUML** - Works with any PlantUML installation
- ✅ **Fast execution** - No kernel overhead
- ⚠️ **Limited view options** - Basic tree structure only (no kernel views)
- ⚠️ **No style support** - Uses default PlantUML styling
- ⚠️ **Does Not Fully Support SysML V2** - simple parser with minimal testing

**Requirements:**
- GraphViz (`apt install graphviz` / `brew install graphviz`)
- PlantUML (`apt install plantuml` / `brew install plantuml`)

## 📦 Installation

### Prerequisites

1. **Python 3.8+**
2. **Choose your method dependencies:**

#### For Kernel Methods (1 & 2):
```bash
# Install conda if needed
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Install SysML v2 kernel
conda install -c conda-forge sysml

# Verify installation
jupyter kernelspec list  # Should show 'sysml' kernel
```

#### For Standalone Method (3):
```bash
# Ubuntu/Debian
sudo apt install graphviz plantuml

# macOS
brew install graphviz plantuml
```

### Package Installation

```bash
# Install base package
pip install sysml-v2-visualizer

# Install with optional dependencies
pip install sysml-v2-visualizer[kernel]     # For kernel methods
pip install sysml-v2-visualizer[standalone] # For standalone method
pip install sysml-v2-visualizer[dev]        # For development
```

## 🚀 Usage Examples

### Command Line Interface

```bash
# Check what methods are available
sysml-visualize --check-deps

# Basic usage (uses kernel-integration by default)
sysml-visualize examples/working_vehicle.sysml output.svg

# Specify method explicitly
sysml-visualize model.sysml output.svg --method kernel-api
sysml-visualize model.sysml output.svg --method standalone

# Advanced visualization options (kernel methods only)
sysml-visualize model.sysml output.svg --method kernel-api --view Interconnection
sysml-visualize model.sysml output.svg --method kernel-integration --view Action --style stdcolor
sysml-visualize model.sysml output.svg --method kernel-api --view Tree --element "PackageName::ElementName"

# Verbose output for debugging
sysml-visualize model.sysml output.svg --verbose

# Show help
sysml-visualize --help
```

### Advanced Visualization Options

The kernel-based methods (kernel-integration and kernel-api) support the full range of official SysML v2 visualization options:

#### Available Views
```bash
# Tree view (default) - Hierarchical structure
sysml-visualize model.sysml output.svg --view Tree

# Interconnection view - Shows relationships and connections
sysml-visualize model.sysml output.svg --view Interconnection

# Action view - Focuses on action elements and flows
sysml-visualize model.sysml output.svg --view Action

# State view - State-based diagrams
sysml-visualize model.sysml output.svg --view State

# Sequence view - Sequence diagrams
sysml-visualize model.sysml output.svg --view Sequence

# Case view - Use case scenarios
sysml-visualize model.sysml output.svg --view Case

# Mixed view - Combination of multiple views
sysml-visualize model.sysml output.svg --view MIXED
```

#### Styling Options
```bash
# Standard color scheme
sysml-visualize model.sysml output.svg --view Tree --style stdcolor

# Custom styles (as supported by kernel)
sysml-visualize model.sysml output.svg --view Interconnection --style custom
```

#### Element-Specific Visualization
```bash
# Visualize entire package
sysml-visualize model.sysml output.svg --element "VehicleExample"

# Visualize specific part definition
sysml-visualize model.sysml output.svg --element "VehicleExample::Vehicle"

# Combine with views and styles
sysml-visualize model.sysml output.svg --view Action --style stdcolor --element "VehicleExample::Vehicle"
```

### Python API Examples

```python
# Example 1: Kernel Integration (Recommended)
from sysml_visualizer import KernelIntegratedSysMLVisualizer

visualizer = KernelIntegratedSysMLVisualizer()

# Basic usage
result = visualizer.visualize_file("model.sysml", "output.svg")
print(f"Generated {Path(result).stat().st_size} byte SVG")

# With view and style options
result = visualizer.visualize_file("model.sysml", "output.svg",
                                  view="Interconnection", style="stdcolor")

# Visualize specific element
result = visualizer.visualize_file("model.sysml", "output.svg",
                                  view="Tree", element="VehicleExample::Vehicle")

# Example 2: Standalone (No dependencies)
from sysml_visualizer import StandaloneSysMLVisualizer

visualizer = StandaloneSysMLVisualizer()
result = visualizer.visualize_file("model.sysml", "output.svg")

# Example 3: Kernel API (Interactive)
from sysml_visualizer import SysMLKernelVisualizer

visualizer = SysMLKernelVisualizer()

# Direct SysML code with visualization options
result = visualizer.visualize("package Demo { part def Vehicle; }",
                             view="Action", style="stdcolor")

# File-based visualization with options
result = visualizer.visualize_file("model.sysml",
                                  view="Interconnection",
                                  element="Demo::Vehicle")
```

## 📖 Command Reference

### Available View Types

All kernel-based methods (kernel-integration and kernel-api) support the full range of official SysML v2 visualization views:

- **Default**: Default kernel view
- **Tree** (default): Hierarchical structure view showing element relationships
- **Interconnection**: Relationship and connection diagrams
- **Action**: Behavioral elements and action flows
- **State**: State machine diagrams and state transitions
- **Sequence**: Sequence diagrams showing interactions over time
- **Case**: Use case scenarios and case-based views
- **MIXED**: Combined view types for comprehensive visualization

### Available Styles

Kernel methods support various styling options to enhance visual presentation:

- **stdcolor**: Standard color scheme for improved readability
- **sysmlbw**: Black and white SysML styling (built-in)
- **monochrome**: Monochrome styling option
- **Custom styles**: Any style supported by the underlying PlantUML/SysML kernel

*Note: The standalone method uses default PlantUML styling and does not support custom styles.*

### CLI Options Reference

#### Core Options
- `--method <METHOD>`: Choose visualization method
  - `kernel-integration` (default): Production-ready kernel integration
  - `kernel-api`: Direct kernel API access for development
  - `standalone`: Minimal dependencies, air-gapped environments

#### Visualization Options (Kernel Methods Only)
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
├── sysml_visualizer/
│   ├── __init__.py              # Package exports
│   ├── kernel_integration.py   # Method 1: Kernel Integration
│   ├── kernel_api.py           # Method 2: Kernel API
│   ├── standalone.py           # Method 3: Enhanced Standalone
│   ├── cli.py                  # Command line interface
│   ├── utils.py                # Utility functions
│   ├── examples/               # Example SysML files
│   │   ├── working_vehicle.sysml
│   └── sysmlbw.skin           # Authentic SysML skin file
├── setup.py                    # Package configuration
└── README.md                   # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/sysml-v2-visualizer.git
cd sysml-v2-visualizer

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black sysml_visualizer/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Ensure all tests pass: `pytest`
4. Format code: `black sysml_visualizer/`
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

   # Get installation suggestions
   sysml-visualize model.sysml output.svg --method kernel-integration
   ```

3. **No SVG Output**
   - Ensure your SysML code defines packages/elements
   - Check that SysML syntax is valid
   - Try the working example first: `sysml-visualizer/examples/working_vehicle.sysml`

### Getting Help

- 📖 [Documentation](https://github.com/your-org/sysml-v2-visualizer/blob/main/README.md)
- 🐛 [Bug Reports](https://github.com/your-org/sysml-v2-visualizer/issues)
- 💬 [Discussions](https://github.com/your-org/sysml-v2-visualizer/discussions)

## 📊 Method Comparison

| Feature | Kernel Integration | Kernel API | Standalone |
|---------|-------------------|------------|------------|
| **Authenticity** | 100% | 100% | ~95% |
| **Dependencies** | Kernel + Python | Kernel + Python | GraphViz + PlantUML |
| **Speed** | Fast | Medium | Fast |
| **CI/CD Ready** | ✅ | ✅ | ✅ |
| **Air-gapped** | ❌ | ❌ | ✅ |
| **Interactive** | ❌ | ✅ | ❌ |
| **View Options** | All kernel views | All kernel views | Limited |
| **Style Support** | Full kernel styles | Full kernel styles | Basic |
| **Element Selection** | ✅ | ✅ | ❌ |


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


**Generate professional SysML v2 diagrams with confidence!** 🚀