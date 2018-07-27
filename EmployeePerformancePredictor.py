from pynput import keyboard, mouse
import matplotlib.pyplot as plt
import pandas as pd


class EmployeePerformancePredictor(object):
    def __init__(self):
        self.key_listener = None
        self.mouse_listener = None
        self.column = ["DATE","TIME", "PRESSED CHAR", "PRESSED COUNT", "RELEASED CHAR", "RELEASED COUNT", "MOUSE MOVE COUNT",
                       "MOUSE CLICKED COUNT", "MOUSE SCROLLED COUNT", "FINAL COUNT"]
        try:
            self.data_frame = pd.read_msgpack("EmployeeRawData.msg")
        except:
            self.data_frame = pd.DataFrame()
        self.key_pressed = []
        self.key_released = []
        self.key_pressed_count = 0
        self.key_released_count = 0
        self.mouse_move_count = 0
        self.mouse_clicked_count = 0
        self.mouse_scrolled_count = 0
        self.count = 0
        self.data = []
        self.index = pd.datetime.now().strftime("%y/%m/%d_%H:%M")
        self.date_index = pd.datetime.now().strftime("%y/%m/%d")

    def start_processing(self):
        while True:
            self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
            self.key_listener.start()
            self.mouse_listener.start()
            while self.index == pd.datetime.now().strftime("%y/%m/%d_%H:%M"):
                pass
            self.count = self.key_pressed_count + self.mouse_move_count + self.mouse_clicked_count + self.mouse_scrolled_count
            self.data = [[self.index.split("_")[0], self.index.split("_")[1],"N/A", self.key_pressed_count, "N/A", self.key_released_count,
                          self.mouse_move_count, self.mouse_clicked_count, self.mouse_scrolled_count, self.count]]
            if self.data_frame.empty:
                self.data_frame = pd.DataFrame(data=self.data, columns=self.column)
            else:
                self.data_frame = self.data_frame.append(pd.DataFrame(data=self.data, columns=self.column))
            self.index = pd.datetime.now().strftime("%y/%m/%d_%H:%M")
            self.key_listener.stop()
            self.mouse_listener.stop()
            self.data_reset()
            self.data_frame.to_msgpack("EmployeeRawData.msg")

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
        self.count = 0
        self.data = []


if __name__ == '__main__':
    ROOT = EmployeePerformancePredictor()
    ROOT.start_processing()
