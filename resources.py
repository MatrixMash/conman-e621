import os, sys
import json
import time
import re

import requests

import logging
logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.dirname(os.path.abspath(__file__))
personal_path = os.path.join(script_dir, 'personal.txt')
cache_dir = os.path.join(script_dir, 'image_cache')

username = 'matrixmash10'
with open(personal_path) as personal_file:
    api_key = personal_file.read().splitlines()[0].strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

file_extensions = r'\.(?:jpg|png|gif)'
is_cached_image_name = re.compile(r'(\d+)({})'.format(file_extensions))
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

    def get_search(self, search_string, limit=None):
        return LazySearch(search_string, limit)

resource_manager = ResourceManager()

class LazySearch:
    def __init__(self, search_string, limit=None):
        self.search_string = search_string
        self.cache_limit = 6
        self.total_limit = limit
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
        posts_to_serve = self.total_limit
        while posts_to_serve is None or posts_to_serve > 0:
            self.load_next()
            yield from self.cache['posts']
            posts_to_serve -= len(self.cache['posts'])
            if len(self.cache['posts']) != self.cache_limit: # No more posts on e621
                break
            if posts_to_serve < self.cache_limit and posts_to_serve > 0:
                self.cache_limit = posts_to_serve
    def __iter__(self):
        return iter(self.posts())

def run():
    search = LazySearch('duo', 19)
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        print(file_url)

if __name__ == '__main__':
    run()

