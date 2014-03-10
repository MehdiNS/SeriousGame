import kivy
kivy.require('1.8.0') 

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from sg.game1 import Game1App

class Intro(BoxLayout):
    id_box = ObjectProperty()
    id_grid = ObjectProperty()
    button_box = ObjectProperty()
    
    def login(self):
        print(self.id_box.text)
        if self.id_box.text == "test":
            self.id_box.background_color = [0.4,1,0.7,1]
            self.remove_widget(self.button_box)
            self.remove_widget(self.id_box)
            self.remove_widget(self.id_grid)
            return Game1App().run();
        else:
            self.id_box.background_color = [1,0.4,0.4,1]



class Main(App):
    def build(self):
        return Intro();

Main().run()
