#MUSIC PLAYER RANDOM ORDERED SORT
import os, sys
#os.environ["KIVY_VIDEO"] = "ffpyplayer"
from random import *

songDict = {}
songVal = {}
                
#how to use generator mp3gen()
i = 0
for mp3file in ["1","9","7k","r","j","i","7","g","a","2",]:
    songDict[i] = mp3file
    songVal[str(mp3file)] = 0
    i += 1
    if i > 7:
        break

    
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleKVIDsDataViewBehavior 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import *
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import traceback

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        #set self.data:
        self.data = [{'textinfo.text': x, 'selected': False} for x in [songDict[y] for y in songDict]]
        print("self.data item?", self.data[0], len(self.data))

    def scroll_to_index(self, index):
        box = self.children[0]
        pos_index = (box.default_size[1] + box.spacing) * index
        scroll = self.convert_distance_to_scroll(
            0, pos_index - (self.height * 0.5))[1]
        if scroll > 1.0:
            scroll = 1.0
        elif scroll < 0.0:
            scroll = 0.0
        self.scroll_y = 1.0 - scroll
    
    def NextSong(self, *args):
        rvRef = App.get_running_app().root.get_screen('selectscreen').ids["songlistid"].ids["recycle_grid1"]
        randPickInt = randint(0,len(rvRef.data)-1)
        
        for d in rvRef.data:
            #if we found the song, change to selected
            if d['textinfo.text'] == songDict[randPickInt]:
                d['selected'] = True
                dictElement = d
        #video doesn't work on mp3, so use soundloader
        target = os.path.normpath(rvRef.data[randPickInt]['textinfo.text'])
        
        #change the label to the current song
        App.get_running_app().root.get_screen('selectscreen').ids["songlistid"].ids["songtitle"].text = target
        
        targettextOG = rvRef.data[randPickInt]['textinfo.text']
        #PLAN: apply_selection always triggers when reycycleview refreshes, so set a global var of the selected guy. within the widget, if the name is the same as the selected guy, make yourself selected
        global curSelectedSong
        curSelectedSong = rvRef.data[randPickInt]['textinfo.text']
        
        counter = 0
        for d in rvRef.data:
            #remove all previously selected
            if d['selected']:
                d['selected'] = False
            #if we found the song, change to selected
            if d['textinfo.text'] == targettextOG:
                print("VERSING", d['textinfo.text'], targettextOG, d['textinfo.text'] == targettextOG)
                d['selected'] = True
                print("so has d updated?", d)
                rvRef.data[counter] = d
                print("so has rvRef.data updated?", rvRef.data[counter])
            counter += 1
        print("WHAT IS RV DATA?", rvRef.data)
        App.get_running_app().root.get_screen('selectscreen').ids["songlistid"].ids["recycle_grid1"].scroll_to_index(randPickInt)
        rvRef.refresh_from_data()

#this is from the advanced default example from https://kivy.org/doc/stable-1.10.1/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleView
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                             RecycleBoxLayout):

    ''' Adds selection and focus behaviour to the view. '''
    def __init__(self, **kwargs):
        #https://stackoverflow.com/questions/50362476/attributeerror-mainrouter-object-has-no-attribute-disabled-count
        super(SelectableRecycleBoxLayout, self).__init__(**kwargs)

def WeightedChoice():
    pass
    
class SongLinkButton(RecycleKVIDsDataViewBehavior,BoxLayout,Label):
    
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    #how to set id correctly through python: https://stackoverflow.com/questions/50099151/python-how-to-set-id-of-button
    #when you add this guy add an image widget and in the box layout add the yt title 
    def __init__(self, **kwargs):
        #https://stackoverflow.com/questions/50362476/attributeerror-mainrouter-object-has-no-attribute-disabled-count
        super(SongLinkButton, self).__init__(**kwargs)        

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SongLinkButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SongLinkButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global curSelectedSong
        
        try:
            if curSelectedSong == rv.data[index]["textinfo.text"]:
                self.selected == True
        except:
            pass
        
        global soundObj
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        #and the current screen is songselect
        #for screen names refer to <Manachan> in VideoDanceStar.kv, capitalization matters
        if is_selected and App.get_running_app().root.current == 'selectscreen':
            #video doesn't work on mp3, so use soundloader
            target = os.path.normpath(rv.data[index]['textinfo.text'])
            
            Clock.schedule_interval(App.get_running_app().root.get_screen('selectscreen').ids["songlistid"].ids["recycle_grid1"].NextSong, 1)
    
            #change the label to the current song
            App.get_running_app().root.get_screen('selectscreen').ids["songlistid"].ids["songtitle"].text = target
            #print("selection changed to {0}".format(rv.data[index]))
        else:
            pass
            #print("selection removed for {0}".format(rv.data[index]))
        
        
#need to add reference to dropdownid because validatelink fails since weakref does not exist (aka dropdown doesn't exist when ur in gradescreen)
#https://stackoverflow.com/questions/46060693/referenceerror-weakly-referenced-object-no-longer-exists-kivy-dropdown
class Manachan(ScreenManager):
    pass

class SongList(GridLayout):
    pass

class SelectionScreen(Screen):
        pass
    
class MyApp(App):

    def build(self):
        #return Label(text='Hello world')
        self.load_kv('MPROSRVbug.kv')
        self.title = "Music Player Random Ordered Sort by Pengindoramu"
        return Manachan()

if __name__ == '__main__':
    MyApp().run()
