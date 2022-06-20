import arcade
from simulation.config import *


class Wave:
    def __init__(self, x : float, y : float, color : arcade.Color, maximum_radius : float = SWEEP_LENGTH, init_radius : float = INIT_WAVE_RADIUS) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.maximum_radius = maximum_radius
        self.init_radius = init_radius
        self.radius = self.init_radius
        self.radius_delta = 1

    def draw_wave(self) -> None:
        arcade.draw_circle_outline(self.x, self.y, self.radius, color=self.color, border_width=2)

    def update_radius(self) -> None:
        if self.is_in_range():
            self.radius += self.radius_delta
        else:
            self.radius = self.init_radius

    def is_in_range(self) -> bool:
        return self.radius <= self.maximum_radius
    

class RadarWave(Wave):
    def __init__(self, x: float, y: float, color: arcade.Color = arcade.color.GREEN) -> None:
        super().__init__(x, y, color)


class ObjectWave(Wave):
    def __init__(self, x: float, y: float, color: arcade.Color = arcade.color.YELLOW) -> None:
        super().__init__(x, y, color)

    def is_in_range(self) -> bool:
        if self.radius + self.x > self.maximum_radius:
            return False
        if self.radius + self.y > self.maximum_radius:
            return False
        return True