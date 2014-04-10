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
    """Class to represent the menu
    """   
    
    def launchGame1(self):
        """Function which launch the first game
        """
        return Game2App().run();
    
    def launchGame2(self):
        """Function which launch the second game
        """
        return Game3App().run();
    
class GameMenuApp(App):
    """Class to launch the menu
    """   
    def build(self):
        """Function which constructs the menu
        """
        return GameMenu();

#GameMenuApp().run()