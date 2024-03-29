import itertools
import tkinter # have to make PostEditor a Frame so it can catch keypress events

from resources import resource_manager
from display import PostDisplay
# To avoid circular dependency, I import EditReviewer in the "go_to_review" function.
#from reviewer import EditReviewer

def tag_lists(post):
    tag_list_names = ["general", "species", "character", "copyright", "artist", "invalid", "lore", "meta"]
    return [post['tags'][name] for name in tag_list_names] + [post['locked_tags']]
def is_locked(post, tag): return tag in post['locked_tags']
def tags_of_post(post):
    return itertools.chain.from_iterable(tag_lists(post))
def post_has_tag(post, tag): return tag in tags_of_post(post)

class PostEditor(tkinter.Frame):
    def __init__(self, master, project_name):
        super().__init__(master)
        master.title('conman: an e621 tag editor')
        self.post_display = PostDisplay(self)
        self.master = master
        self.bind('<KeyPress>', self.do_keypress)
        
        self.project = None
        self.current_index = None
        self.search = None
        self.set_project(project_name)
        
        self.pack()
        self.focus_set()    # Request keypress events
    
    def title(self, text): self.master.title(text)
    def get_current_post(self): return self.post_display.current_post
    def get_posts_with_changes(self): return [p for p in self.search.cache if p.get('changes', False)]
    
    # This function is kind of an antipattern, cuz I don't know how to name it.
    # It looks for the matching data structure, and if it doesn't exist,
    # initializes it to return later. It's very stateful, I didn't plan for it,
    # and I don't know if I should replace it or what.
    def load_current_change_dict(self):
        p = self.get_current_post()
        if not 'changes' in p:
            p['changes'] = {}
        return p['changes']
    
    def post_has(self, tag): return post_has_tag(self.get_current_post(), tag)
    def add_tag(self, tag):
        d = self.load_current_change_dict()
        if not self.post_has(tag):  # I had to draw a truth table for this. Good luck! ;)
            d[tag] = True
        else:
            if tag in d:
                del d[tag]
        self.post_display.draw_focus_tags()
    def remove_tag(self, tag):
        d = self.load_current_change_dict()
        if self.post_has(tag):
            d[tag] = False
        else:
            if tag in d:
                del d[tag]
        self.post_display.draw_focus_tags()
    def toggle_tag(self, tag):
        d = self.load_current_change_dict()
        if tag in d:
            del d[tag]
        else:
            d[tag] = not self.post_has(tag)
        self.post_display.draw_focus_tags()
            
    def set_project(self, project_name):
        project = resource_manager.set_project(project_name)
        self.post_display.set_project(project)
        self.project = project
        if hasattr(project, 'search'):
            self.set_search(project.search)
        else:
            print('This project has no search field???')
        if hasattr(project, 'default_text'):
            self.post_display.set_default_text(project.default_text)
    def set_search(self, search_string):
        self.search = resource_manager.get_indexed_search(search_string)
        self.go_to(0)
    
    def quit(self): self.master.destroy()
    def go_to_review(self):
        self.destroy()
        from reviewer import EditReviewer   # Import now to avoid circular dependency
        for p in self.get_posts_with_changes():
            print(p['id'], p['changes'])
        reviewer = EditReviewer(self.master, self.get_posts_with_changes())
    
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
        if not self.project is None:
            self.project.on_key(self, key_event)

def run():
    import tkinter
    #print('Project options:', '\n'.join(resource_manager.projects.keys()))
    #project_name = input('Name of project? ')
    #print()
    project_name = 'test_sample_3'
    root = tkinter.Tk()
    editor = PostEditor(root, project_name)
    root.mainloop()
    
if __name__ == '__main__':
    run()

