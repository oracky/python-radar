from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel, UIFlatButton
from arcade.gui.events import UIOnChangeEvent, UIOnClickEvent
from simulation.shapes import Ellipse
from simulation.config import *


class RadarWidgetManager:
    def __init__(self, window : arcade.Window) -> None:
        self.window = window
        self.manager = UIManager()
        self.manager.enable()

    def setup(self) -> None:
        self.__setup_minimap()
        self.__setup_generative_widgets()
        self.__setup_speed_widgets()

    def draw(self) -> None:
        self.manager.draw()

    def __setup_minimap(self) -> None:
        label_minimap = UILabel(text=f"Live view", font_size=16)
        self.manager.add(UIAnchorWidget(child=label_minimap, align_y=130, align_x=-30, anchor_x='right', anchor_y='bottom'))

    def __setup_speed_widgets(self) -> None:
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
            self.window.speed = RADIANS_PER_FRAME * int(ui_radar_slider.value) / DEFAULT_PERCENTAGE_VALUE

        @ui_objects_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_objects.text = f"Objects speed: {int(ui_objects_slider.value)}%"
            label_objects.fit_content()
            self.window.update_objects_speed_range(5 * int(ui_objects_slider.value) // DEFAULT_PERCENTAGE_VALUE)

        @ui_radar_swape_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_radar_swape.text = f"Radar range:: {int(ui_radar_swape_slider.value)}%"
            label_radar_swape.fit_content()
            self.window.radar_range = ui_radar_swape_slider.value / DEFAULT_PERCENTAGE_VALUE
        

        self.manager.add(UIAnchorWidget(child=ui_radar_slider, align_y=-20, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_radar, align_x=20, align_y=-10, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_objects_slider, align_y=-80, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_objects, align_x=20, align_y=-70, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_radar_swape_slider, align_y=-140, anchor_x='left', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_radar_swape, align_x=20, align_y=-130, anchor_x='left', anchor_y='top'))

    def __setup_generative_widgets(self) -> None:
        self.window.shapes_number = 0

        ui_slider = UISlider(value=0, min_value=0, max_value=20, width=150, height=50)
        label_slider = UILabel(text=f"Number of objects: {int(ui_slider.value)}", font_size=10)
        generate_button = UIFlatButton(text="Generate new moving objects", width=200, style={'bg_color': arcade.color.DARK_SLATE_GRAY})

        @ui_slider.event()
        def on_change(event: UIOnChangeEvent):
            label_slider.text = f"Number of objects: {int(ui_slider.value)}"
            label_slider.fit_content()
            self.window.shapes_number = int(ui_slider.value)

        @generate_button.event()
        def on_click(event: UIOnClickEvent):
            self.window.setup_shapes(Ellipse, arcade.color.RED)


        self.manager.add(UIAnchorWidget(child=generate_button, align_y=-10, align_x=-10, anchor_x='right', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=ui_slider, align_y=-80, anchor_x='right', anchor_y='top'))
        self.manager.add(UIAnchorWidget(child=label_slider, align_x=-20, align_y=-70, anchor_x='right', anchor_y='top'))