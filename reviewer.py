import itertools
import tkinter

from display import PostDisplay, PostEditor

CONTROL = 0b100

class EditReviewer:
    def __init__(self, master, change_dict):
        self.post_display = PostDisplay(master)
        self.master = master
        master.bind('<KeyPress>', self.do_keypress)
        master.title('Review your edits: Press delete to delete. Escape when done.')
        
        self.changes = list(change_dict.values())
        
        self.current_index = 0
        self.go_to(0)
    
    def quit(self): self.master.destroy()
    
    def next(self, offset=1): self.go_to(self.current_index + offset)
    def previous(self, offset=1): self.go_to(self.current_index - offset)
    def has_next(self, offset=1): return self.current_index + offset in self
    
    def __contains__(self, index): return index in self.search
    def go_to(self, index):
        try:
            if index < 0:
                raise IndexError
            post_changes = self.changes[index]
            self.set_post(post_changes['post'])
            print('Consider changes:', post_changes['changes'])
            self.current_index = index
        except IndexError:
            if index < 0:
                self.current_index = -1
            else:
                self.current_index = len(self.changes)
            self.set_post(None)
        print(self.current_index)
        
    def set_post(self, post): self.post_display.set_post(post)
    def do_keypress(self, key_event):
        symbol = key_event.keysym.lower()
        if symbol == "left":
            self.previous()
        elif symbol == "right":
            self.next()
        elif symbol == "escape" or (CONTROL & key_event.state and symbol == 'w'):
            self.quit()
        elif symbol == 'delete':
            if self.current_index >= 0 and self.current_index < len(self.changes):
                del self.changes[self.current_index]
                if self.current_index == len(self.changes):     # If we delete the last image, step back.
                    self.current_index -= 1
                self.go_to(self.current_index)
        elif symbol == 'space':
            self.toggle_tag('set:conman_test')
        elif symbol == 'p':
            import pprint
            pprint.pprint([c['post']['id'] for c in self.changes])
    #    else:
    #        print(symbol)


import reviewer_test
changes = reviewer_test.changes

def run():
    #root = tkinter.Tk()
    #editor = PostEditor(root, 'test_sample_3')
    #root.mainloop()
    #changes = editor.changes
    root = tkinter.Tk()
    reviewer = EditReviewer(root, changes)
    root.mainloop()
    
if __name__ == '__main__':
    run()

