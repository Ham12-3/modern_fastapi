from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder


# Custom styles using Kivy’s Builder for rounded corners and background styles
Builder.load_string('''
<StyledButton>:
    background_normal: ''
    background_color: (0, 0, 0, 0)
    color: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]
''')

from backend import Youtubedownloader

from tkinter import filedialog

Window.clearcolor = get_color_from_hex('#FFFFFF')



class StyledButton(Button):
    pass
class DownloaderGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        