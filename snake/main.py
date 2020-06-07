import arcade
import random
import os
from pynput.keyboard import Controller
from snake.player import PlayerCharacter
from snake.agent import key_action


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"
WALL_SCALING_BOX = 1

COIN_SCALE = 0.5
COIN_COUNT = 50

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

random.seed(42)

class TravellingSalesman(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        """ Set up the game and initialize the variables. """
        # # Sprite lists
        self.player_list = None
        self.coin_list = None
        self.wall_list = None

        # Set up the player
        self.player = None

        self.total_time = 0.0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player = PlayerCharacter()

        self.total_time = 0.0

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 0.8

        self.player_list.append(self.player)

        self.physics_engine = None

        #Generate wall in x-direction
        wall = arcade.Sprite("img/snakeBody.png", WALL_SCALING_BOX)
        n_walls_x = SCREEN_WIDTH // wall._width
        for i in range(n_walls_x):
            wall = arcade.Sprite("img/snakeBody.png", WALL_SCALING_BOX)
            wall.center_x = wall._width//2 + wall._width*i
            wall.center_y = wall._height//2
            self.wall_list.append(wall)
            
            wall = arcade.Sprite("img/snakeBody.png", WALL_SCALING_BOX)
            wall.center_x = wall._width//2 + wall._width*i
            wall.center_y = SCREEN_HEIGHT - wall._height//2
            self.wall_list.append(wall)
            
        #Generate wall in y-direction
        n_walls_y= SCREEN_HEIGHT // wall._height
        for i in range(1, n_walls_y-1):
            wall = arcade.Sprite("img/snakeBody.png", WALL_SCALING_BOX)
            wall.center_x = wall._width//2
            wall.center_y = wall._height//2 + wall._height*i 
            self.wall_list.append(wall)
            
            wall = arcade.Sprite("img/snakeBody.png", WALL_SCALING_BOX)
            wall.center_x = SCREEN_WIDTH - wall._width//2
            wall.center_y = wall._height//2 + wall._height*i 
            self.wall_list.append(wall)


        #Generate coins
        for i in range(COIN_COUNT):
            coin = arcade.AnimatedTimeSprite(scale=0.5)
            inside_walls = False
            while not inside_walls:
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)
                if ((coin.center_x >= wall._width) & (coin.center_x <= SCREEN_WIDTH - wall._width) & 
                (coin.center_y >= wall._height) & (coin.center_y <= SCREEN_HEIGHT - wall._height)):
                    inside_walls = True

            coin.textures = []
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_1.png"))
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_2.png"))
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_3.png"))
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_4.png"))
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_3.png"))
            coin.textures.append(arcade.load_texture(":resources:images/items/gold_2.png"))
            coin.scale = COIN_SCALE
            coin.cur_texture_index = random.randrange(len(coin.textures))

            self.coin_list.append(coin)
        

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)


        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.coin_list.draw()
        self.player_list.draw()
        self.wall_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.player.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Calculate seconds by using a modulus (remainder)
        self.seconds = self.total_time % 60

        # Figure out our output
        output = f"Time: {self.seconds:0.3f} seconds"

        # Output the timer text.
        arcade.draw_text(output, 630, 20, arcade.color.WHITE, 14)


    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:

            arcade.window_commands.close_window()

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time=1/60):
        """ Movement and game logic """

        # n = random.randint(1, 4)
        # key_action(n)

        self.coin_list.update()
        self.coin_list.update_animation()
        self.player_list.update()
        self.player_list.update_animation()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.player.score += 1
        
        self.total_time += delta_time

        self.physics_engine.update()


        #Reset game when ended
        if self.player.score == COIN_COUNT:
            print(f'COMPLETED ON TIME {self.seconds}')
            arcade.window_commands.close_window()


def main():
    """ Main method """
    window = TravellingSalesman(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()