#!/usr/bin/env python3
"""
Standalone SysML Visualizer - No Kernel Required

This module reverse engineers the SysML v2 visualization system to create
standalone visualizations without requiring the Jupyter kernel API.

Based on analysis of the official kernel output, this recreates the exact
PlantUML generation patterns used by the official implementation.
"""

import re
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import uuid

class SysMLElement:
    """Represents a SysML model element."""

    def __init__(self, name: str, element_type: str, stereotype: str = None):
        self.name = name
        self.element_type = element_type  # 'part_def', 'part', 'attribute', etc.
        self.stereotype = stereotype or element_type
        self.uuid = str(uuid.uuid4())
        self.attributes = []
        self.parts = []
        self.parent = None

    def add_attribute(self, name: str, attr_type: str = "String"):
        """Add an attribute to this element."""
        attr = SysMLElement(f"{name}: {attr_type}", "attribute", "attribute")
        attr.parent = self
        self.attributes.append(attr)
        return attr

    def add_part(self, name: str, part_type: str, multiplicity: str = None):
        """Add a part to this element."""
        part_name = f"{name}: {part_type}"
        if multiplicity:
            part_name += f"[{multiplicity}]"
        part = SysMLElement(part_name, "part", "part")
        part.parent = self
        self.parts.append(part)
        return part

class SysMLPackage:
    """Represents a SysML package containing elements."""

    def __init__(self, name: str):
        self.name = name
        self.uuid = str(uuid.uuid4())
        self.elements = []
        self.part_definitions = []
        self.parts = []

    def add_part_def(self, name: str) -> SysMLElement:
        """Add a part definition to this package."""
        element = SysMLElement(name, "part_def", "part def")
        self.part_definitions.append(element)
        self.elements.append(element)
        return element

    def add_part(self, name: str, part_type: str, multiplicity: str = None) -> SysMLElement:
        """Add a part usage to this package."""
        part_name = f"{name}: {part_type}"
        if multiplicity:
            part_name += f"[{multiplicity}]"
        element = SysMLElement(part_name, "part", "part")
        self.parts.append(element)
        self.elements.append(element)
        return element

class SysMLParser:
    """Parse SysML code and build model structure."""

    def __init__(self):
        self.packages = []

    def parse(self, sysml_code: str) -> List[SysMLPackage]:
        """Parse SysML code and return packages."""
        self.packages = []

        # Use balanced brace parsing for packages
        package_matches = self._find_balanced_braces(sysml_code, r'package\s+(\w+)\s*')

        for package_name, package_content in package_matches:
            package = self._parse_package_content(package_name, package_content)
            self.packages.append(package)

        return self.packages

    def _parse_package_content(self, package_name: str, content: str) -> SysMLPackage:
        """Parse the content of a package."""
        package = SysMLPackage(package_name)

        # Parse part definitions with better brace handling
        part_def_matches = self._find_balanced_braces(content, r'part\s+def\s+(\w+)\s*')
        for part_name, part_content in part_def_matches:
            part_def = package.add_part_def(part_name)
            self._parse_part_content(part_def, part_content)

        # Parse part usages
        part_usage_matches = self._find_balanced_braces(content, r'part\s+(\w+)\s*:\s*(\w+)(?:\s*\[([^\]]+)\])?\s*')
        for match_groups, part_content in part_usage_matches:
            if isinstance(match_groups, tuple) and len(match_groups) >= 2:
                part_name = match_groups[0]
                part_type = match_groups[1]
                multiplicity = match_groups[2] if len(match_groups) > 2 else None
                part = package.add_part(part_name, part_type, multiplicity)

        return package

    def _find_balanced_braces(self, content: str, pattern: str) -> List[Tuple]:
        """Find pattern matches with balanced braces."""
        results = []
        regex = re.compile(pattern)

        pos = 0
        while pos < len(content):
            match = regex.search(content, pos)
            if not match:
                break

            # Find opening brace
            brace_start = content.find('{', match.end())
            if brace_start == -1:
                pos = match.end()
                continue

            # Find matching closing brace
            brace_count = 1
            brace_pos = brace_start + 1
            while brace_pos < len(content) and brace_count > 0:
                if content[brace_pos] == '{':
                    brace_count += 1
                elif content[brace_pos] == '}':
                    brace_count -= 1
                brace_pos += 1

            if brace_count == 0:
                # Found complete block
                block_content = content[brace_start + 1:brace_pos - 1]
                if len(match.groups()) == 1:
                    results.append((match.group(1), block_content))
                else:
                    results.append((match.groups(), block_content))

            pos = brace_pos

        return results

    def _parse_part_content(self, element: SysMLElement, content: str):
        """Parse the content of a part definition."""
        # Parse nested parts
        part_pattern = r'part\s+(\w+)\s*:\s*(\w+)(?:\s*\[([^\]]+)\])?\s*;'
        for match in re.finditer(part_pattern, content):
            part_name = match.group(1)
            part_type = match.group(2)
            multiplicity = match.group(3)
            element.add_part(part_name, part_type, multiplicity)

        # Parse attributes
        attr_pattern = r'attribute\s+(\w+)\s*:\s*(\w+)\s*;'
        for match in re.finditer(attr_pattern, content):
            attr_name = match.group(1)
            attr_type = match.group(2)
            element.add_attribute(attr_name, attr_type)

        # Parse actions (treated as operations)
        action_pattern = r'action\s+(\w+)\s*\(\s*\)\s*;'
        for match in re.finditer(action_pattern, content):
            action_name = match.group(1)
            element.add_attribute(f"{action_name}()", "operation")

class StandalonePlantUMLGenerator:
    """Generate PlantUML code from SysML model - reverse engineered from kernel output."""

    def __init__(self):
        self.element_counter = 1
        self.element_map = {}  # Maps elements to their IDs (E1, E2, etc.)

    def generate(self, packages: List[SysMLPackage]) -> str:
        """Generate PlantUML code for SysML packages."""
        if not packages:
            return ""

        plantuml_lines = [
            "@startuml",
            "skinparam monochrome true",
            "skinparam wrapWidth 300",
            "hide circle",
            ""
        ]

        # Generate package structure matching kernel output
        for package in packages:
            plantuml_lines.extend(self._generate_package(package))

        # Generate relationships
        for package in packages:
            plantuml_lines.extend(self._generate_relationships(package))

        plantuml_lines.append("@enduml")

        return "\n".join(plantuml_lines)

    def _generate_simple_package(self, package: SysMLPackage) -> List[str]:
        """Generate simplified PlantUML for a package."""
        lines = [f"package {package.name} {{", ""]

        # Add simple class representations
        for element in package.part_definitions:
            lines.append(f"  class {element.name} {{")
            for part in element.parts:
                # Extract type name from "name: Type[mult]" format
                type_name = self._extract_type_name(part.name)
                lines.append(f"    + {part.name}")
            lines.append("  }")
            lines.append("")

        # Add relationships
        for element in package.part_definitions:
            for part in element.parts:
                type_name = self._extract_type_name(part.name)
                # Find if this type exists as a part definition
                for target in package.part_definitions:
                    if target.name == type_name:
                        lines.append(f"  {element.name} *-- {type_name}")
                        break

        lines.append("}")
        lines.append("")
        return lines

    def _generate_package(self, package: SysMLPackage) -> List[str]:
        """Generate PlantUML for a package."""
        lines = []

        # Package declaration
        package_id = f"E{self.element_counter}"
        self.element_map[package] = package_id
        self.element_counter += 1

        lines.append(f'package "{package.name}" as {package_id}  [[psysml:{package.uuid} ]]  {{')

        # Generate part definitions
        for element in package.part_definitions:
            lines.extend(self._generate_element(element, is_definition=True))

        # Generate part usages
        for element in package.parts:
            lines.extend(self._generate_element(element, is_definition=False))

        lines.append("}")
        lines.append("")

        return lines

    def _generate_element(self, element: SysMLElement, is_definition: bool = True) -> List[str]:
        """Generate PlantUML for a SysML element."""
        lines = []

        element_id = f"E{self.element_counter}"
        self.element_map[element] = element_id
        self.element_counter += 1

        # Determine element type and stereotype (matching kernel spacing)
        if is_definition:
            comp_type = "def"
            stereotype = f"<<(T,blue) part  def>>"  # Note: double space like kernel
        else:
            comp_type = "usage"
            stereotype = f"<<(T,blue) part>>"

        # Component declaration matching kernel output exactly
        lines.append(f'component "{element.name}" as {element_id} {stereotype} [[psysml:{element.uuid} ]] {{')
        lines.append('}')

        return lines

    def _generate_relationships(self, package: SysMLPackage) -> List[str]:
        """Generate relationships between elements."""
        lines = []

        # Generate relationships for part definitions (their internal parts)
        for part_def in package.part_definitions:
            if part_def.parts:
                part_def_id = self.element_map[part_def]
                for part in part_def.parts:
                    # Create virtual component for internal parts
                    part_id = f"E{self.element_counter}"
                    self.element_counter += 1

                    # Generate the internal part component (matching kernel)
                    lines.append(f'component "{part.name}" as {part_id} <<(T,blue) part>> [[psysml:{uuid.uuid4()} ]] {{')
                    lines.append('}')

                    # Composition relationship (matching kernel syntax)
                    lines.append(f"{part_def_id} *- - {part_id} [[psysml:{uuid.uuid4()} ]] ")

                    # Type relationship (part to its definition) - matching kernel syntax
                    type_name = self._extract_type_name(part.name)
                    type_def = self._find_type_definition(package, type_name)
                    if type_def:
                        type_def_id = self.element_map[type_def]
                        lines.append(f"{part_id} - -:|> {type_def_id} [[psysml:{uuid.uuid4()} ]] ")

        return lines

    def _extract_type_name(self, part_name: str) -> str:
        """Extract type name from 'name: Type[multiplicity]' format."""
        if ':' in part_name:
            type_part = part_name.split(':')[1].strip()
            # Remove multiplicity if present
            if '[' in type_part:
                type_part = type_part.split('[')[0].strip()
            return type_part
        return part_name

    def _find_type_definition(self, package: SysMLPackage, type_name: str) -> Optional[SysMLElement]:
        """Find the part definition for a given type name."""
        for element in package.part_definitions:
            if element.name == type_name:
                return element
        return None

class StandaloneSysMLVisualizer:
    """Complete standalone visualization system."""

    def __init__(self, plantuml_jar_path: str = None):
        """
        Initialize the visualizer.

        Args:
            plantuml_jar_path: Path to PlantUML JAR file. If None, tries to find it.
        """
        self.plantuml_jar_path = plantuml_jar_path or self._find_plantuml_jar()
        self.parser = SysMLParser()
        self.generator = StandalonePlantUMLGenerator()

    def visualize_file(self, sysml_file_path: str, output_path: str) -> str:
        """
        Generate visualization from a .sysml file.

        Args:
            sysml_file_path: Path to .sysml file
            output_path: Path for output SVG file

        Returns:
            Path to generated SVG file
        """
        # Read SysML file
        with open(sysml_file_path, 'r') as f:
            sysml_code = f.read()

        return self.visualize_code(sysml_code, output_path)

    def visualize_code(self, sysml_code: str, output_path: str) -> str:
        """
        Generate visualization from SysML code.

        Args:
            sysml_code: SysML source code
            output_path: Path for output SVG file

        Returns:
            Path to generated SVG file
        """
        print(f"🔍 Parsing SysML code...")

        # Parse SysML code
        packages = self.parser.parse(sysml_code)

        if not packages:
            raise ValueError("No valid SysML packages found in code")

        print(f"📦 Found {len(packages)} package(s)")
        for pkg in packages:
            print(f"   - {pkg.name}: {len(pkg.part_definitions)} part defs, {len(pkg.parts)} parts")

        # Generate PlantUML
        print(f"🎨 Generating PlantUML...")
        plantuml_code = self.generator.generate(packages)

        # Render to SVG
        print(f"🖼️  Rendering SVG...")
        svg_path = self._render_plantuml(plantuml_code, output_path)

        print(f"✅ Visualization saved to: {svg_path}")
        return svg_path

    def _render_plantuml(self, plantuml_code: str, output_path: str) -> str:
        """Render PlantUML code to SVG."""
        if not self.plantuml_jar_path:
            raise RuntimeError("PlantUML JAR not found. Please install PlantUML.")

        # Create temporary PlantUML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_puml_path = temp_file.name

        try:
            # Run PlantUML
            output_dir = str(Path(output_path).parent)
            cmd = [
                "java", "-jar", self.plantuml_jar_path,
                "-tsvg", "-o", output_dir,
                temp_puml_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                raise RuntimeError(f"PlantUML rendering failed: {result.stderr}")

            # Move generated SVG to desired location
            temp_svg_path = Path(temp_puml_path).with_suffix('.svg')
            if temp_svg_path.exists():
                shutil.move(str(temp_svg_path), output_path)
            else:
                raise RuntimeError(f"Expected SVG file not found: {temp_svg_path}")

        finally:
            # Clean up
            Path(temp_puml_path).unlink(missing_ok=True)

        return output_path

    def _find_plantuml_jar(self) -> Optional[str]:
        """Find PlantUML JAR file."""
        # Check if plantuml command is available
        if shutil.which("plantuml"):
            return "plantuml"  # Use system command

        # Look for JAR files
        possible_paths = [
            "plantuml.jar",
            Path(__file__).parent / "plantuml.jar",
            Path(__file__).parent.parent / "plantuml.jar",
            "/usr/share/plantuml/plantuml.jar",
            "/usr/local/share/plantuml/plantuml.jar",
            Path.home() / "plantuml.jar"
        ]

        for path in possible_paths:
            if Path(path).exists():
                return str(path)

        return None

    def get_plantuml_code(self, sysml_code: str) -> str:
        """Get the generated PlantUML code without rendering."""
        packages = self.parser.parse(sysml_code)
        return self.generator.generate(packages)

def main():
    """Command line interface."""
    if len(sys.argv) < 3:
        print("Usage: python standalone_sysml_visualizer.py <input.sysml> <output.svg>")
        print("       python standalone_sysml_visualizer.py --plantuml <input.sysml>")
        sys.exit(1)

    if sys.argv[1] == "--plantuml":
        # Just output PlantUML code
        input_file = sys.argv[2]
        visualizer = StandaloneSysMLVisualizer()

        with open(input_file, 'r') as f:
            sysml_code = f.read()

        plantuml_code = visualizer.get_plantuml_code(sysml_code)
        print(plantuml_code)
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Create visualizer
    visualizer = StandaloneSysMLVisualizer()

    try:
        result_path = visualizer.visualize_file(input_file, output_file)
        print(f"🎯 Success! Visualization: {result_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()