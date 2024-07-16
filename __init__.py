
bl_info = {
    "name": "Creating premises for VSLAM algorithms",
    "description": "A custom Blender addon for creating premises for VSLAM algorithms",
    "author": "Karpenko Gleb Aleksandrovich",
    "version": (1, 0),
    "blender": (2, 80, 0),  # Убедитесь, что версия Blender соответствует вашей.
    "location": "View3D > UI > Creating premises for VSLAM algorithms",
    "category": "Object",
}

import bpy

# Определение свойств
def register_props():
    bpy.types.Scene.field_size = bpy.props.IntProperty(name="Field Size", default=10)
    bpy.types.Scene.field_height = bpy.props.IntProperty(name="Height", default=1080)
    bpy.types.Scene.field_width = bpy.props.IntProperty(name="Width", default=1920)
    bpy.types.Scene.field_focal_length = bpy.props.FloatProperty(name="Focal Length", default=35.0)
    bpy.types.Scene.field_speed = bpy.props.FloatProperty(name="Speed", default=1.0)
    bpy.types.Scene.my_color = bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=4, default=(1.0, 0.462745, 0.0980392, 1.0), min=0.0, max=1.0)
    bpy.types.Scene.my_enum = bpy.props.EnumProperty(
        name="Enum Menu",
        items=[
            ('OPTION_ONE', "Dangeon tiles", ""),
            ('OPTION_TWO', "User recruitment", ""),
        ],
        default='OPTION_ONE'
    )
    bpy.types.Scene.field_katal = bpy.props.StringProperty(name="Working Directory", subtype='DIR_PATH')
    bpy.types.Scene.field_dist = bpy.props.StringProperty(name="Distortion Matrix")
    bpy.types.Scene.field_katal_tiles = bpy.props.StringProperty(name="Tiles Directory", subtype='DIR_PATH')
    bpy.types.Scene.field_katal_re = bpy.props.StringProperty(name="Reconstruction Directory", subtype='DIR_PATH')

def unregister_props():
    del bpy.types.Scene.field_size
    del bpy.types.Scene.field_height
    del bpy.types.Scene.field_width
    del bpy.types.Scene.field_focal_length
    del bpy.types.Scene.field_speed
    del bpy.types.Scene.my_color
    del bpy.types.Scene.my_enum
    del bpy.types.Scene.field_katal
    del bpy.types.Scene.field_dist
    del bpy.types.Scene.field_katal_tiles
    del bpy.types.Scene.field_katal_re

class CustomAddonPanel(bpy.types.Panel):
    bl_label = "Generation of premises"
    bl_idname = "PT_Generation_of_premises"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generation of premises'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Размеры поля (тайлы):")
        row.prop(context.scene, "field_size", text="")
        
        row = layout.row()
        row.label(text="Разрешение (px):")
        row.prop(context.scene, "field_height", text="")
        row.prop(context.scene, "field_width", text="")
        
        row = layout.row()
        row.label(text="Фокусное расстояние (мм):")
        row.prop(context.scene, "field_focal_length", text="")
        
        row = layout.row()
        row.label(text="Скорость (м/с):")
        row.prop(context.scene, "field_speed", text="")
        
        layout.prop(context.scene, "my_color", text="Color Picker")
        
        row = layout.row()
        row.label(text="Рабочий каталог:")
        row.prop(context.scene, "field_katal", text="")
        
        row = layout.row()
        row.label(text="Матрица дисторсии:")
        row.prop(context.scene, "field_dist", text="")
        
        layout.prop(context.scene, "my_enum", text="Enum Menu")
        
        row = layout.row()
        row.label(text="Путь к набору")
        row.prop(context.scene, "field_katal_tiles", text="")
        
        layout.operator("customaddon.button", text="Запуск генерации")
        
        row = layout.row()
        row.label(text="Каталог для воссоздания:")
        row.prop(context.scene, "field_katal_re", text="")
        
        layout.operator("customaddon1.button", text="Воссоздание генерации")

class CustomAddonButton(bpy.types.Operator):
    bl_idname = "customaddon.button"
    bl_label = "Запуск"

    def execute(self, context):
        field_data = [context.scene.field_1, context.scene.field_2, context.scene.field_3, context.scene.field_4, context.scene.field_5]
        for i, data in enumerate(field_data):
            print(f"Field {i + 1}: {data}")
        
        return {'FINISHED'}

class CustomAddonButton1(bpy.types.Operator):
    bl_idname = "customaddon1.button"
    bl_label = "Запуск"

    def execute(self, context):
        field_data = [context.scene.field_1, context.scene.field_2, context.scene.field_3, context.scene.field_4, context.scene.field_5]
        for i, data in enumerate(field_data):
            print(f"Field {i + 1}: {data}")
        
        return {'FINISHED'}

# Регистрация классов и свойств
def register():
    bpy.utils.register_class(CustomAddonPanel)
    bpy.utils.register_class(CustomAddonButton)
    bpy.utils.register_class(CustomAddonButton1)
    register_props()

def unregister():
    bpy.utils.unregister_class(CustomAddonPanel)
    bpy.utils.unregister_class(CustomAddonButton)
    bpy.utils.unregister_class(CustomAddonButton1)
    unregister_props()

if __name__ == "__main__":
    register()
