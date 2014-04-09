import kivy
kivy.require('1.8.0') 

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader

class GameMenu(BoxLayout):
    def launchGame1(self):
        print "Launching ..."
    
class GameMenuApp(App):
    def build(self):
        return GameMenu();

#GameMenuApp().run()