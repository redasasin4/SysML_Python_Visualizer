# SysML v2 Visualization Examples

This directory contains comprehensive examples of SysML v2 visualizations generated using different methods and CLI options. All examples are based on the `working_vehicle.sysml` model.

## Source SysML Model

**File:** `working_vehicle.sysml`

```sysml
package VehicleExample {
    part def Vehicle {
        part engine : Engine;
        part wheels : Wheel[4];
        part body : Body;
        perform Vehicle_Action;
    }
    action Vehicle_Action{
        action Engine_Action;
    }
    part def Engine {
        perform Vehicle_Action.Engine_Action;
    }

    part def Wheel {
    }

    part def Body {
    }

    part myVehicle : Vehicle;
}
```

## Generated Examples

### 1. Standalone Visualization

**Command:**
```bash
python src/standalone.py examples/working_vehicle.sysml examples/working_vehicle_standalone.svg
```

**Generated File:** `working_vehicle_standalone.svg` (8,685 bytes)

**Description:** Basic standalone visualization using pure Python implementation without kernel dependencies.

---

### 2. Kernel API Examples

#### Tree View with Standard Color

**Command:**
```bash
python src/kernel_api.py viz_file examples/working_vehicle.sysml examples/working_vehicle_tree_stdcolor.svg --view Tree --style stdcolor
```

**Generated File:** `working_vehicle_tree_stdcolor.svg` (20,963 bytes)

**Description:** Full package tree view with standard color styling, showing hierarchical structure of all elements.

#### Tree View of Specific Element

**Command:**
```bash
python src/kernel_api.py viz_file examples/working_vehicle.sysml examples/working_vehicle_Vehicle_tree.svg --view Tree --element "VehicleExample::Vehicle"
```

**Generated File:** `working_vehicle_Vehicle_tree.svg` (8,661 bytes)

**Description:** Focused tree view of only the Vehicle part definition and its internal components.

#### Interconnection View

**Command:**
```bash
python src/kernel_api.py viz_file examples/working_vehicle.sysml examples/working_vehicle_VehicleExample_interconnection.svg --view Interconnection --element "VehicleExample"
```

**Generated File:** `working_vehicle_VehicleExample_interconnection.svg` (15,651 bytes)

**Description:** Interconnection diagram showing relationships and connections between package elements.

#### Action View

**Command:**
```bash
python src/kernel_api.py viz_file examples/working_vehicle.sysml examples/working_vehicle_action.svg --view Action
```

**Generated File:** `working_vehicle_action.svg` (5,890 bytes)

**Description:** Action-focused view highlighting behavioral elements and action flows in the model.

---

## Usage Notes

1. All commands assume execution from the project root directory
2. Kernel API method requires the SysML conda environment to be active
3. File sizes may vary slightly between generations due to unique IDs