import os, sys
import json
import time
import re
import math

import requests

#import logging
#logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(script_dir, 'config')
credentials_path = os.path.join(config_dir, 'credentials.txt')
cache_dir = os.path.join(script_dir, 'image_cache')

with open(credentials_path) as credentials_file:
    lines = credentials_file.read().splitlines()
    username = lines[0].strip()
    api_key = lines[1].strip()

URL_BASE = 'https://e621.net/'
HEADERS_BASE = {'user-agent':'ConMan/1.2 (e621 tagging interface by MatrixMash)'}
PARAMETERS_BASE = {}

dummy_project = {
    'key_bindings' : {
        'Return':'say_enter',
            'n':'say_n',
            'N':'say_N',
            'Control_L':'say_left_control',
            'h':'say_dummy_message',
            'l':'do_dummy_load',
            'Escape': 'do_quit',
    },
    'search':'asdfasdfasdfew',
    'default_text' : 'No image here. Press h to print test message.',
}

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

digits = r'\d+'
size = '(?:file|preview|sample)'
image_name = '(' + digits + '-' + size + ')'
image_extension = '(' + r'\.' + '(?:jpg|png|gif|webm)' + ')'
is_cached_image_name = re.compile(image_name + image_extension)
class ResourceManager:
    def __init__(self):
        self.cache_table = {}
        for root, dirs, files in os.walk(cache_dir):
            for file_name in files:
                m = is_cached_image_name.match(file_name)
                if m is None:
                    continue
                name, extension = m.groups()
                self.cache_table[name] = file_name
        self.projects = {'dummy':dummy_project}
        for root, dirs, files in os.walk(config_dir):
            for file_name in files:
                name, extension = os.path.splitext(file_name)
                if extension == '.json':
                    path = os.path.join(root, file_name)
                    with open(path) as project_file:
                        project = json.load(project_file)
                    self.projects[name] = project
        self.session = requests.Session()
        self.session.auth = (username, api_key)
    def get_url(self, url, headers={}, params={}, **kwargs):
        time.sleep(1) # Rate limiting lol
        params = {**PARAMETERS_BASE, **params}
        headers = {**HEADERS_BASE, **headers}
        result = self.session.get(url, headers=headers, params=params, **kwargs)
        if result.status_code == 401:
            print('Authentication failure on url', url)
            print('Is your username and api key in config/credentials.txt on separate lines? Do you need to regenerate your api key?')
        return result

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
    
    def get_project(self, name): return self.projects[name]

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

