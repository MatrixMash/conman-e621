import os, sys
import time
import re, math
import importlib

import requests

#import logging
#logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.dirname(os.path.abspath(__file__))
projects_dir = os.path.join(script_dir, 'projects')
cache_dir = os.path.join(script_dir, 'image_cache')

URL_BASE = 'https://e621.net/'
HEADERS_BASE = {'user-agent':'ConMan/1.2 (e621 tagging interface by MatrixMash)'}
PARAMETERS_BASE = {}

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

digits = r'\d+'
size = '(?:file|preview|sample)'
image_name = '(' + digits + '-' + size + ')'
image_extension = '(' + r'\.' + '(?:jpg|png|gif|webm|swf)' + ')'
is_cached_image_name = re.compile(image_name + image_extension)
class ResourceManager: # Singleton, get instance via resources.resource_manager
    def __init__(self):
        self.cache_table = {}
        for root, dirs, files in os.walk(cache_dir):
            for file_name in files:
                m = is_cached_image_name.match(file_name)
                if m is None:
                    continue
                name, extension = m.groups()
                self.cache_table[name] = file_name
        self.projects = {}
        for project_file_name in os.listdir(projects_dir):
            name, extension = os.path.splitext(project_file_name)
            if extension != '.py':
                continue
            self.projects[name] = importlib.import_module('projects.{}'.format(name))
        self.session = requests.Session()
    def get_url(self, url, headers={}, params={}, **kwargs):
        time.sleep(1) # Rate limiting lol
        params = {**PARAMETERS_BASE, **params}
        headers = {**HEADERS_BASE, **headers}
        result = self.session.get(url, headers=headers, params=params, **kwargs)
        if result.status_code == 401:
            print('Authentication failure on GET url', url)
            print('  Is your username really {}?'.format(self.session.auth[0]))
            print('  Are your username and API key assigned to auth in the project?')
            print('  Did you regenerate your API key recently?')
        return result
    
    def patch_url(self, url, data=None, headers={}, params={}, **kwargs):
        #time.sleep(1) # Rate limiting lol
        params = {**PARAMETERS_BASE, **params}
        headers = {**HEADERS_BASE, **headers}
        result = self.session.patch(url, data=data, headers=headers, **kwargs)
        if result.status_code == 401:
            print('Authentication failure on PATCH url', url)
            print('  Is your username really {}?'.format(self.session.auth[0]))
            print('  Are your username and API key assigned to auth in the project?')
            print('  Did you regenerate your API key recently?')
        return result
    
    def set_project(self, name):
        self.current_project = self.projects[name]
        if hasattr(self.current_project, 'auth'):
            self.session.auth = self.current_project.auth
        else:
            print('This project has no auth field???')
        return self.current_project

    def cache_image(self, post, size='file'):
        image_id = post['id']; url = post[size]['url']
        _, extension = os.path.splitext(url)
        image_name = str(image_id) + '-' + size
        cached_filename = image_name + extension
        cached_path = os.path.join(cache_dir, cached_filename)
        if os.path.isfile(cached_path):
            print(cached_path)
            raise Exception('Redownloading a cached file. What have I done wrong now?')
        with open(cached_path, 'wb') as cache_file:
            data = self.get_url(url).content
            cache_file.write(data)
        self.cache_table[image_name] = cached_filename

    def get_image_data(self, post, size='file'):
        image_id = str(post['id']) + '-' + size
        if not image_id in self.cache_table:
            self.cache_image(post, size)
        cached_path = os.path.join(cache_dir, self.cache_table[image_id])
        return open(cached_path, 'rb').read()

    def get_indexed_search(self, search_string, limit=None):
        return IndexedSearch(search_string, limit)
    def get_search(self, search_string, limit=None):
        return LazySearch(search_string, limit)
    def do_patch(self, post_and_changes):
        diff = changes_to_string_diff(post_and_changes['changes'])
        id_ = post_and_changes['post']['id']
        print('performing patch', repr(diff), 'on post', id_)
        print('view', post_and_changes['post']['file']['url'])
        return self.patch_url(URL_BASE + 'posts/{}.json'.format(id_), json={'post':{'tag_string_diff':diff}})
        
    def add_patches(self, patch_list):
        for p in patch_list:
            self.do_patch(p)

def changes_to_string_diff(changes):
    return ' '.join(('' if do_add else '-') + tag for tag, do_add in changes.items())

resource_manager = ResourceManager()

class LazySearch:
    def __init__(self, search_string, limit=None):
        self.search_string = search_string
        self.cache_limit = 75   # Doesn't really matter
        self.posts_to_serve = limit if limit is not None else math.inf
        if limit is not None and limit < self.cache_limit:
            self.cache_limit = limit
        self.before_id = None
        self.cache = []
    def load_next(self):
        if len(self.cache) > 0:
            self.before_id = self.cache['posts'][-1]['id']
        params = {'limit':self.cache_limit, 'tags':self.search_string}
        if self.before_id is not None:
            params['page'] = 'b' + str(self.before_id)
        result = resource_manager.get_url(URL_BASE + 'posts.json', params=params)
        if result.status_code == 401:
            self.cache = []
            return
        try:
            self.cache = result.json()['posts']
        except KeyError as k:
            print('Search failure on {}.'.format(self.search_string))
            self.cache = []
    def posts(self):
        while self.posts_to_serve > 0:
            self.load_next()
            yield from self.cache
            self.posts_to_serve -= len(self.cache)
            if len(self.cache) != self.cache_limit: # Search has ended already
                break
            if self.posts_to_serve < self.cache_limit:  # Avoid yielding more posts than self.posts_to_serve
                self.cache_limit = self.posts_to_serve
    def __iter__(self):
        return iter(self.posts())

class IndexedSearch:
    def __init__(self, search_string, limit=None):
        self.search_iterator = iter(LazySearch(search_string, limit))
        self.cache = []
    def __contains__(self, index):
        if index < 0:
            return False
        try:
            self[index]
            return True
        except ValueError:
            return False
    def __getitem__(self, index):
        try:
            while index >= len(self.cache):
                self.cache.append(next(self.search_iterator))
        except StopIteration:
            raise ValueError('Search ended at {} posts. Index {} out of range.'.format(len(self.cache), index))
        if index < 0:
            raise ValueError('Index into search must be zero or more.')
        return self.cache[index]

def run():
    search = LazySearch('duo', 19)
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        print(file_url)

if __name__ == '__main__':
    run()

