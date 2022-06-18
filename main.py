import arcade
from simulation.radar import Radar

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Radar Sweep Example"
RADIANS_PER_FRAME = 0.02


if __name__ == '__main__':
    radar = Radar(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, RADIANS_PER_FRAME)
    radar.setup()
    arcade.run()

