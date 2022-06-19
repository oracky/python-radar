from dataclasses import dataclass
import arcade
import math
import datetime
from uuid import uuid4
from typing import Type
from simulation.shapes import StableRectangle, Ellipse, Shape
from simulation.utils import Point2D
from simulation.config import *
from simulation.widget_manager import RadarWidgetManager

Numerical = int or float

@dataclass
class RadarListElement:
    radar_time_stamp : datetime.datetime
    shape : Shape
    id : int

    def is_active(self, current_timestamp : datetime.datetime, seconds_to_refresh : float = RADAR_REFRESH_TIME) -> bool:
        return current_timestamp - self.radar_time_stamp < datetime.timedelta(seconds=seconds_to_refresh)


class Radar(arcade.Window):
    def __init__(self, width : int, height : int, title : str, speed : float = RADIANS_PER_FRAME, minimap_ratio : Numerical = MINIMAP_RATIO,
     shapes_number : int = NUMBER_OF_SHAPES, objects_speed : int = OBJECTS_DEFAULT_SPEED, radar_range : float = RADAR_RANGE) -> None:
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.draw_time = 0
        self.angle = 0
        self.speed = speed
        self.radar_range = radar_range
        self.radar_discovered_objects : 'list[RadarListElement]' = []
        self.objects_speed = objects_speed
        self.shapes_number = shapes_number
        self.shape_list : 'list[Shape]' = None
        self.x1 = CENTER_X
        self.x2 = CENTER_X
        self.y1 = CENTER_Y
        self.y1 = CENTER_Y

        self.widget_manager = RadarWidgetManager(self)
        
        self.minimap_ratio = minimap_ratio
        self.minimap_width = int(self.width / self.minimap_ratio)
        self.minimap_height = int(self.minimap_width * self.height / self.width)
        self.minimap_sprite_list = None
        self.minimap_texture = None
        self.minimap_sprite = None

    def setup(self) -> None:
        self.__setup_base()
        self.__setup_minimap()

    def setup_shapes(self, shape_class : Type[Shape], color : arcade.Color) -> None:
        for _ in range(self.shapes_number):
            x, y = Shape.randomize_position(self.width, self.height)
            width, height = Shape.randomize_size()
            angle = Shape.randomize_angle()
            d_x, d_y, d_angle = Shape.randomize_movement(self.objects_speed)

            shape = shape_class(x, y, width, height, angle, d_x, d_y,
                                  d_angle, color)
            
            self.shape_list.append(shape)

    def update_speed(self, speed : float) -> None:
        self.speed = speed

    def update_objects_speed_range(self, objects_speed) -> None:
        self.objects_speed = objects_speed
        for shape in self.shape_list:
            shape.delta_x, shape.delta_y, shape.delta_angle = Shape.randomize_movement(self.objects_speed)

    def __setup_base(self) -> None:
        self.shape_list = []
        self.setup_shapes(StableRectangle, arcade.color.AERO_BLUE)
        self.setup_shapes(Ellipse, arcade.color.RED)
        self.widget_manager.setup()

    def __setup_minimap(self) -> None:
        size = (self.minimap_width, self.minimap_height)
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=self.width - self.minimap_width / 2,
                                            center_y=self.minimap_height / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

    def __update_minimap(self) -> None:
        proj = 0, MAP_WIDTH, 0, MAP_HEIGHT
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.__update_radar(minimap=True)
            self.__draw_shapes_minimap()

    def __update_angle(self) -> None:
        self.angle += self.speed
        if self.angle > 2 * math.pi:
            self.angle = 0.0

    def __draw_shapes_minimap(self) -> None:
        for shape in self.shape_list:
            shape.draw()

    def __draw_shapes(self) -> None:
        for element in self.radar_discovered_objects:
            element.shape.draw()

    def __update_discoveries(self) -> None:
        for shape in self.shape_list:
            if shape.is_in_range(Point2D(CENTER_X, CENTER_Y), Point2D(self.x1, self.y1), Point2D(self.x2, self.y2)):
                new_shape = shape.from_shape(shape)
                if id(shape) not in (elem.id for elem in self.radar_discovered_objects):
                    self.radar_discovered_objects.append(RadarListElement(datetime.datetime.now(), new_shape, id(shape)))
        
        updated_discoveries = [elem for elem in self.radar_discovered_objects if elem.is_active(datetime.datetime.now())]
        self.radar_discovered_objects = updated_discoveries
    
    def __update_radar(self, minimap : bool = False) -> None:
        self.x1 = SWEEP_LENGTH * math.sin(self.angle) + CENTER_X
        self.y1 = SWEEP_LENGTH * math.cos(self.angle) + CENTER_Y
        self.x2 = SWEEP_LENGTH * math.sin(self.angle + self.radar_range) + CENTER_X
        self.y2 = SWEEP_LENGTH * math.cos(self.angle + self.radar_range) + CENTER_Y
        
        arcade.draw_circle_outline(CENTER_X, CENTER_Y, SWEEP_LENGTH + 1,
							arcade.color.DARK_GREEN, 10)
        if not minimap:
            arcade.draw_line(CENTER_X, CENTER_Y, self.x1, self.y1, arcade.color.OLIVE, 4)
            arcade.draw_line(CENTER_X, CENTER_Y, self.x2, self.y2, arcade.color.OLIVE, 4)

    def on_update(self, _) -> None:
        for shape in self.shape_list:
            shape.move()

    def on_draw(self) -> None:
        self.__update_angle()

        arcade.start_render()
        self.__update_radar()
        self.widget_manager.draw()
        
        self.__update_minimap()
        self.__update_discoveries()
        self.__draw_shapes()

        self.minimap_sprite_list.draw()
