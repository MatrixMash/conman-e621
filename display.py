import tkinter

from io import BytesIO      # Turn in-memory bytes returned by resource_manager into stream expected by PIL
from PIL import Image, ImageTk, UnidentifiedImageError

from resources import resource_manager

class PostDisplay(tkinter.Frame):
    def __init__(self, master, default_text='Nobody here but us chickens.'):
        super().__init__(master)
        self.master = master
        master.title('conman: an e621 tag editor')
        self.pack()
        self.default_text = default_text
        self.create_widgets()
        self.current_post = None
        
        self.max_size = (2000, 1000)
        self.view = 'file_shrink'
    
    def set_post(self, post):
        if post is None:
            self.main_label['image'] = ''
            return
        self.current_post = post
        if self.view in ['file', 'preview', 'sample']:
            image_bytes = resource_manager.get_image_data(post, self.view)
        else:
            image_bytes = resource_manager.get_image_data(post)
        try:
            image = Image.open(BytesIO(image_bytes))
        except UnidentifiedImageError as uie:
            self.main_label['image'] = ''
            print(uie)
            print('from url', post['file']['url'])
            return
        if self.view == 'file_shrink':
            image.thumbnail(self.max_size)
        photo_image = ImageTk.PhotoImage(image)
        self.main_label['image'] = photo_image
        self.main_label.image = photo_image # So tk doesn't forget the image on us
        self.main_label.pack()
    def set_default_text(self, t): self.main_label['text'] = t
    def create_widgets(self):
        self.main_label = tkinter.Label(self, text=self.default_text)
        self.main_label.pack()

def run():
#    print('Project options:', '\n'.join(resource_manager.projects.keys()))
#    project_name = 'test_sample_3'#input('Name of project? ')
#    print()
#    root = tkinter.Tk()
#    editor = PostEditor(root, project_name)
#    root.mainloop()
#    print('Control flow is restored to me.')
#    root = tkinter.Tk()
#    root.title('Hi there!')
#    root.mainloop()
    print('Demo for PostDisplay not implemented.')
    
if __name__ == '__main__':
    run()

