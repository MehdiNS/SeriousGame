import kivy
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import os

import dataBase
from gameMenu import GameMenuApp


class ExportDialog(BoxLayout):
    export = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Intro(BoxLayout):
    id_box = ObjectProperty()
    id_grid = ObjectProperty()
    button_box = ObjectProperty()
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    

    def login(self):
        print(self.id_box.text)
        if self.id_box.text == "test":
            self.id_box.background_color = [0.4,1,0.7,1]
            self.remove_widget(self.button_box)
            self.remove_widget(self.id_box)
            self.remove_widget(self.id_grid)
            return GameMenuApp().run();
        else:
            self.id_box.background_color = [1,0.4,0.4,1]
    
    def show_export(self):
        content = ExportDialog(export=self.export, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
        
    def dismiss_popup(self):
        self._popup.dismiss()
        
    def export(self, path, filename):
        db = dataBase.DataBase()
        str = path+'/'+filename
        print str
        db.JSonToCSV(db.SQliteToJSOn("Game3"),str,[])
        self.dismiss_popup()

class Main(App):
    def build(self):
        return Intro();

Main().run()
