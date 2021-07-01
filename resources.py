import os, sys
import json
import time
import re
import math

import requests

#import logging
#logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_dir, 'config', 'credentials.txt')
cache_dir = os.path.join(script_dir, 'image_cache')

with open(credentials_path) as credentials_file:
    lines = credentials_file.read().splitlines()
    username = lines[0].strip()
    api_key = lines[1].strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

image_file_extensions = r'\.(?:jpg|png|gif)'
is_cached_image_name = re.compile(r'(\d+)({})'.format(image_file_extensions))
class ResourceManager:
    def __init__(self):
        self.cache_table = {}
        for root, dirs, files in os.walk(cache_dir):
            for file_name in files:
                m = is_cached_image_name.match(file_name)
                if m is None:
                    continue
                name, extension = m.groups()
                self.cache_table[int(name)] = file_name
    def get_url(self, url, **kwargs):
        time.sleep(1) # Rate limiting lol
        return requests.get(url, **kwargs, headers=HEADERS_BASE)

    def cache_image(self, post):
        image_id = post['id']; url = post['file']['url']
        _, extension = os.path.splitext(url)
        cached_filename = str(image_id) + extension
        cached_path = os.path.join(cache_dir, cached_filename)
        with open(cached_path, 'wb') as cache_file:
            data = self.get_url(url).content
            cache_file.write(data)
        self.cache_table[image_id] = cached_filename

    def get_image(self, post):
        image_id = post['id']
        if not image_id in self.cache_table:
            self.cache_image(post)
        cached_path = os.path.join(cache_dir, self.cache_table[image_id])
        return open(cached_path, 'rb').read()

    def get_indexed_search(self, search_string, limit=None):
        return IndexedSearch(search_string, limit)
    def get_search(self, search_string, limit=None):
        return LazySearch(search_string, limit)

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
        self.cache = resource_manager.get_url(URL_BASE + 'posts.json', params=params).json()
    def posts(self):
        while self.posts_to_serve > 0:
            self.load_next()
            yield from self.cache['posts']
            self.posts_to_serve -= len(self.cache['posts'])
            if len(self.cache['posts']) != self.cache_limit: # Search has ended already
                break
    def __iter__(self):
        return iter(self.posts())

class IndexedSearch:
    def __init__(self, search_string, limit=None):
        self.search_iterator = iter(LazySearch(search_string, limit))
        self.cache = []
    def __contains__(self, index):
        try:
            self.get(index)
            return True
        except ValueError:
            return False
    def __getitem__(self, index):
        try:
            while index >= len(self.cache):
                self.cache.append(next(self.search_iterator))
        except StopIteration:
            raise ValueError('Search ended at {} posts. Index {} out of range.'.format(len(self.cache), index))
        return self.cache[index]

def run():
    search = LazySearch('duo', 19)
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        print(file_url)

if __name__ == '__main__':
    run()

