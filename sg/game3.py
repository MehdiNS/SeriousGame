from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import *
import time

#import dataBase
import gameMenu


#,category,size,x,center_y,pos_base,img_source,sound_src
class Object(Widget):
    """Class to manage drag and drop
   
    """   
    
    
    #Open a connection for each Object
    #local_db = dataBase.DataBase()  
    
    def on_touch_move(self, touch):
        """Function called when the object is moved
        
        :param touch: finger on the screen     
        
        """       
        #If the current object is the one grab
        if touch.grab_current is self:
            #Update of position
            self.parent.touched_object = self
            self.center_x = touch.x
            self.center_y = touch.y          
    
    def on_touch_down(self, touch):
        """Function called when the object is double clicked
        
        :param touch: finger on the screen     
        
        """
        #Get the object touched by the user    
        if self.collide_point(*touch.pos): 
            if touch.is_double_tap:    
                #Play a sound if the user do a double tap           
                sound = SoundLoader.load(self.text)
                sound.play()
                return;
            #Set opacity to display the current selected object
            self.opacity = 0.2
            #The object is grabbed
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        """Function called when the object is dropped after a move
        
        :param touch: finger on the screen     
        
        """
        #If this is the correct object
        if touch.grab_current is self:    
            #The Object is ungrabbed
            touch.ungrab(self)  
            #The initial opacity is set                
            self.opacity = 1
            #Check if the object has been dropped on the category House
            if (self.collide_customed(self.parent.category_house)):
                print("House touched")
                #If there is no other category in collision
                if(not self.collide_customed(self.parent.category_vehicle)):
                    #Check if the object has been dropped on the good category
                    if (self.category=="house"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        val = self.parent.score
                        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
                        #Object is removed
                        self.parent.remove_widget(self)
                        #SAving in dataBase
                        self.local_db.insert_into_Table("Game2", ["time Date", "score int"], [time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime()), str(val)])
                        self.local_db.print_table("game2")
                        #self.local_db.JSonToCSV(self.local_db.SQliteToJSOn("Game2"))
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base

            #Check if the object has been dropped on the category Vehicle
            elif(self.collide_customed(self.parent.category_vehicle)):
                print("Vehicle touched")
                #If there is no other category in collision                
                if((not self.collide_customed(self.parent.category_house))and(not self.collide_customed(self.parent.category_character))):
                    #Check if the object has been dropped on the good category
                    if (self.category=="vehicle"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        #Object is removed
                        self.parent.remove_widget(self)
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base

            #Check if the object has been dropped on the category Character
            elif(self.collide_customed(self.parent.category_character)):
                print("Character touched")
                #If there is no other category in collision
                if (not self.collide_customed(self.parent.category_vehicle)):
                    #Check if the object has been dropped on the good category
                    if (self.category=="character"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        #Object is removed
                        self.parent.remove_widget(self)
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base   
            
            #The object is moved back to the initial position
            self.pos = self.pos_base
    
    def collide_customed(self, widget):
        '''
        Fonction which implement custom collision between 2 widgets
        This function draw a square with center (self.center_x, self.center_y) and size = ( widget.size - self.size)/2 (1 if res <0)
        :param Widget: the widget to test collision with self
        :type widget = Widget, we will use center_x,center_y and size
        
        :return Return true is self's custom zone is in collision with widget
    '''
        #Calcul of radius
        size = ((widget.size_hint_x - self.size_hint_x)/4)
        # if r <=0, the test will be done with a point
        if (size<=0):
            size = 1
        #Creation of the zone
        zone = Widget()
        zone.center_x = widget.center_x
        zone.center_y = widget.center_y
        zone.size_hint_x = size
        zone.size_hint_y = size
        
        #Test the collision
        return(self.collide_widget(zone))

class Object2(Widget):
    """Class to manage drag and drop
   
    """   
    
    
    def __init__(self, cat):
        self.category = cat
    #Open a connection for each Object
    #local_db = dataBase.DataBase()  
    
    def on_touch_move(self, touch):
        """Function called when the object is moved
        
        :param touch: finger on the screen     
        
        """       
        #If the current object is the one grab
        if touch.grab_current is self:
            #Update of position
            self.parent.touched_object = self
            self.center_x = touch.x
            self.center_y = touch.y          
    
    def on_touch_down(self, touch):
        """Function called when the object is double clicked
        
        :param touch: finger on the screen     
        
        """
        #Get the object touched by the user    
        if self.collide_point(*touch.pos): 
            if touch.is_double_tap:    
                #Play a sound if the user do a double tap           
                sound = SoundLoader.load(self.text)
                sound.play()
                return;
            #Set opacity to display the current selected object
            self.opacity = 0.2
            #The object is grabbed
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        """Function called when the object is dropped after a move
        
        :param touch: finger on the screen     
        
        """
        #If this is the correct object
        if touch.grab_current is self:    
            #The Object is ungrabbed
            touch.ungrab(self)  
            #The initial opacity is set                
            self.opacity = 1
            #Check if the object has been dropped on the category House
            if (self.collide_customed(self.parent.category_house)):
                print("House touched")
                #If there is no other category in collision
                if(not self.collide_customed(self.parent.category_vehicle)):
                    #Check if the object has been dropped on the good category
                    if (self.category=="house"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        val = self.parent.score
                        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
                        #Object is removed
                        self.parent.remove_widget(self)
                        #SAving in dataBase
                        self.local_db.insert_into_Table("Game2", ["time Date", "score int"], [time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime()), str(val)])
                        self.local_db.print_table("game2")
                        #self.local_db.JSonToCSV(self.local_db.SQliteToJSOn("Game2"))
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base

            #Check if the object has been dropped on the category Vehicle
            elif(self.collide_customed(self.parent.category_vehicle)):
                print("Vehicle touched")
                #If there is no other category in collision                
                if((not self.collide_customed(self.parent.category_house))and(not self.collide_customed(self.parent.category_character))):
                    #Check if the object has been dropped on the good category
                    if (self.category=="vehicle"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        #Object is removed
                        self.parent.remove_widget(self)
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base

            #Check if the object has been dropped on the category Character
            elif(self.collide_customed(self.parent.category_character)):
                print("Character touched")
                #If there is no other category in collision
                if (not self.collide_customed(self.parent.category_vehicle)):
                    #Check if the object has been dropped on the good category
                    if (self.category=="character"):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav');
                        sound.play();
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        #Object is removed
                        self.parent.remove_widget(self)
                        return True
                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base   
            
            #The object is moved back to the initial position
            self.pos = self.pos_base
    
    def collide_customed(self, widget):
        '''
        Fonction which implement custom collision between 2 widgets
        This function draw a square with center (self.center_x, self.center_y) and size = ( widget.size - self.size)/2 (1 if res <0)
        :param Widget: the widget to test collision with self
        :type widget = Widget, we will use center_x,center_y and size
        
        :return Return true is self's custom zone is in collision with widget
    '''
        #Calcul of radius
        size = ((widget.size_hint_x - self.size_hint_x)/4)
        # if r <=0, the test will be done with a point
        if (size<=0):
            size = 1
        #Creation of the zone
        zone = Widget()
        zone.center_x = widget.center_x
        zone.center_y = widget.center_y
        zone.size_hint_x = size
        zone.size_hint_y = size
        
        #Test the collision
        return(self.collide_widget(zone))
        
class Category(Widget):
    '''       
    This is a category
'''
    def __init__(self,src,**kwargs):
        Widget.__init__(self, **kwargs)
        print(src)
        #self.size = (Window.size[0]*1/8,Window.size[1]*1/6)
        self.canvas.add(Rectangle(pos = self.pos, size = self.size, source = src))
                         
class CategoryHouse(Widget):
    '''       
    This is the category which regroup all house objects
'''
    
class CategoryVehicle(Widget):
    '''       
    This is the category which regroup all vehicle objects
'''

class CategoryCharacter(Widget):
    '''       
    This is the category which regroup all character objects
'''
class Game3(Widget):
    
    #Create object list
    ObjectList = []
    
    #Create cat list
    CategoryList =[]
    
    #When init the Game
    def __init__(self, **kwargs):
        print()
        print()
        Widget.__init__(self, **kwargs)
        # Opening file reading mode
        loaded_file = open("./game3.txt", "r")     
        #read the first line
        line = loaded_file.readline()
        
        #Loading all the file in 2 different lists
        while (line!="endfile"):
            if (line[0]!='#'):
                tab_res = line.split('&')
                if (tab_res[0]=="Object"):
                    #Create Object with src and category 
                    obj = Object2(tab_res[1])
                    self.ObjectList.append(obj)
                if (tab_res[0]=="Category"):
                    cat = Category(tab_res[1], size=(Window.size[0]*1/8,Window.size[1]*1/6))
                    self.CategoryList.append(cat)
            #read the next line
            line = loaded_file.readline()
         
        for obj in self.CategoryList:
                self.add_widget(obj) 
                break  

    #Score display
    score = NumericProperty(0)
    remaining = NumericProperty(18)
    clock = NumericProperty(0)
    
    #Define the three categories
    category_house = ObjectProperty(None)
    category_vehicle = ObjectProperty(None)
    category_character = ObjectProperty(None)
    
        
    def increment_clock(self, dt):
        if (self.remaining!=0):
            self.clock += 1;
        else:
            return False;
    
    def update(self, dt):
        if (self.remaining==0):
            self.on_winning();
            return False;
        
    def on_winning(self):
        layout = BoxLayout(orientation='vertical')
        def callback(instance):
            if (instance.text=='Rejouer'):
                return Game3App().run();
            else:
                return gameMenu.GameMenuApp().run();
            print('The button <%s> is being pressed' % instance.text)
        btn1 = Button(text='Rejouer')
        btn1.bind(on_press=callback)
        btn2 = Button(text='Changer de jeu')
        btn2.bind(on_press=callback)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        popup = Popup(title='Felicitations !!! Ton score : ' + str(self.score),
                      title_size = '20sp' ,
                      content=layout,
                      size_hint=(None, None),
                      size=(400, 400),
                      auto_dismiss=False)
        popup.open()
        print "popup ouvert"
        sound = SoundLoader.load('../sound/finished.wav')
        sound.play()

    
class Game3App(App):
    
    def build(self):
        #Set window's size
        print(Config.get('graphics', 'width'))
        print(Config.get('graphics', 'height'))
        #Start the game
        game = Game3()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.increment_clock, 1.0)
        return game

if __name__ == '__main__':
    Game3App().run()