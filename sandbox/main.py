from core.window import Window
import kivy
from kivy.app import App
from kivy.clock import ClockEvent
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.popup import Popup
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from uix.button import Button

from gameMenu import GameMenuApp


kivy.require('1.8.0') 

class Test(Layout):
    button_box = ObjectProperty()
    
    def update(self,dt):
        pass
    
    def playVideo(self, chaine):
        layout = BoxLayout(orientation='vertical')
        video = Video(source=chaine, state='play', size_hint=(1, 0.9));
        layout.add_widget(video);
        button = Button(text='Revenir au jeu', size_hint=(1, 0.1))
        layout.add_widget(button)
        popup = Popup(title='Ecoute bien ! ',
                      content=layout,
                      size_hint=(None, None),
                      size=(600, 600),
                      auto_dismiss=False
                      )
        button.bind(on_press=popup.dismiss)
        popup.open();


class Main(App):
    def build(self):
        test = Test()
        Clock.schedule_interval(test.update, 10.)
        return Test();

Main().run()
