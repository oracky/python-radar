from dataclasses import dataclass
import arcade
import math
import datetime
from uuid import uuid4
from typing import Type
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel, UIFlatButton
from arcade.gui.events import UIOnChangeEvent, UIOnClickEvent
from simulation.shapes import StableRectangle, Ellipse, Shape
from simulation.utils import Point2D

Numerical = int or float

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Radar Sweep Example"

# These constants control the particulars
# about the radar
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.04
RADAR_RANGE = 1.0 # in radians
DEFAULT_PERCENTAGE_VALUE = 50
SWEEP_LENGTH = 250
RADAR_REFRESH_TIME = 3.0


# Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.DARK_SLATE_GRAY)
MAP_WIDTH = 800
MAP_HEIGHT = 600

@dataclass
class RadarListElement:
    radar_time_stamp : datetime.datetime
    shape : Shape
    id : int

    def is_active(self, current_timestamp : datetime.datetime, seconds_to_refresh : float = RADAR_REFRESH_TIME):
        return current_timestamp - self.radar_time_stamp < datetime.timedelta(seconds=seconds_to_refresh)


class Radar(arcade.Window):
    def __init__(self, width : int, height : int, title : str, speed : float = RADIANS_PER_FRAME, minimap_ratio : Numerical = 5,
     shapes_number : int = 10, objects_speed : int = 1, radar_range : float = RADAR_RANGE):
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

        self.manager = UIManager()
        self.manager.enable()
        
        
        # Mini-map related
        self.minimap_ratio = minimap_ratio
        self.minimap_width = int(self.width / self.minimap_ratio)
        self.minimap_height = int(self.minimap_width * self.height / self.width)
        self.minimap_sprite_list = None
        # Texture and associated sprite to render our minimap to
        self.minimap_texture = None
        self.minimap_sprite = None


    def setup(self):
        # Setup base objects
        self.shape_list = []
        self.__setup_shapes(StableRectangle, arcade.color.AERO_BLUE)
        self.__setup_shapes(Ellipse, arcade.color.RED)
        self.__setup_speed_widgets()
        self.__setup_generative_widgets()

        # Construct the minimap
        size = (self.minimap_width, self.minimap_height)
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=self.width - self.minimap_width / 2,
                                            center_y=self.minimap_height / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

        label_minimap = UILabel(text=f"Live view", font_size=16)
        self.manager.add(UIAnchorWidget(child=label_minimap, align_y=130, align_x=-30, anchor_x='right', anchor_y='bottom'))

    def update_speed(self, speed):
        self.speed = speed

    def update_objects_speed_range(self, objects_speed):
        self.objects_speed = objects_speed
        for shape in self.shape_list:
            shape.delta_x, shape.delta_y, shape.delta_angle = Shape.randomize_movement(self.objects_speed)

    def __setup_speed_widgets(self):
        ui_radar_slider = UISlider(value=DEFAULT_PERCENTAGE_VALUE, min_value=0, max_value=100, width=150, height=50)
        label_radar = UILabel(text=f"Radar speed: {int(ui_radar_slider.value)}%", font_size=10)

        ui_objects_slider = UISlider(value=DEFAULT_PERCENTAGE_VALUE, min_value=0, max_value=100, width=150, height=50)
        label_objects = UILabel(text=f"Objects speed: {int(ui_radar_slider.value)}%", font_size=10)

        ui_radar_swape_slider = UISlider(value=DEFAULT_PERCENTAGE_VALUE, min_value=0, max_value=100, width=150, height=50)
        label_radar_swape = UILabel(text=f"Radar range: {int(ui_radar_swape_slider.value)}%", font_size=10)

        @ui_radar_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_radar.text = f"Radar speed: {int(ui_radar_slider.value)}%"
            label_radar.fit_content()
            self.speed = RADIANS_PER_FRAME * int(ui_radar_slider.value) / DEFAULT_PERCENTAGE_VALUE

        @ui_objects_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_objects.text = f"Objects speed: {int(ui_objects_slider.value)}%"
            label_objects.fit_content()
            self.update_objects_speed_range(5 * int(ui_objects_slider.value) // DEFAULT_PERCENTAGE_VALUE)

        @ui_radar_swape_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_radar_swape.text = f"Radar range:: {int(ui_radar_swape_slider.value)}%"
            label_radar_swape.fit_content()
            self.radar_range = ui_radar_swape_slider.value / DEFAULT_PERCENTAGE_VALUE
        

        self.manager.add(UIAnchorWidget(child=ui_radar_slider, align_y=-20, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_radar, align_x=20, align_y=-10, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_objects_slider, align_y=-80, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_objects, align_x=20, align_y=-70, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_radar_swape_slider, align_y=-140, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_radar_swape, align_x=20, align_y=-130, anchor_x='left', anchor_y='top'))

    def __setup_generative_widgets(self):
        self.shapes_number = 0

        ui_slider = UISlider(value=0, min_value=0, max_value=20, width=150, height=50)
        label_slider = UILabel(text=f"Number of objects: {int(ui_slider.value)}", font_size=10)
        generate_button = UIFlatButton(text="Generate new moving objects", width=200, style={'bg_color': arcade.color.DARK_SLATE_GRAY})

        @ui_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_slider.text = f"Number of objects: {int(ui_slider.value)}"
            label_slider.fit_content()
            self.shapes_number = int(ui_slider.value)

        @generate_button.event()
        def on_click(event: UIOnClickEvent):
            self.__setup_shapes(Ellipse, arcade.color.RED)


        self.manager.add(UIAnchorWidget(child=generate_button, align_y=-10, align_x=-10, anchor_x='right', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_slider, align_y=-80, anchor_x='right', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_slider, align_x=-20, align_y=-70, anchor_x='right', anchor_y='top'))


    def __setup_shapes(self, shape_class : Type[Shape], color : arcade.Color):
        for _ in range(self.shapes_number):
            x, y = Shape.randomize_position(self.width, self.height)
            width, height = Shape.randomize_size()
            angle = Shape.randomize_angle()
            d_x, d_y, d_angle = Shape.randomize_movement(self.objects_speed)

            shape = shape_class(x, y, width, height, angle, d_x, d_y,
                                  d_angle, color)
            
            self.shape_list.append(shape)

    def __update_minimap(self):
        proj = 0, MAP_WIDTH, 0, MAP_HEIGHT
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.__update_radar(minimap=True)
            self.__draw_shapes_minimap()

    def __update_angle(self):
        self.angle += self.speed
        if self.angle > 2 * math.pi:
            self.angle = 0.0

    def __draw_shapes_minimap(self):
        for shape in self.shape_list:
            shape.draw()

    def __draw_shapes(self):
        for element in self.radar_discovered_objects:
            element.shape.draw()

    def __update_discoveries(self):
        for shape in self.shape_list:
            if shape.is_in_range(Point2D(CENTER_X, CENTER_Y), Point2D(self.x1, self.y1), Point2D(self.x2, self.y2)):
                new_shape = Shape.from_shape(Ellipse, shape)
                if id(shape) not in (elem.id for elem in self.radar_discovered_objects):
                    self.radar_discovered_objects.append(RadarListElement(datetime.datetime.now(), new_shape, id(shape)))
        
        updated_discoveries = [elem for elem in self.radar_discovered_objects if elem.is_active(datetime.datetime.now())]
        self.radar_discovered_objects = updated_discoveries
    
    def __update_radar(self, minimap : bool = False):
        self.x1 = SWEEP_LENGTH * math.sin(self.angle) + CENTER_X
        self.y1 = SWEEP_LENGTH * math.cos(self.angle) + CENTER_Y
        self.x2 = SWEEP_LENGTH * math.sin(self.angle + self.radar_range) + CENTER_X
        self.y2 = SWEEP_LENGTH * math.cos(self.angle + self.radar_range) + CENTER_Y
        
        arcade.draw_circle_outline(CENTER_X, CENTER_Y, SWEEP_LENGTH + 1,
							arcade.color.DARK_GREEN, 10)
        if not minimap:
            arcade.draw_line(CENTER_X, CENTER_Y, self.x1, self.y1, arcade.color.OLIVE, 4)
            arcade.draw_line(CENTER_X, CENTER_Y, self.x2, self.y2, arcade.color.OLIVE, 4)

    def on_update(self, dt):
        """ Move everything """

        for shape in self.shape_list:
            shape.move()

    def on_draw(self):
        self.__update_angle()

        arcade.start_render()
        self.__update_radar()
        self.manager.draw()
        
        # Update the minimap
        self.__update_minimap()
        self.__update_discoveries()
        self.__draw_shapes()

        # Draw the minimap
        self.minimap_sprite_list.draw()
