from io import BytesIO
import tkinter

from PIL import Image, ImageTk

from resources import resource_manager
from config import shortcut_callbacks

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

class PostDisplay(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('conman: an e621 tag editor')
        self.pack()
        self.create_widgets()
        self.current_post = None
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

class PostEditor:
    def __init__(self, master):
        self.post_display = PostDisplay(master)
        self.master = master
        self.master.bind('<KeyPress>', self.do_keypress)
        
        self.user_shortcuts = {
             'Left': 'arrow_key',
             'Right': 'arrow_key',
             'Escape': 'do_quit',
         }
        '''{
            'Return':'say_enter',
            'n':'say_n',
            'N':'say_N',
            'Control_L':'say_left_control',
            'h':'say_help',
            'l':'do_load',
            'Escape': 'do_quit',
        }'''
        
        self.current_index = None
        self.search = None
    def set_search(self, search_string):
        self.search = resource_manager.get_indexed_search(search_string)
        self.current_index = 0
        self.go_to(0)
    
    def quit(self): self.master.destroy()
    
    def next(self, offset=1): self.go_to(self.current_index + offset)
    def previous(self, offset=1): self.go_to(self.current_index - offset)
    def has_next(self, offset=1): return self.current_index + offset in self
    
    def __contains__(self, index): return index in self.search
    def go_to(self, index):
        post = self.search[index]
        self.set_post(post)
        self.current_index = index
    def set_post(self, post):
        self.post_display.set_post(post)
    def do_keypress(self, key_event):
        if key_event.keysym in self.user_shortcuts:
            function_name = self.user_shortcuts[key_event.keysym]
            f = getattr(shortcut_callbacks, function_name)
            f(self, self.post_display.current_post, key_event)

def run():
    root = tkinter.Tk()
    editor = PostEditor(root)
    #editor.set_search('rating:s butterfly')
    editor.set_search('ears_up rating:s feral -text duo')
    root.mainloop()
    
if __name__ == '__main__':
    run()

