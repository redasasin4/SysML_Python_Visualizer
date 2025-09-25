#!/usr/bin/env python3
"""
SysML Kernel API - Direct Access to Official SysML v2 Visualization

This module provides programmatic access to the official SysML v2 Jupyter kernel,
enabling the generation of authentic SysML visualizations outside of Jupyter notebooks.

Key Features:
- Direct kernel communication using jupyter_client
- Automatic package detection from SysML code
- SVG output extraction and file saving
- Support for all %viz magic command options
- CI/CD ready implementation

Requirements:
- SysML v2 Jupyter kernel (conda install -c conda-forge sysml)
- jupyter-client Python package

Example Usage:
    api = SysMLKernelAPI()
    if api.start_kernel():
        outputs = api.visualize(sysml_code)
        api.stop_kernel()

Author: Generated for SysML v2 visualization CI/CD pipeline
License: MIT
"""

from jupyter_client import KernelManager
import sys
from pathlib import Path

class SysMLKernelAPI:
    """
    Python API for interfacing with the official SysML v2 Jupyter kernel.

    This class manages the lifecycle of a SysML v2 kernel and provides methods
    to execute SysML code and generate visualizations using the same engine
    that powers the Jupyter notebook %viz magic commands.

    Attributes:
        km: KernelManager instance for managing the SysML kernel
        kc: KernelClient instance for communicating with the kernel

    Example:
        >>> api = SysMLKernelAPI()
        >>> api.start_kernel()
        >>> outputs = api.visualize("package Demo { part def Vehicle; }")
        >>> api.stop_kernel()
    """

    def __init__(self):
        """Initialize the SysML Kernel API."""
        self.km = None
        self.kc = None

    def start_kernel(self):
        """
        Start the SysML v2 Jupyter kernel.

        Initializes a new SysML kernel instance and establishes communication
        channels. The kernel must be started before executing any SysML code.

        Returns:
            bool: True if kernel started successfully, False otherwise

        Raises:
            Exception: If kernel initialization fails
        """
        print("Starting SysML kernel...")
        self.km = KernelManager(kernel_name='sysml')
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()

        # Wait for kernel to be ready
        try:
            self.kc.wait_for_ready(timeout=30)
            print("✅ SysML kernel is ready")
            return True
        except Exception as e:
            print(f"❌ Failed to start kernel: {e}")
            return False

    def execute_code(self, code):
        """Execute SysML code in the kernel"""
        if not self.kc:
            raise RuntimeError("Kernel not started")

        print(f"Executing SysML code:\n{code}")

        # Execute the code
        msg_id = self.kc.execute(code)

        # Collect outputs
        outputs = []
        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=10)
                if msg['parent_header']['msg_id'] == msg_id:
                    if msg['msg_type'] == 'execute_result':
                        outputs.append({
                            'type': 'execute_result',
                            'data': msg['content']['data']
                        })
                    elif msg['msg_type'] == 'display_data':
                        outputs.append({
                            'type': 'display_data',
                            'data': msg['content']['data']
                        })
                    elif msg['msg_type'] == 'stream':
                        outputs.append({
                            'type': 'stream',
                            'name': msg['content']['name'],
                            'text': msg['content']['text']
                        })
                    elif msg['msg_type'] == 'error':
                        outputs.append({
                            'type': 'error',
                            'ename': msg['content']['ename'],
                            'evalue': msg['content']['evalue'],
                            'traceback': msg['content']['traceback']
                        })
                    elif msg['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                        break
            except Exception as e:
                print(f"Timeout or error getting message: {e}")
                break

        return outputs

    def visualize(self, sysml_code=None, view=None, style=None, element=None):
        """
        Execute SysML code and generate visualization using %viz magic commands.

        This method combines SysML model execution with visualization generation
        using the official SysML kernel's %viz command with full feature support.

        Args:
            sysml_code (str, optional): SysML code to execute before visualization.
                                       If None, only %viz commands are executed.
            view (str, optional): Visualization view type. Options include:
                                 - 'Tree' (default): Hierarchical tree view
                                 - 'Interconnection': Connection/relationship view
                                 - 'Graph': Graph-based layout
                                 - 'Dependencies': Dependency relationships
            style (str, optional): Visualization style. Options include:
                                  - 'stdcolor': Standard color scheme
                                  - Custom styles supported by kernel
            element (str, optional): Specific element to visualize (e.g., 'Package::Element')

        Returns:
            list: List of kernel output messages, including display_data with SVG
                 content if visualization succeeds.

        Example:
            >>> outputs = api.visualize(sysml_code, view='Interconnection', style='stdcolor')
            >>> outputs = api.visualize(sysml_code, view='Tree', element='VehicleExample::Vehicle')
        """
        outputs = []

        # First execute the SysML code if provided
        if sysml_code:
            print("Executing SysML model...")
            model_outputs = self.execute_code(sysml_code)
            outputs.extend(model_outputs)

        # Then execute %viz magic command
        print("Generating visualization with %viz...")

        # Extract package name from previous outputs if needed
        package_name = None
        for output in outputs:
            if output['type'] == 'execute_result' and 'data' in output:
                text = output['data'].get('text/plain', '')
                if text.startswith('Package '):
                    # Extract package name like "Package Demo (id)"
                    import re
                    match = re.match(r'Package (\w+)', text)
                    if match:
                        package_name = match.group(1)
                        print(f"Detected package name: {package_name}")
                        break

        if not package_name:
            package_name = "Demo"  # fallback

        # Build %viz command with user-specified options
        viz_cmd = "%viz"

        # Add view option (default to Tree if not specified)
        view_type = view if view else "Tree"
        viz_cmd += f" --view {view_type}"

        # Add style option if specified
        if style:
            viz_cmd += f" --style {style}"

        # Add target element (use user-specified element or detected package)
        target = element if element else package_name
        viz_cmd += f" {target}"

        print(f"Executing: {viz_cmd}")
        viz_outputs = self.execute_code(viz_cmd)
        outputs.extend(viz_outputs)

        # Check if we got SVG output
        for output in viz_outputs:
            if output['type'] == 'display_data' and 'data' in output:
                if 'image/svg+xml' in output['data']:
                    print(f"✅ Got SVG with command: {viz_cmd}")
                    return outputs
            elif output['type'] == 'execute_result' and 'data' in output:
                if 'image/svg+xml' in output['data']:
                    print(f"✅ Got SVG with command: {viz_cmd}")
                    return outputs

        # If primary command failed, try fallback with Tree view
        if view_type != "Tree":
            print(f"Primary view '{view_type}' failed, trying Tree view as fallback...")
            fallback_cmd = f"%viz --view Tree {target}"
            print(f"Executing fallback: {fallback_cmd}")
            fallback_outputs = self.execute_code(fallback_cmd)
            outputs.extend(fallback_outputs)

            for output in fallback_outputs:
                if output['type'] == 'display_data' and 'data' in output:
                    if 'image/svg+xml' in output['data']:
                        print(f"✅ Got SVG with fallback command: {fallback_cmd}")
                        return outputs
                elif output['type'] == 'execute_result' and 'data' in output:
                    if 'image/svg+xml' in output['data']:
                        print(f"✅ Got SVG with fallback command: {fallback_cmd}")
                        return outputs

        return outputs

    def visualize_file(self, output_file=None, view=None, style=None, element=None):
        """
        Visualize all .sysml files and optionally save to output file.
        Auto-discovers all .sysml files in current directory and subdirectories.

        Args:
            output_file (str, optional): Path to save SVG output
            view (str, optional): Visualization view type
            style (str, optional): Visualization style
            element (str, optional): Specific element to visualize

        Returns:
            str: Path to output file or 'kernel_output.svg' if no output specified
        """
        from pathlib import Path
        from .utils import find_sysml_files, combine_sysml_files

        # Auto-discover all .sysml files
        sysml_files = find_sysml_files()
        if not sysml_files:
            raise FileNotFoundError("No .sysml files found in current directory or subdirectories")

        sysml_code = combine_sysml_files(sysml_files)
        return self.visualize_content(sysml_code, output_file, view=view, style=style, element=element)

    def visualize_content(self, sysml_content, output_file=None, view=None, style=None, element=None):
        """
        Visualize SysML content and optionally save to output file.

        Args:
            sysml_content (str): SysML content to visualize
            output_file (str, optional): Path to save SVG output
            view (str, optional): Visualization view type
            style (str, optional): Visualization style
            element (str, optional): Specific element to visualize

        Returns:
            str: Path to output file or 'kernel_output.svg' if no output specified
        """
        from pathlib import Path

        # Generate visualization
        self.start_kernel()
        try:
            outputs = self.visualize(sysml_content, view=view, style=style, element=element)

            # Extract SVG from outputs
            svg_content = None
            for output in outputs:
                if output['type'] == 'display_data' and 'data' in output:
                    if 'image/svg+xml' in output['data']:
                        svg_content = output['data']['image/svg+xml']
                        break
                elif output['type'] == 'execute_result' and 'data' in output:
                    if 'image/svg+xml' in output['data']:
                        svg_content = output['data']['image/svg+xml']
                        break

            if not svg_content:
                raise RuntimeError("No SVG content generated from kernel")

            # Save to output file
            output_path = output_file or "kernel_output.svg"
            Path(output_path).write_text(svg_content)

            return output_path

        finally:
            self.stop_kernel()

    def stop_kernel(self):
        """Stop the kernel"""
        if self.kc:
            self.kc.stop_channels()
        if self.km:
            self.km.shutdown_kernel()
        print("✅ Kernel stopped")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='SysML v2 Kernel API - Direct access to official SysML visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Auto-discovery mode (finds all .sysml files)
  python kernel_api.py viz_file output.svg

  # Specify view type
  python kernel_api.py viz_file output.svg --view Interconnection
  python kernel_api.py viz_file output.svg --view Tree
  python kernel_api.py viz_file output.svg --view State
  python kernel_api.py viz_file output.svg --view Action

  # Add styling
  python kernel_api.py viz_file output.svg --view Tree --style stdcolor

  # Visualize specific element
  python kernel_api.py viz_file output.svg --element PackageName::ElementName

  # Execute SysML code directly
  python kernel_api.py execute "package Demo { part def Vehicle; }" output.svg --view Interconnection

Available Views (from SysML kernel):
  Default        Default kernel view
  Tree           Hierarchical tree view (default)
  State          State-based view
  Interconnection Connection/relationship view
  Action         Action-based view
  Sequence       Sequence diagrams
  Case           Case-based view
  MIXED          Mixed view types

Available Styles:
  stdcolor       Standard color scheme
  (other styles supported by kernel)
        '''
    )

    parser.add_argument('command', choices=['execute', 'visualize', 'viz_file'],
                       help='Command to execute')

    parser.add_argument('input', nargs='?', help='SysML code (for execute/visualize commands)')

    parser.add_argument('output', nargs='?', default='kernel_output.svg',
                       help='Output SVG file (default: kernel_output.svg)')

    parser.add_argument('--view', choices=['Default', 'Tree', 'State', 'Interconnection', 'Action', 'Sequence', 'Case', 'MIXED'],
                       default='Tree', help='Visualization view type (default: Tree)')

    parser.add_argument('--style', help='Visualization style (e.g., stdcolor)')

    parser.add_argument('--element', help='Specific element to visualize (e.g., Package::Element)')

    args = parser.parse_args()

    command = args.command
    output_file = args.output

    api = SysMLKernelAPI()

    try:
        if not api.start_kernel():
            sys.exit(1)

        if command == "execute":
            if not args.input:
                print("Error: Input SysML code is required for execute command")
                sys.exit(1)
            code = args.input
            outputs = api.execute_code(code)

        elif command == "visualize":
            if not args.input:
                print("Error: Input SysML code is required for visualize command")
                sys.exit(1)
            code = args.input
            outputs = api.visualize(code, view=args.view, style=args.style, element=args.element)

        elif command == "viz_file":
            # Auto-discover all .sysml files instead of requiring specific input file
            outputs = api.visualize_file(view=args.view, style=args.style, element=args.element)

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

        # Process outputs
        print("\n" + "="*50)
        print("KERNEL OUTPUTS:")
        print("="*50)

        svg_content = None
        for i, output in enumerate(outputs):
            print(f"\n--- Output {i+1} ---")
            print(f"Type: {output['type']}")

            if output['type'] == 'display_data' and 'data' in output:
                data = output['data']
                print(f"Display data keys: {list(data.keys())}")

                if 'image/svg+xml' in data:
                    svg_content = data['image/svg+xml']
                    print("📊 SVG visualization found!")
                    print(f"SVG length: {len(svg_content)} characters")

                    # Save SVG to file
                    with open(output_file, 'w') as f:
                        f.write(svg_content)
                    print(f"💾 Saved visualization to: {output_file}")

                if 'text/plain' in data:
                    print(f"Text: {data['text/plain']}")

                if 'text/html' in data:
                    print("HTML content found")
                    print(f"HTML length: {len(data['text/html'])} characters")

            elif output['type'] == 'execute_result' and 'data' in output:
                data = output['data']
                print(f"Execute result keys: {list(data.keys())}")

                if 'image/svg+xml' in data:
                    svg_content = data['image/svg+xml']
                    print("📊 SVG visualization found in execute_result!")
                    print(f"SVG length: {len(svg_content)} characters")

                    # Save SVG to file
                    with open(output_file, 'w') as f:
                        f.write(svg_content)
                    print(f"💾 Saved visualization to: {output_file}")

                if 'text/plain' in data:
                    plain_text = data['text/plain']
                    print(f"Plain text: {plain_text}")

                    # Check if it contains SVG content as text
                    if '<svg' in plain_text.lower():
                        print("📊 SVG content found in text/plain!")
                        svg_content = plain_text
                        with open(output_file, 'w') as f:
                            f.write(svg_content)
                        print(f"💾 Saved SVG from text to: {output_file}")

            elif output['type'] == 'stream':
                print(f"{output['name']}: {output['text']}")

            elif output['type'] == 'error':
                print(f"❌ Error: {output['ename']}: {output['evalue']}")
                if 'traceback' in output:
                    print("Traceback:")
                    for line in output['traceback']:
                        print(f"  {line}")

        if svg_content:
            print("\n✅ Visualization generated successfully!")
        else:
            print("\n⚠️  No SVG visualization found in outputs")

    except KeyboardInterrupt:
        print("\\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        api.stop_kernel()

if __name__ == "__main__":
    main()