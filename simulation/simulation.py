import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Shape List Demo 3"

HALF_SQUARE_WIDTH = 2.5
HALF_SQUARE_HEIGHT = 2.5
SQUARE_SPACING = 10

test_point = [[(1,1),(20,50), (40,70), (60,190)], [(210, 100), (51, 300), (100,300), (200,500)]]

class Simulation(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.draw_time = 0
        self.shape_list = None

    def setup(self):
        self.shape_list = arcade.ShapeElementList()

        # --- Create all the rectangles

        # We need a list of all the points and colors
        point_list = []
        color_list = []

        for rec in test_point:
            point_list.extend(rec)
            color_list.extend((arcade.color.DARK_BLUE for _ in range(4)))
            
        shape = arcade.create_rectangles_filled_with_colors(point_list, color_list)
        self.shape_list.append(shape)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Start timing how long this takes
        # draw_start_time = timeit.default_timer()

        # --- Draw all the rectangles
        self.shape_list.draw()

        # output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
        # arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18)

        # self.draw_time = timeit.default_timer() - draw_start_time