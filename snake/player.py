import arcade
import numpy as np


CHARACTER_SCALING = 1

N_HISTORY_MOVES = 60


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---
        main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.texture = self.idle_texture_pair[0]


        self.score = 0

        self.position_history = np.zeros((N_HISTORY_MOVES ,2))