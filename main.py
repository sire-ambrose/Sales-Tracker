from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from  kivy.uix.filechooser import FileChooserListView
import shutil, os
from datetime import date
import pandas as pd
import os
Save_folder= os.getcwd()
try:
    os.mkdir(Save_folder)
except :
    pass

today = date.today()
heading= 'Date,  Item,  Quanty,  Cost Price,  Selling Price,  Net Income'+'\n'

file_name = today.strftime("%B %Y")+'.csv'
try :
    present= open(Save_folder+'//'+file_name, "x")
    present=open(Save_folder+'//'+file_name, "w")
    present.write(heading)
    present.close()
except:
    pass

class disp(BoxLayout):
    def __init__(self,widget, **kwargs):
        super(disp, self).__init__(**kwargs)
        self.orientation='vertical'
        self.file=widget
        #inside_file=open(self.file, 'r')
        inside_file=pd.read_csv(self.file)
        self.widget=Label(text=str(inside_file))
        self.add_widget(self.widget)
        self.GL=GridLayout(cols=1, size_hint_y=None, size=(1,75))
        self.cancel=Button(text='Cancel')
        self.GL.add_widget(self.cancel)
        self.add_widget(self.GL)

class disps(BoxLayout):
    def __init__(self,widget, **kwargs):
        super(disps, self).__init__(**kwargs)
        self.orientation='vertical'
        self.file=widget

        if self.file[-1]=='g' or 'f':
            self.widget=Image(source=widget)
            self.add_widget(self.widget)
        elif self.file[-1]=='4':
            self.widget=Video(source=widget)
            #lbl=Label(text=str(self.widget.loaded))
            self.add_widget(self.widget)
        self.GL=GridLayout(cols=2, size_hint_y=None, size=(1,75))
        self.save=Button(text='Delete', on_press=self.delete)
        self.cancel=Button(text='Cancel')
        self.GL.add_widget(self.save)
        self.GL.add_widget(self.cancel)
        self.add_widget(self.GL)
    def delete(self, instance):
        os.remove(self.file)

class saver(FileChooserListView):
    def __init__(self, **kwargs):
        super(saver, self).__init__(**kwargs)
        self.show_hidden=True
        self.rootpath=Save_folder
        self.pop=Popup()
        
    def on_submit(self, selection, touch):
        for f in selection:
            con=disp(f)
            con.cancel.on_press=self.exit
            self.pop=Popup(title='Status',auto_dismiss=False, content=con)
            self.pop.open()
    def exit(self):
        self.pop.dismiss()

def slice(word):
    num=[]
    j=0
    for i in word:
        if i == ',':
            num.append(j)
        j +=1
    sliced=[]
    latest= 0
    for i in num:
        sliced.append(int(word[latest:i]))
        latest= i+1
    sliced.append(int(word[num[-1]+1:]))
    return sliced


class saved(BoxLayout):
    def __init__(self, **kwargs):
        super(saved, self).__init__(**kwargs)
        self.orientation='vertical'
        self.grid=GridLayout()
        self.grid.cols=2
        self.grid.add_widget(Label(text='Item Sold : '))
        self.item= TextInput()
        self.grid.add_widget(self.item)

        self.grid.add_widget(Label(text='Quantity : '))
        self.quantity= TextInput()
        self.grid.add_widget(self.quantity)

        self.grid.add_widget(Label(text='Cost Price : '))
        self.cost_price= TextInput()
        self.grid.add_widget(self.cost_price)

        self.grid.add_widget(Label(text='Selling Price : \ne.g 400,250,500'))
        self.selling_price= TextInput()
        self.grid.add_widget(self.selling_price)

        self.grid.add_widget(Label())
        self.add_widget(self.grid)
        self.submit= Button(text='Submit', on_press=self.keep, size_hint=(0.2,0.2), pos_hint={'x':0.4})
        self.add_widget(self.submit)
        self.rootpath=Save_folder
        
    def keep(self, instance):
        present= open(file_name, 'a')
        if ',' in self.selling_price.text:
            present.write(today.strftime("%d")+',  '+self.item.text+',  '+self.quantity.text+',  '+str(sum(slice(self.cost_price.text)))+',  '+str(sum(slice(self.selling_price.text)))+',  '+str(sum(slice(self.selling_price.text))-sum(slice(self.cost_price.text)))+'\n')
        else:
            present.write(today.strftime("%d")+',  '+self.item.text+',  '+self.quantity.text+',  '+self.cost_price.text+',  '+self.selling_price.text+',  '+str(int(self.selling_price.text)-int(self.cost_price.text))+'\n')
        present.close()
        self.item.text, self.quantity.text, self.cost_price.text, self.selling_price.text= '','','',''
    
    def exit(self):
        self.pop.dismiss()

class first_screen(BoxLayout):
    def __init__(self, **kwargs):
        super(first_screen, self).__init__(**kwargs)
        self.orientation='vertical'
        self.gl=GridLayout(cols=3, size_hint_y=None)
        self.btn_status=Button(text='History', on_press=self.status)
        self.gl.add_widget(self.btn_status)
        self.btn_saved=Button(text='Add New Transaction', on_press=self.saved)
        self.gl.add_widget(self.btn_saved)
        self.btn_abt=Button(text='About', on_press=self.abt)
        self.gl.add_widget(self.btn_abt)
        self.add_widget(self.gl)
        self.sta=saver()
        self.add_widget(self.sta)
        self.sav=saved()
    def status(self, instance):
        self.clear_widgets()
        self.add_widget(self.gl)
        self.add_widget(self.sta)
    def saved(self, instance):
        self.clear_widgets()
        self.add_widget(self.gl)
        self.add_widget(saved())
    def abt(self, instance):
        self.clear_widgets()
        self.add_widget(self.gl)
        self.add_widget(about())
class about(Label):
    def __init__(self, **kwargs):
        super(about, self).__init__(**kwargs)
        abt='           HOW TO USE\n\n1. Make sure WhatsApp is installed in phone memory\n\n2. View the status with WhatsApp Messenger\n\n3. Open Saver App\n\n4. Click WhatsApp Status button\n\n5. Double tap on a status to view and save\n\n\n\n          CONTACT DEVELOPER\n\nFacebook : Sire Ambrose\n\nEmail : ikpeleambroseobinna@gmail.com\n\nWhatsApp : +2348118499120 '
        self.text=abt
class Kivy(App):
    def build(self):
        self.icon='icon.png'
        return first_screen()
        
if __name__ =="__main__":
    Kivy().run()