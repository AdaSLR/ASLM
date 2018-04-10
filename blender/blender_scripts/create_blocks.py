import bpy
import numpy as np 


class MakeData(object):
    def __init__(self):
        # Define start and end of simulation
        self.frame_start = 0
        self.frame_end = 400

        # Borders of box
        self.center = [0, 0, 0]
        self.x_border = self.center[0] + 7
        self.y_border = self.center[1] + 7
        self.z_border = self.center[2] + 30

        self.setup_enviroment()
        self.create_blocks()
        self.stop_animation()
        self.highlight_best_element()   
        

    def setup_enviroment(self):
        # Animations settings
        bpy.data.scenes['Scene'].frame_start = self.frame_start
        bpy.data.scenes['Scene'].frame_end = self.frame_end

        # Add camera and global light
        bpy.ops.object.camera_add(location=[0, 0, 35])
        bpy.ops.object.lamp_add(type='SUN')

        # Camera settings
        bpy.data.cameras['Camera'].sensor_width = 42

        # # View from camera
        # bpy.ops.view3d.viewnumpad(type='CAMERA')

    def create_blocks(self):
        # Limits of sempling
        xmax, ymax, zmax = self.x_border, self.y_border, self.z_border + 5
        xmin, ymin, zmin =  - self.x_border, - self.y_border, self.z_border

        for _ in range(50):
            x, y, z = np.random.rand(1), np.random.rand(1), np.abs(np.random.rand(1))
            x = x * np.random.choice([xmax, xmin], size=1, replace=True)
            y = y * np.random.choice([ymax, ymin], size=1, replace=True)
            z = z * np.random.choice([zmax, zmin], size=1, replace=True)

            bpy.ops.mesh.primitive_cylinder_add(location=[x, y, z], rotation=(y, z, x),
            vertices=10, radius=1)
            bpy.ops.rigidbody.object_add(type='ACTIVE')

        # Start animation    
        bpy.ops.screen.animation_play()

    def stop_animation(self):

        def stop_at_last_frame(scene):
            if scene.frame_current == scene.frame_end:
                bpy.ops.screen.animation_cancel()

        bpy.app.handlers.frame_change_pre.append(stop_at_last_frame)



    def find_best_element(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        # Find the highest element in the box
        z_locations = []
        names = []
        for obj in bpy.data.objects:
            if obj.name not in ['basket', 'Camera', 'Lamp', 'Sun']:
                z_locations.append(obj.location[2])
                names.append(obj.name)

        best_element = np.argmax(z_locations)
        best_element = names[best_element]
        bpy.ops.object.select_all(action='DESELECT' )
        return bpy.data.objects[best_element]
        

    def highlight_best_element(self):
        # Create material for highlighting
        obj = self.find_best_element()
        bpy.ops.object.select_pattern(pattern=obj.name)
        mat = bpy.data.materials.new(name='Chto_po_mateshe')
        mat.diffuse_color = (1, 0, 0)
        obj.data.materials.append(mat)
            

# bpy.ops.render.render(animation=True, use_viewport=True)
# bpy.ops.render.render(animation=True)

if __name__ == '__main__':
    new_data = MakeData()