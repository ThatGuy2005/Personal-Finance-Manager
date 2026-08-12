from PyQt6.QtWidgets import QPushButton

from windows import Window

from decimal import Decimal

def to_float(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, str) and val.endswith('%'):
        return float(val.rstrip('%'))
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            return val
    return val

# Rewrite to take *args
def add_widgets_to_window(window: Window, widgets: list) -> None:
        """Takes a list of widgets and puts them on the window.
        The buttons are put on the layout. This function will call
        show_widgets!!!"""
        for widget in widgets:
                window.add_widget(widget)

        window.show_widgets()

def create_pushbutton(parent, label, callback=None) -> QPushButton:
        """Given some data it creates a button."""
        if callback is not None:
                b = QPushButton(parent, text=label)
                b.clicked.connect(callback)
                return b
        return QPushButton(parent,text=label)