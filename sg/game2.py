from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import OptionProperty, NumericProperty, ListProperty
import time


class Object(Widget):
    """Class to manage drag and drop
   
    """
    print("Salut")
    
      
        
    def on_touch_move(self, touch):
        """Function called when the object is moved
        
        :param touch: finger on the screen     
        
        """
        
        
        #If the current object is the one grab
        if touch.grab_current is self:
            print("pos_base"+str(self.pos_base)+"\n")
            #print("old_x :"+str(self.old_x)+"old_y"+str(self.old_y)+"\n")
            #print("On_touch_move activated"+str(self.x)+"\n")
            self.center_x = touch.x
            self.center_y = touch.y

            
    
    def on_touch_down(self, touch):
        """Function called when the object is double clicked
        
        :param touch: finger on the screen     
        
        """  
        
        if self.collide_point(*touch.pos):
            print("On_touch_down activated"+str(self.x)+"\n")  
            if touch.is_double_tap:                
                sound = SoundLoader.load(self.text)
                sound.play()
                return;
            self.opacity = 0.2
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        """Function called when the object is dropped after a move
        
        :param touch: finger on the screen     
        
        """
        print(self.name)
        if (self.category=="cat_house"):
            print("house found")
            mem = self
        #If this is the correct object
        if touch.grab_current is self:            
            if self.collide_widget(mem):
                print("touch")
            #If the object isn't dropped on a category, x and y are reset
            if self.x>400 :
                print(str(self.pos_base))
                self.pos = self.pos_base
                
                self.opacity = 1
                #The object is dropped
                touch.ungrab(self)
                return True
            #Else the object isn't visible anymore and old_x, old_y are set
            else :
                #The object is dropped and removed
                touch.ungrab(self)
                print(str(self))
                self.parent.remove_widget(self)
                return True

class Category(Widget):
  '''  
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
'''
class Game2(Widget):
    
    def update(self, dt):
        pass
    
    def on_winning(self, touch):
        pass
    def get_Widget(self):
        return self.Widget

class Game2App(App):
    def build(self):
        game = Game2()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    Game2App().run()