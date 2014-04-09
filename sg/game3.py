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
import random
import time

#import dataBase
import gameMenu


class Object2(Widget):
    """Class to manage drag and drop
   
    """   
    src=""
    name=""
    category=""
    pos_base=[0,0]
    def __init__(self,src,nme,cat,**kwargs):
        Widget.__init__(self, **kwargs)
        self.name=nme
        self.category=cat
        self.rect = Rectangle(pos = self.pos, size = self.size, source = src)
        self.canvas.add(self.rect)
        #self.bind(x=self.updateX(),y=self.updateY())
        self.src=src
        #Open a connection for each Object
        #local_db = dataBase.DataBase()  
    def __update__(self):
        print("COUCOU")
    def updateCatSize(self):
        self.size=(Window.size[0]*1/4,Window.size[1]*2/3)            
    
    def set_x(self,x):
        self.x=x;
        
    def set_pos_base(self,pos_base):
        self.pos_base=pos_base;
    
    def set_center_y(self,center_y):
        self.center_y=center_y;
    
    def get_name(self):
        return(self.name)
    def UpdatePos(self, pos):
        self.center_x = pos.x
        self.center_y = pos.y
        self.rect.pos = [pos.x-self.rect.size[0]/2,pos.y-self.rect.size[1]/2]     
        
    def Back_to_Base(self, pos_base):
        self.x=pos_base[0]
        self.y=pos_base[1]      
        self.rect.pos = [pos_base[0],pos_base[1]] 
        
         
    def on_touch_move(self, touch):
        """Function called when the object is moved
        
        :param touch: finger on the screen     
        
        """       
        #If the current object is the one grab
        if touch.grab_current is self:
            #Update of position
            self.UpdatePos(touch)
    
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
            print(self.name)
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
            for ob in self.parent.FormDisplayed:
                if (self.collide_customed(ob)):
                    print("check cat: "+self.category+"="+ob.category+"?")
                    if (self.category==ob.category):
                        print("Congratulations !")
                        sound = SoundLoader.load('../sound/right.wav')
                        sound.play()
                        #Update of score
                        self.parent.score += 5
                        self.parent.remaining = self.parent.remaining - 1
                        #val = self.parent.score
                        #SAving in dataBase
                        #self.local_db.insert_into_Table("Game2", ["time Date", "score int"], [time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime()), str(val)])
                        #self.local_db.print_table("game2")   
                        #Store the Widget representing the picture already found by the child
                        self.parent.already_learned.append(self)
                        #Start a new round
                        self.parent.new_round()

                    else:
                        print("This is the wrong category")
                        sound = SoundLoader.load('../sound/wrong.wav');
                        sound.play();
                        #Update of score
                        self.parent.score -= 1
                        #The object is moved back to the initial position
                        self.pos = self.pos_base
            
            #The object is moved back to the initial position
            #Update of position
            self.Back_to_Base(self.pos_base)
    
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
       
        
class ObjectForm(Widget):
    '''       
    This class represents empty shapes
'''
    def __init__(self,src,nme,cat,**kwargs):
        Widget.__init__(self, **kwargs)
        self.name=nme
        self.category=cat
        self.rect = Rectangle(pos = self.pos, size = self.size, source = src)
        self.canvas.add(self.rect)
        #self.bind(x=self.updateX(),y=self.updateY())
        self.src=src
        #Open a connection for each Object
        #local_db = dataBase.DataBase()  
    
    def __update__(self):
        print("COUCOU")
    def updateCatSize(self):
        self.size=(Window.size[0]*1/4,Window.size[1]*2/3)
    def updateX(self):
        pass
    def updateY(self):
        pass                
    
    def set_x(self,x):
        self.x=x;
        
    def set_pos_base(self,pos_base):
        self.pos_base=pos_base;
    
    def set_center_y(self,center_y):
        self.center_y=center_y;
    
    def get_name(self):
        return(self.name)
        
class Game3(Widget):
    #Save window's size to use later
    windowSave = Window.size;
    
    #Create object list
    ObjectList = []
    
    #Create cat list
    ObjectFormList =[]
    
    #List to store Form displayed and Object displayed
    FormDisplayed = []
    ObjDisplayed = []
    
    #Create a list to store pictures already found by the children
    already_learned = []
    
    #When init the Game
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        # Opening file reading mode
        loaded_file = open("./game3.txt", "r")     
        #read the first line
        line = loaded_file.readline()
        
        #Loading all the file in 2 different lists
        while (line!="endfile"):
            if (line[0]!='#'):
                tab_res = line.split('&')
                tab_save = tab_res[1].split('/')
                tab_name = tab_save[4].split('.')
                nameImg = tab_name[0]
                if (tab_res[0]=="Object"):                   
                    #Create Object with src and category 
                    obj = Object2(tab_res[1],nameImg,tab_res[2],size=(self.windowSave[0]*1/4,self.windowSave[1]*1/3),text=tab_res[3])               
                    self.ObjectList.append(obj)
                if (tab_res[0]=="ObjectForm"):
                    cat =tab_res[2]
                    form = ObjectForm(tab_res[1],nameImg,cat[:-1], size=(self.windowSave[0]*1/4,self.windowSave[1]*1/3))
                    self.ObjectFormList.append(form)
            #read the next line
            line = loaded_file.readline()
        self.new_round()
                  
    #Score display
    score = NumericProperty(0)
    remaining = NumericProperty(18)
    clock = NumericProperty(0)
    
    def new_round(self):  
        #Store ObjectList and ObjectFormList size
        size_list_obj = len(self.ObjectList)
        size_list_obj_form = len(self.ObjectFormList)
        #Create 2 list to store random values 
        mem_rand_obj = []
        mem_rand_form = []
        #Reset list of objects and forms displayed
        for o in self.ObjDisplayed:
            self.remove_widget(o)
        for f in self.FormDisplayed:
            self.remove_widget(f)
        self.FormDisplayed = []
        self.ObjDisplayed = []
        #2 list to store objects before update
        saveFormDisplayed = []
        saveObjDisplayed = []
        #Display 3 items on the right
        for i in [1,3,5]:
            ##############"PART FOR THE OBJ######################
            #Choose an integer randomly, but different for the previous one
            rand_obj = random.randint(0, size_list_obj-1)            
            checked = 0
            while (checked != 1):
                rand_obj = random.randint(0, size_list_obj-1)
                checked=1
                for j in mem_rand_obj:                    
                    if (j == rand_obj):
                        checked = 0
                    
            mem_rand_obj.append(rand_obj)
                
            #Select the corresponding object   
            obj = self.ObjectList[rand_obj]
            print(obj.get_name())
            #Set object
            obj.set_center_y(self.windowSave[1]*i/6)
            obj.set_x(self.windowSave[0]*1/8)
            ##############"PART FOR THE FORM######################
            #Choose an integer randomly, but different for the previous one
            rand_form = random.randint(0, size_list_obj_form-1)            
            checked = 0
            while (checked != 1):
                rand_form = random.randint(0, size_list_obj_form-1)
                checked=1
                for j in mem_rand_obj:                    
                    if (j == rand_form):
                        checked = 0  
                for j in mem_rand_form:                    
                    if (j == rand_form):
                        checked = 0     
            mem_rand_form.append(rand_form)       
                 
            objForm = self.ObjectFormList[rand_form]
            
            #Set Object
            objForm.set_center_y(self.windowSave[1]*i/6)
            objForm.set_x(self.windowSave[0]*5/8)            
                        
            #Update lists
            saveFormDisplayed.append(objForm)
            saveObjDisplayed.append(obj)
        
        rand_identique = random.randint(0, 2)
        rand_pos = random.randint(0, 2)
        
        for obj in saveObjDisplayed:
            #Both Widgets are added
            obj2 = Object2(obj.src,obj.name,obj.category,size=obj.size,center_y=obj.center_y-50,x=obj.x)
            obj2.set_pos_base([obj.x,obj.y])
            self.add_widget(obj2)
            self.ObjDisplayed.append(obj2)
        indice=0    
        for objForm in saveFormDisplayed:
            if (indice==rand_pos):
                for obj_inter in self.ObjectFormList:
                    print(len(obj_inter.category))
                    print(len(self.ObjDisplayed[rand_identique].category))
                    print(obj_inter.category)
                    print(self.ObjDisplayed[rand_identique].category)
                    if (obj_inter.category == (self.ObjDisplayed[rand_identique].category)):
                        objForm=obj_inter   
                        objForm.x = self.windowSave[0]*5/8
                        objForm.center_y = self.windowSave[1]*(indice*2+1)/6
                        break
            print("cat ="+objForm.category)
            objForm2 = ObjectForm(objForm.src,objForm.name,objForm.category,size=objForm.size,center_y=objForm.center_y-50,x=objForm.x)
            objForm2.set_pos_base([objForm.x,objForm.y])
            self.add_widget(objForm2)  
            self.FormDisplayed.append(objForm2) 
            #update list
            self.FormDisplayed[indice]=objForm2
            indice = indice +1
            
    def increment_clock(self, dt):
        if (self.remaining!=0):
            self.clock += 1;
        else:
            return False;
    
    def updateWidget(self):
        for obj in self.ObjectList:
            obj.updateCatSize();
            break  
        
    
    def update(self, dt):
        if (Window.size != self.windowSave):
            self.windowSave = Window.size;
            self.updateWidget();
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