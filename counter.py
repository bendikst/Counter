import arcade
from screeninfo import get_monitors

monitors = get_monitors()

try:
    SCREEN_WIDTH = monitors[0].width
    SCREEN_HEIGHT = monitors[0].height
except Exception as e:
    print("Monitor resolution not found.")
    exit(1)

SCREEN_TITLE = "SCORE"

class StartButton(arcade.TextButton):
    def __init__(self, center_x, center_y, text_size, action_function):
        super().__init__(center_x, center_y, 360, 150, "START", font_size=text_size, shadow_color=arcade.color.RED, font_color=arcade.color.BLACK, button_height=0, face_color=arcade.color.RED)
        self.action_function = action_function


    def on_press(self):
        self.action_function()


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.score_to_win = 12
        self._start_text_size = 100
        self._start_pos_x = SCREEN_WIDTH//2
        self._start_pos_y = SCREEN_HEIGHT//4
        self.start_button = StartButton(self._start_pos_x, self._start_pos_y, self._start_text_size, self.on_start_button_pressed)


    def on_show(self):
        arcade.set_background_color(arcade.color.RED)
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Menu", SCREEN_WIDTH//2, SCREEN_HEIGHT - SCREEN_HEIGHT//4, arcade.color.BLACK, font_size=100, align="center",
                         anchor_x="center", anchor_y="center", bold=True)
        arcade.draw_text(f"Score to win: {self.score_to_win}", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.BLACK, font_size=100, align="center",
                         anchor_x="center", anchor_y="center", bold=True)
    
        self.start_button.draw()
    
    def on_mouse_press(self, x, y, button, _):
        self.start_button.check_mouse_press(x, y)

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.score_to_win += 1
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.score_to_win -= 1

    def on_start_button_pressed(self):
        counter = CounterView(self.score_to_win)
        self.window.show_view(counter)


class CounterView(arcade.View):
    def __init__(self, score_to_win):
        super().__init__()

        self.score_to_win = score_to_win
        self.text_angle = 0
        self.time_elapsed = 0.0
        self.score = 0
    

    def on_show(self):
        arcade.set_background_color(arcade.color.RED)

        self.window.set_mouse_visible(True)


    def on_update(self, delta_time):
        self.text_angle += 1
        if abs(self.score) < abs(self.score_to_win):
            self.time_elapsed += delta_time


    def on_mouse_press(self, x, y, button, _):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.score += 1
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.score -= 1


    def on_draw(self):
        arcade.start_render()
        
        start_y = SCREEN_HEIGHT//2
        start_x = SCREEN_WIDTH//2
        arcade.draw_text(str(self.score),
                         start_x, start_y, arcade.color.BLACK, 800, align="center",
                         anchor_x="center", anchor_y="center", bold=True)


        start_y = 100
        start_x = 100
        arcade.draw_text(f"Time elapsed: {self.time_elapsed:7.1f}",
                         start_x, start_y, arcade.color.BLACK, 20)
        

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()