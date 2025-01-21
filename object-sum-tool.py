bl_info = {
    "name": "Object Sum Tool",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Elias Alves Chacon",
    "description": "Calculate sum of dimensions or area for objects with the same name prefix."
}

import bpy
import csv
from bpy.props import StringProperty, EnumProperty, BoolProperty
from pathlib import Path

# Global variable for history tracking
calculation_history = []

def calculate_sum(prefix, operation):
    selected_objects = [obj for obj in bpy.data.objects if obj.name.startswith(prefix) and obj.visible_get()]
    result = 0.0

    for obj in selected_objects:
        dim_x, dim_y, dim_z = obj.dimensions

        if operation == 'X':
            result += dim_x
        elif operation == 'Y':
            result += dim_y
        elif operation == 'Z':
            result += dim_z
        elif operation == 'AREA_XY':
            result += dim_x * dim_y
        elif operation == 'AREA_XZ':
            result += dim_x * dim_z
        elif operation == 'AREA_YZ':
            result += dim_y * dim_z
        elif operation == 'AREA_XYZ':
            result += dim_x * dim_y * dim_z
        elif operation == 'BIGGEST':
            result += max(dim_x, dim_y, dim_z)

    return result, len(selected_objects), selected_objects

def format_number(number):
    """Formats the number based on the user's choice (comma or dot)."""
    if bpy.context.scene.use_comma_for_decimal:
        return f"{number:.2f}".replace('.', ',')
    else:
        return f"{number:.2f}"

class OBJECT_PT_PrefixSumTool(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Object Sum Tool"
    bl_idname = "OBJECT_PT_prefix_sum_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "prefix_input", text="Object Name Prefix")
        layout.prop(scene, "calculation_type", text="Calculation Type")
        layout.prop(scene, "use_comma_for_decimal", text="Use Comma for Decimal")
        layout.operator("object.calculate_prefix_sum", text="Calculate")
        layout.operator("object.clear_prefix_sum_history", text="Clear History")
        layout.operator("object.export_prefix_sum_csv", text="Export to CSV")

        layout.label(text="History:")
        col = layout.column()
        col.ui_units_x = max(10, max(len(entry) for entry in calculation_history[-5:]) // 5 + 1)  # Adjust width dynamically
        for entry in calculation_history[-5:]:  # Show last 5 entries
            col.label(text=entry)

class OBJECT_OT_CalculatePrefixSum(bpy.types.Operator):
    """Calculate the sum of dimensions or area for objects with the same prefix"""
    bl_idname = "object.calculate_prefix_sum"
    bl_label = "Calculate Prefix Sum"

    def execute(self, context):
        prefix = context.scene.prefix_input
        operation = context.scene.calculation_type
        result, count, _ = calculate_sum(prefix, operation)

        result_text = f"Prefix: '{prefix}', Objects: {count}, Operation: '{operation}', Result: {format_number(result)}"
        calculation_history.append(result_text)
        self.report({'INFO'}, result_text)
        return {'FINISHED'}

class OBJECT_OT_ClearPrefixSumHistory(bpy.types.Operator):
    """Clear the calculation history"""
    bl_idname = "object.clear_prefix_sum_history"
    bl_label = "Clear Prefix Sum History"

    def execute(self, context):
        global calculation_history
        calculation_history.clear()
        self.report({'INFO'}, "Calculation history cleared.")
        return {'FINISHED'}

class OBJECT_OT_ExportPrefixSumCSV(bpy.types.Operator):
    """Export gathered data to a CSV file"""
    bl_idname = "object.export_prefix_sum_csv"
    bl_label = "Export Prefix Sum CSV"

    def execute(self, context):
        prefix = context.scene.prefix_input
        operation = context.scene.calculation_type
        result, count, objects = calculate_sum(prefix, operation)

        filepath = bpy.path.abspath(f"//prefix_sum_export.csv")
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([f"Prefix: {prefix}", f"Operation: {operation}", f"Sum: {format_number(result)}"])
            writer.writerow(["Object Name", "X", "Y", "Z"])
            for obj in objects:
                writer.writerow([obj.name, format_number(obj.dimensions.x), format_number(obj.dimensions.y), format_number(obj.dimensions.z)])

        self.report({'INFO'}, f"Exported to {filepath}")
        return {'FINISHED'}

class OBJECT_OT_OpenPrefixSumWindow(bpy.types.Operator):
    """Open prefix sum tool with active object name"""
    bl_idname = "object.open_prefix_sum_window"
    bl_label = "Open Prefix Sum Tool"

    def execute(self, context):
        if context.active_object:
            context.scene.prefix_input = context.active_object.name
        bpy.ops.wm.call_panel(name="OBJECT_PT_prefix_sum_tool")
        return {'FINISHED'}

# Add custom properties
bpy.types.Scene.prefix_input = StringProperty(
    name="Prefix Input",
    description="Prefix of the objects to sum dimensions",
    default=""
)

bpy.types.Scene.calculation_type = EnumProperty(
    name="Calculation Type",
    description="Choose the type of calculation",
    items=[
        ('X', "X", "Sum of X dimensions"),
        ('Y', "Y", "Sum of Y dimensions"),
        ('Z', "Z", "Sum of Z dimensions"),
        ('AREA_XY', "Area XY", "Sum of XY areas"),
        ('AREA_XZ', "Area XZ", "Sum of XZ areas"),
        ('AREA_YZ', "Area YZ", "Sum of YZ areas"),
        ('AREA_XYZ', "Area XYZ", "Sum of XYZ volumes"),
        ('BIGGEST', "Bigger Size", "Sum of the biggest dimension for each object")
    ],
    default='X'
)

bpy.types.Scene.use_comma_for_decimal = BoolProperty(
    name="Use Comma for Decimal",
    description="Use comma instead of dot for decimal separator",
    default=False
)

# Register context menu
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_OpenPrefixSumWindow.bl_idname, text="Prefix Sum Tool")

# Register and unregister classes
def register():
    bpy.utils.register_class(OBJECT_PT_PrefixSumTool)
    bpy.utils.register_class(OBJECT_OT_CalculatePrefixSum)
    bpy.utils.register_class(OBJECT_OT_ClearPrefixSumHistory)
    bpy.utils.register_class(OBJECT_OT_ExportPrefixSumCSV)
    bpy.utils.register_class(OBJECT_OT_OpenPrefixSumWindow)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_PrefixSumTool)
    bpy.utils.unregister_class(OBJECT_OT_CalculatePrefixSum)
    bpy.utils.unregister_class(OBJECT_OT_ClearPrefixSumHistory)
    bpy.utils.unregister_class(OBJECT_OT_ExportPrefixSumCSV)
    bpy.utils.unregister_class(OBJECT_OT_OpenPrefixSumWindow)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
