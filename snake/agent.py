from random import randint
from pynput.keyboard import Key, Controller
from time import sleep
from snake.player import PlayerCharacter


MOVEMENT_MAPPING = {
    1: Key.up,
    2: Key.down,
    3: Key.left,
    4: Key.right
}

keyboard = Controller()

def key_action(n):
    key_press = MOVEMENT_MAPPING[n]
    keyboard.press(key_press)
    keyboard.release(key_press)



# def is_divergent(game):
#     game.player
#     return 


if __name__ == "__main__":
    sleep(5)
    
    keyboard = Controller()

    for i in range(10000):
        key_press = MOVEMENT_MAPPING[randint(1, 4)]
        keyboard.press(key_press)
        keyboard.release(key_press)