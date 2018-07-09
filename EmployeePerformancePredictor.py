from pynput import keyboard, mouse
import pandas as pd
import time


class EmployeePerformancePredictor(object):
    def __init__(self):
        self.key_listener = None
        self.mouse_listener = None
        self.column = ["PRESSED CHAR", "PRESSED COUNT", "RELEASED CHAR", "RELEASED COUNT", "MOUSE MOVE COUNT",
                       "MOUSE CLICKED COUNT", "MOUSE SCROLLED COUNT", "FINAL COUNT"]
        self.data_frame = pd.DataFrame()
        self.key_pressed = []
        self.key_released = []
        self.key_pressed_count = 0
        self.key_released_count = 0
        self.mouse_move_count = 0
        self.mouse_clicked_count = 0
        self.mouse_scrolled_count = 0
        self.data = []
        self.index = None

    def start_processing(self):
        while True:
            self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
            self.key_listener.start()
            while self.index != pd.datetime.now().strftime("%y/%m/%d_%H:%M"):
                self.data = [[self.key_pressed, self.key_pressed_count, self.key_released, self.key_released_count,
                              self.mouse_move_count, self.mouse_clicked_count, self.mouse_scrolled_count, "N/A"]]
                self.index = pd.datetime.now().strftime("%y/%m/%d_%H:%M")
                if self.data_frame.empty:
                    self.data_frame = pd.DataFrame(data=self.data, columns=self.column, index=[self.index])
                else:
                    self.data_frame = self.data_frame.append(pd.DataFrame(data=self.data, columns=self.column, index=[self.index]))
                self.key_listener.stop()
                print(self.data_frame)
                self.data_reset()

    def on_press(self, key):
        self.key_pressed_count += 1
        try:
            self.key_pressed.append(key.char)
        except AttributeError:
            self.key_pressed.append(key.name)

    def on_release(self, key):
        self.key_released_count += 1
        try:
            self.key_released.append(key.char)
        except AttributeError:
            self.key_released.append(key.name)

    def on_move(self, x, y):
        self.mouse_move_count += 1

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicked_count += 1
        if not pressed:
            return False

    def on_scroll(self, x, y, dx, dy):
        self.mouse_scrolled_count += 1

    def data_reset(self):
        self.key_pressed = []
        self.key_released = []
        self.key_pressed_count = 0
        self.key_released_count = 0
        self.mouse_move_count = 0
        self.mouse_clicked_count = 0
        self.mouse_scrolled_count = 0
        self.data = []


if __name__ == '__main__':
    ROOT = EmployeePerformancePredictor()
    ROOT.start_processing()
