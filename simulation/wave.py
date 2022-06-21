import arcade
import datetime
import math
from simulation.config import *
from simulation.shapes import Shape


class Wave:
    def __init__(self, x : float, y : float, color : arcade.Color, maximum_radius : float = SWEEP_LENGTH,
     init_radius : float = INIT_WAVE_RADIUS, initial_delay : datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.maximum_radius = maximum_radius
        self.init_radius = init_radius
        self.initial_delay = initial_delay
        self.radius = self.init_radius
        self.radius_delta = RADIUS_DELTA
        self.started_time = datetime.datetime.now()
        self.started = False

    def draw_wave(self) -> None:
        if self.started:
            arcade.draw_circle_outline(self.x, self.y, self.radius, color=self.color, border_width=1)

    def update_radius(self) -> None:
        if self.started:
            if self.is_in_range():
                self.radius += self.radius_delta
            else:
                self.radius = self.init_radius
        else:
            self.__hold_on_delay()

    def is_in_range(self) -> bool:
        return self.radius <= self.maximum_radius

    def is_shape_in_wave(self, shape : Shape):
        return (shape.x - CENTER_X) ** 2 + (shape.y - CENTER_Y) ** 2 - self.radius ** 2 < 0

    def __hold_on_delay(self) -> None:
        if datetime.datetime.now() - self.started_time > self.initial_delay:
            self.started = True
    

class RadarWave(Wave):
    def __init__(self, x: float, y: float, color: arcade.Color = arcade.color.GREEN, maximum_radius : float = SWEEP_LENGTH,
     init_radius : float = INIT_WAVE_RADIUS, initial_delay : datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        super().__init__(x, y, color, maximum_radius, init_radius, initial_delay)


class ObjectWave(Wave):
    def __init__(self, x: float, y: float, color: arcade.Color = arcade.color.BROWN, maximum_radius : float = SWEEP_LENGTH,
     init_radius : float = INIT_WAVE_RADIUS, initial_delay : datetime.timedelta = datetime.timedelta(seconds=0)) -> None:
        super().__init__(x, y, color, maximum_radius, init_radius, initial_delay)
        self.active = True

    def is_in_range(self) -> bool:
        if self.radius + self.__get_distance_from_center() > self.maximum_radius:
            self.active = False
            return False
        if self.radius + self.__get_distance_from_center() > self.maximum_radius:
            self.active = False
            return False
        return True

    def __get_distance_from_center(self):
        return math.sqrt(abs(self.x - CENTER_X) ** 2 + abs(self.y - CENTER_Y) ** 2)