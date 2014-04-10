import kivy
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from game2 import Game2App
from game3 import Game3App


kivy.require('1.8.0') 


class GameMenu(BoxLayout):
    def launchGame1(self):
        return Game2App().run();
    
    def launchGame2(self):
        return Game3App().run();
    
class GameMenuApp(App):
    def build(self):
        return GameMenu();

#GameMenuApp().run()