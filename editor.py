import itertools

from resources import resource_manager
from display import PostDisplay

def tag_lists(post):
    tag_list_names = ["general", "species", "character", "copyright", "artist", "invalid", "lore", "meta"]
    return [post['tags'][name] for name in tag_list_names] + [post['locked_tags']]
def is_locked(post, tag): return tag in post['locked_tags']
def tags_of_post(post):
    return itertools.chain(tag_lists(post))
def post_has_tag(post, tag): return tag in tags_of_post(post)

class PostEditor:
    def __init__(self, master, project_name):
        self.post_display = PostDisplay(master)
        self.master = master
        self.master.bind('<KeyPress>', self.do_keypress)
        
        self.changes = None
        
        self.project = None
        self.current_index = None
        self.search = None
        self.set_project(project_name)
    
    def get_current_post(self): return self.post_display.current_post
    
    # This function is kind of an antipattern, cuz I don't know how to name it.
    # It looks for the matching data structure, and if it doesn't exist,
    # initializes it to return later. It's very stateful, I didn't plan for it,
    # and I don't know if I should replace it or what.
    def load_current_change_dict(self):
        p = self.get_current_post() 
        id_ = p['id']
        if not id_ in self.changes:
            self.changes[id_] = {'post':p, 'changes':{}}
        return self.changes[id_]['changes']
    
    def add_tag(self, tag): self.load_current_change_dict()[tag] = True
    def remove_tag(self, tag): self.load_current_change_dict()[tag] = False
    def toggle_tag(self, tag):
        changes = self.load_current_change_dict()
        if tag in changes:
            changes[tag] = not changes[tag]
        else:
            changes[tag] = not post_has_tag(self.get_current_post(), tag)
            
    def set_project(self, project_name):
        self.changes = {}
        project = resource_manager.set_project(project_name)
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
    print('Project options:', '\n'.join(resource_manager.projects.keys()))
    project_name = 'test_sample_3'#input('Name of project? ')
    print()
    root = tkinter.Tk()
    editor = PostEditor(root, project_name)
    root.mainloop()
    print('Control flow is restored to me.')
    root = tkinter.Tk()
    root.title('Hi there!')
    root.mainloop()
    
if __name__ == '__main__':
    run()

