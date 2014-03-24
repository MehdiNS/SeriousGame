from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import OptionProperty, NumericProperty, ListProperty, ReferenceListProperty,\
    ObjectProperty
import time


class Object(Widget):
    """Class to manage drag and drop
   
    """
    print("Salut")
    #print(parent.touched_object)
      
        
    def on_touch_move(self, touch):
        """Function called when the object is moved
        
        :param touch: finger on the screen     
        
        """
        
        
        #If the current object is the one grab
        if touch.grab_current is self:
            
            self.parent.touched_object = self
            print(self)
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
        print("\n")
        print(self.category)
        print(touch.grab_current)
        print("\n")
        mem = Object()
        if (self.category=="cat_house"):
            print("house found")
            mem = self
            print("mem :")
            print(mem)
        #If this is the correct object
        if touch.grab_current is self:            
            if self.collide_widget(mem):
                print("touched dkldklzdqdqkzl")
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

class CategoryHouse(Widget):
    '''       

'''
    
class CategoryVehicle(Widget):
    '''       

'''

class CategoryCharacter(Widget):
    '''       

'''
class Game2(Widget):
    
    #Define the three categories
    category_house = ObjectProperty(None)
    category_vehicle = ObjectProperty(None)
    category_character = ObjectProperty(None)
    
    #Define the object touched
    touched_object = ObjectProperty(None)
    
    def update(self, dt, touch):
        if (self.category_house.collide_point(touch.pos)):
            print("Maison touchee")
        #if ((self.touched_object.category == self.category_house.category) 
            #and (self.category_house.collide_point())):
            #print("Well done !")
        #self.ball.move()

        #bounce off top and bottom
        #if (self.ball.y < 0) or (self.ball.top > self.height):
            #self.ball.velocity_y *= -1

        #bounce off left and right
        #if (self.ball.x < 0) or (self.ball.right > self.width):
            #self.ball.velocity_x *= -1
    
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