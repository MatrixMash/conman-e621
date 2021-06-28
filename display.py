from io import BytesIO
import tkinter

from PIL import Image, ImageTk

from resources import resource_manager
#from config import shared

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
#        self['width'] = 200
#        self['height'] = 200
        self.create_widgets()
#        self.set_shortcuts()
    def create_widgets(self):
        data = resource_manager.get_image(dummy_post)
        image = Image.open(BytesIO(data))
        photo_image = ImageTk.PhotoImage(image)
        l = tkinter.Label(self, image=photo_image)
        l.image = photo_image   # So tk doesn't forget the image on us
        l.pack()
#    def set_shortcuts(self):
#        self.master.bind('n', shared.say_hi)
        #self.minsize((500, 500))

#def show_data(data):
#    stream = BytesIO(data)
#    image = Image.open(stream)
#    image.show()

#def show_post(post):
#    data = resource_manager.get_image(post)
#    show_data(data)

def run():
    root = tkinter.Tk()
    Conman(root)
    root.mainloop()
#    for post in resource_manager.get_search('rating:s apple', 5):
#        show_post(post)
#        input('press enter to continue')
    
if __name__ == '__main__':
    run()

