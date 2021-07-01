from io import BytesIO
import tkinter

from PIL import Image, ImageTk

from resources import resource_manager
from config import shortcut_callbacks

class PostDisplay(tkinter.Frame):
    def __init__(self, master, default_text='Nobody here but us chickens.'):
        super().__init__(master)
        self.master = master
        master.title('conman: an e621 tag editor')
        self.pack()
        self.default_text = default_text
        self.create_widgets()
        self.current_post = None
    def set_post(self, post):
        if post is None:
            self.main_label['image'] = ''
            return
        self.current_post = post
        image = Image.open(BytesIO(resource_manager.get_image(post)))
        photo_image = ImageTk.PhotoImage(image)
        self.main_label['image'] = photo_image
        self.main_label.image = photo_image # So tk doesn't forget the image on us
        self.main_label.pack()
    def set_default_text(self, t): self.main_label['text'] = t
    def create_widgets(self):
        self.main_label = tkinter.Label(self, text=self.default_text)
        self.main_label.pack()

class PostEditor:
    def __init__(self, master):
        self.post_display = PostDisplay(master)
        self.master = master
        self.master.bind('<KeyPress>', self.do_keypress)
        
        self.current_index = None
        self.search = None
    def set_project(self, project):
        self.project = project
        self.set_search(project['search'])
        self.post_display.set_default_text(project['default_text'])
    def set_search(self, search_string):
        self.search = resource_manager.get_indexed_search(search_string)
        self.go_to(0)
    
    def quit(self): self.master.destroy()
    
    def next(self, offset=1): self.go_to(self.current_index + offset)
    def previous(self, offset=1): self.go_to(self.current_index - offset)
    def has_next(self, offset=1): return self.current_index + offset in self
    
    def __contains__(self, index): return index in self.search
    def go_to(self, index):
        try:
            post = self.search[index]
            self.set_post(post)
            self.current_index = index
        except ValueError:
            if index < 0:
                self.current_index = -1
            else:
                self.current_index = len(self.search.cache)
            self.set_post(None)
        
    def set_post(self, post):
        self.post_display.set_post(post)
    def do_keypress(self, key_event):
        bindings = self.project['key_bindings']
        if key_event.keysym in bindings:
            function_name = bindings[key_event.keysym]
            f = getattr(shortcut_callbacks, function_name)
            f(self, self.post_display.current_post, key_event)

def run():
    root = tkinter.Tk()
    editor = PostEditor(root)
    editor.set_project(resource_manager.get_project('sample'))
    root.mainloop()
    
if __name__ == '__main__':
    run()

