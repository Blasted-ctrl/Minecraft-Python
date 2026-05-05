import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController # Your Player

app = Ursina()

textures = {
    1: load_texture("Assets/Textures/Grass.png"),
    2: load_texture("Assets/Textures/Brick.png"),
    3: load_texture("Assets/Textures/Dirt.png"),
    4: load_texture("Assets/Textures/Stone.png"),
    5: load_texture("Assets/Textures/Wood.png"),

}

sky_bg = load_texture("Assets/Textures/Sky.png")
build_sound = Audio("Assets/SFX/Build_Sound.wav",loop = False,autoplay = False)

block_pick = 1
general_world_size = 20

class Block(Button):
    def __init__(self,position=(0,0,0),texture=textures[1],breakable=True):
        super().__init__(
            parent = scene,
            position = position,
            model ="Assets/Models/Block.obj",
            origin_y = 0.5,
            texture = texture,
            color = color.Color(0,0,random.uniform(0.9,1), 1),
            highlight_color = color.light_gray,
            scale = 0.5
        )
        self.breakable = breakable
    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                build_sound.play()
                new_block = Block(position = self.position + mouse.normal,texture = textures[block_pick])
            elif key == "right mouse down" and self.breakable:
                build_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "sphere",
            texture = sky_bg,
            scale = 150,
            double_sided = True
        )

class Tree(Entity):
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = "Assets/Models/Lowpoly_tree_sample.obj",
            scale = (0.6,0.6,0.6),
            collider = "mesh", # Collision

        )

def generate_trees(num_trees = 3,terrain_Size = 20):
    for i in range(num_trees):
        x = random.randint(0,terrain_Size-1)
        y = 0
        z = random.randint(0,terrain_Size-1)
        Tree(position=(x,y,z))


def generate_terrain():
    height = 5
    for z in range(general_world_size):
        for x in range(general_world_size):
            for y in range(height):
                if y == height -1:
                    Block(position=(x,y,z),texture=textures[1])
                elif y >= height -3:
                    Block(position=(x,y,z),texture=textures[2])
                else:
                    Block(position=(x,y,z),texture = textures[5],breakable=False)
            Block(position=(x,-1,z),texture=textures[5],breakable=False)

generate_trees()
# Update every second.
def update():

    global block_pick
    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i
            break

    if held_keys["escape"]:
        application.quit()
    if player.y <= -5:
        player.position = (10,10,10)



# Ursina automatically looks for update function, no need to call it. (Updates every seconds)
player = FirstPersonController(position=(10,10,10))
player.cursor.visible = False
sky = Sky()
generate_terrain()

app.run()