from io import BytesIO
import tkinter

from PIL import Image, ImageTk

from resources import resource_manager
from config import shortcut_callbacks

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

class Conman(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('conman: an e621 tag editor')
        self.pack()
        self.create_widgets()
        self.current_post = None
        
        self.user_shortcuts = {
            'Return':'say_enter',
            'n':'say_n',
            'N':'say_N',
            'Control_L':'say_left_control',
            'h':'say_help',
            'l':'do_load',
        }
        self.master.bind('<KeyPress>', self.do_keypress)
        
    def set_post(self, post):
        self.current_post = post
        image = Image.open(BytesIO(resource_manager.get_image(post)))
        photo_image = ImageTk.PhotoImage(image)
        self.main_label['image'] = photo_image
        self.main_label.image = photo_image # So tk doesn't forget the image on us
        self.main_label.pack()
    def create_widgets(self):
        self.main_label = tkinter.Label(self, text='No image here. Press h to print help.')
        self.main_label.pack()
    
    def do_keypress(self, key_event):
        if key_event.keysym in self.user_shortcuts:
            function_name = self.user_shortcuts[key_event.keysym]
            f = getattr(shortcut_callbacks, function_name)
            f(self, self.current_post, key_event)

def run():
    root = tkinter.Tk()
    Conman(root)
    root.mainloop()
#    for post in resource_manager.get_search('rating:s apple', 5):
#        show_post(post)
#        input('press enter to continue')
    
if __name__ == '__main__':
    run()

