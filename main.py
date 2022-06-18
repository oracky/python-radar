import arcade
from simulation.radar import Radar
from simulation.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


if __name__ == '__main__':
    radar = Radar(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    radar.setup()
    arcade.run()

