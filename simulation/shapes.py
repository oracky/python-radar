from __future__ import annotations
from typing import Type
import arcade
import random
from simulation.utils import Point2D, PointHelper
from simulation.config import *

class Shape:
    RECT_MAX_SIZE = 30
    RECT_MIN_SIZE = 10

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color
        self.shape_list = None
        self.moving = True

    def move(self) -> None:
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle
        if self.x < 0 and self.delta_x < 0:
            self.delta_x *= -1
        if self.y < 0 and self.delta_y < 0:
            self.delta_y *= -1
        if self.x > SCREEN_WIDTH and self.delta_x > 0:
            self.delta_x *= -1
        if self.y > SCREEN_HEIGHT and self.delta_y > 0:
            self.delta_y *= -1

    def draw(self) -> None:
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        self.shape_list.draw()


    def is_in_range(self, v1 : Point2D, v2 : Point2D, v3 : Point2D) -> bool:
        return PointHelper.is_point_in_triangle(Point2D(self.x, self.y), v1, v2, v3)

    def from_shape(self, instance : Shape) -> Shape:
        return Shape(instance.x, instance.y, instance.width, instance.height, instance.angle, instance.delta_x, instance.delta_y, instance.delta_angle, arcade.color.GREEN)

    @staticmethod
    def randomize_movement(speed : int) -> 'tuple[int, int, int]':
        if speed == 0:
            return (0, 0, 0)

        d_x = random.randrange(-1 * speed, 1 * speed)
        d_y = random.randrange(-1 * speed, 1 * speed)
        d_angle = random.randrange(-3, 4)

        return (d_x, d_y, d_angle)

    @staticmethod
    def randomize_position(screen_width : int, screen_height : int) -> 'tuple[int, int]':
        x = random.randrange(0, screen_width)
        y = random.randrange(0, screen_height)

        return (x, y)

    @staticmethod
    def randomize_size() -> 'tuple[int, int]':
        width = random.randrange(Shape.RECT_MIN_SIZE, Shape.RECT_MAX_SIZE)
        height = random.randrange(Shape.RECT_MIN_SIZE, Shape.RECT_MAX_SIZE)

        return (width, height)

    @staticmethod
    def randomize_angle() -> int:
        return random.randrange(0, 360)


class Ellipse(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color) -> None:

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_ellipse_filled(0, 0,
                                             self.width, self.height,
                                             self.color, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)
    
    def from_shape(self, instance : Shape) -> Shape:
        return Ellipse(instance.x, instance.y, instance.width, instance.height, instance.angle, instance.delta_x, instance.delta_y, instance.delta_angle, arcade.color.GREEN)



class Rectangle(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color) -> None:

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_rectangle_filled(0, 0,
                                               self.width, self.height,
                                               self.color, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)

    def from_shape(self, instance : Shape) -> Shape:
        return Rectangle(instance.x, instance.y, instance.width, instance.height, instance.angle, instance.delta_x, instance.delta_y, instance.delta_angle, arcade.color.GREEN)


class Line(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color) -> None:

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_line(0, 0,
                                   self.width, self.height,
                                   self.color, 2)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)

    def from_shape(self, instance : Shape) -> Shape:
        return Line(instance.x, instance.y, instance.width, instance.height, instance.angle, instance.delta_x, instance.delta_y, instance.delta_angle, arcade.color.GREEN)

class StableRectangle(Rectangle):
    def __init__(self, x, y, width, height, angle, delta_x, delta_y, delta_angle, color) -> None:
        super().__init__(x, y, width, height, angle, delta_x, delta_y, delta_angle, color)

        self.moving = False

    def from_shape(self, instance : Shape) -> Shape:
        return StableRectangle(instance.x, instance.y, instance.width, instance.height, instance.angle, instance.delta_x, instance.delta_y, instance.delta_angle, arcade.color.GREEN)

    def move(self) -> None:
        pass