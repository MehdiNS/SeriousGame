from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import time


class Object(Widget):
    
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y

            
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                sound = SoundLoader.load(self.text)
                sound.play()
                return;
            self.opacity = 0.2
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y
            self.opacity = 1
            touch.ungrab(self)
            return True

    

class Game1(Widget):
    
    def update(self, dt):
        pass
    
    def on_winning(self, touch):
        pass


class Game1App(App):
    def build(self):
        game = Game1()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    Game1App().run()