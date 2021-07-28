import itertools
import tkinter

from display import PostDisplay
from resources import resource_manager

CONTROL = 0b100

class EditReviewer(tkinter.Frame):
    def __init__(self, master, posts):
        super().__init__(master)
        self.master = master
        self.post_display = PostDisplay(self)
        self.post_display.set_project(resource_manager.current_project)
        self.bind('<KeyPress>', self.do_keypress)
        master.title('Review your edits: Press delete to delete. Escape when done.')
        
        self.posts = posts
        
        self.current_index = 0
        self.go_to(0)
        
        self.pack()
        self.focus_set()
    
    def quit(self): self.master.destroy()
    
    def next(self, offset=1): self.go_to(self.current_index + offset)
    def previous(self, offset=1): self.go_to(self.current_index - offset)
    def has_next(self, offset=1): return self.current_index + offset in self
    
    def __contains__(self, index): return index in self.search
    def go_to(self, index):
        try:
            if index < 0:
                raise IndexError
            self.set_post(self.posts[index])
            self.current_index = index
        except IndexError:
            if index < 0:
                self.current_index = -1
            else:
                self.current_index = len(self.posts)
            self.set_post(None)
        
    def set_post(self, post): self.post_display.set_post(post)
    def do_keypress(self, key_event):
        symbol = key_event.keysym.lower()
        if symbol == 'left':
            self.previous()
        elif symbol == 'right':
            self.next()
        elif symbol == 'escape' or (CONTROL & key_event.state and symbol == 'w'):
            self.quit()
        elif symbol == 'delete':
            if self.current_index >= 0 and self.current_index < len(self.posts):
                del self.posts[self.current_index]
                if self.current_index == len(self.posts):     # If we delete the last image, step back.
                    self.current_index -= 1
                self.go_to(self.current_index)
        elif symbol == 'return':
            resource_manager.queue_patches(self.posts)
            self.master.destroy()
        elif symbol == 'space':
            self.toggle_tag('set:conman_test')
        elif symbol == 'p':
            for post in self.posts:
                id_ = post['id']
                c = post['changes']
                print('{}: {}'.format(id_, c))
    #    else:
    #        print(symbol)


import reviewer_test
edits = reviewer_test.changes

def run():
    from editor import PostEditor
    root = tkinter.Tk()
    editor = PostEditor(root, 'test_sample_3')
    #root.mainloop()
    #edits = editor.edits
    
    #root = tkinter.Tk()
    #reviewer = EditReviewer(root, edits)
    #root.mainloop()
    
    
    #from projects import test_sample_3
    #resource_manager.set_project('test_sample_3')       # Need auth to do post changes, baka
    #post_and_changes = list(edits.values())[3]
    
    #print(post_and_changes['changes'])
    #post_and_changes['changes']['duo'] = False
    #post_and_changes['changes']['solo'] = True
    #post_and_changes['changes']['group'] = False
    #import sys
    #sys.exit()
    #p = 
    #print(p)
    #print(p.content)
    
if __name__ == '__main__':
    run()

