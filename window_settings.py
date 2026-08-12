from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect

class Settings():
    """A class that holds the settings of the main window."""

    def __init__(self):
        rect = QGuiApplication.primaryScreen().availableGeometry()
        self.x = rect.x()
        self.y = rect.y()
        self.width = rect.width() - 10
        self.height = rect.height() - 50

        self.button_width = 100
        self.button_height = 50

        self.page_width = 300
        self.page_height = 400

        self.scroll_widget_w = 500
        self.scroll_widget_h = 500

        self.margin = 50

    def get_centerx(self):
        return self.width//2
    
    def get_centery(self):
        return self.height//2
    
    def get_screen_size(self):
        obj = QGuiApplication.primaryScreen().availableGeometry()
        x, y, width, height = obj.x(), obj.y(), obj.width(), obj.height()
        rect = QRect(x, y, width-10, height-50)
        return rect
    
    def get_left(self):
        return 0
    
    def get_right(self):
        return self.width
    
    def get_top(self):
        return 0
    
    def get_bottom(self):
        return self.height