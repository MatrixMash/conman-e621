import itertools
import tkinter

from io import BytesIO      # Turn in-memory bytes returned by resource_manager into stream expected by PIL
from PIL import Image, ImageTk, UnidentifiedImageError

from resources import resource_manager

def tag_lists(post):
    tag_list_names = ["general", "species", "character", "copyright", "artist", "invalid", "lore", "meta"]
    return [post['tags'][name] for name in tag_list_names] + [post['locked_tags']]
def tags_of_post(post):
    return itertools.chain.from_iterable(tag_lists(post))
def post_has_tag(post, tag):
    return tag in tags_of_post(post)

class PostDisplay(tkinter.Frame):
    def __init__(self, master, default_text='Nobody here but us chickens.'):
        super().__init__(master)
        self.master = master
        self.pack()
        self.default_text = default_text
        self.create_widgets()
        
        self.current_post = None
        self.focus_tags = []
        
        self.max_size = (2000, 1000)
        self.view = 'file_shrink'
    
    def draw_image(self):
        post = self.current_post
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
    
    def draw_tags(self):
        post = self.current_post
        self.tags_text['state'] = 'normal'
        self.tags_text.delete('1.0', 'end')
        if post is not None:
            keys_and_names = (
                ('invalid', 'Invalid'),
                ('artist', 'Artists'),
                ('copyright', 'Copyrights'),
                ('character', 'Characters'),
                ('species', 'Species'),
                ('general', 'General'),
                ('meta', 'Meta'),
                ('lore', 'Lore'),
            )
            for key, display_name in keys_and_names:
                tags = post['tags'][key]
                if tags:
                    self.tags_text.insert('end', '{}\n'.format(display_name))
                    for tag in tags:
                        self.tags_text.insert('end', '   {}\n'.format(tag))
        self.tags_text['state'] = 'disable'
    
    def draw_focus_tags(self):
        post = self.current_post
        self.focus_tags_text['state'] = 'normal'
        self.focus_tags_text.delete('1.0', 'end')
        
        if post is not None:
            changes = post.get('changes', {})
            unique_tags = {*self.focus_tags, *changes.keys()}
            for t in unique_tags:
                if t in changes:
                    prepend = '+' if changes[t] else '-'
                    text_tag = 'present' if changes[t] else 'absent'
                else:
                    prepend = '  '
                    text_tag = 'present' if post_has_tag(post, t) else 'absent'
                t = prepend + t + '\n'
                self.focus_tags_text.insert('insert', t, text_tag)
                    
        self.focus_tags_text['state'] = 'disable'
    
    def set_project(self, project):
        self.focus_tags = getattr(project, 'focus_tags', [])
    def set_post(self, post):
        self.current_post = post
        self.draw_image()
        self.draw_tags()
        self.draw_focus_tags()
    def set_default_text(self, t): self.main_label['text'] = t
    
    def create_widgets(self):
        self.focus_tags_text = tkinter.Text(self, width=30, state='disable', font='DejaVu')
        self.focus_tags_text.pack(side='right')
        self.focus_tags_text.tag_configure('present', background='#ddddff')
        self.focus_tags_text.tag_configure('absent', foreground='#222222')
        
        self.main_label = tkinter.Label(self, text=self.default_text)
        self.main_label.pack(side='right')
        self.tags_text = tkinter.Text(self, width=30, state='disable', font='DejaVu')
        self.tags_text.pack(side='right', fill='both')

def run():
    print('Demo for PostDisplay not implemented.')
    
if __name__ == '__main__':
    run()

