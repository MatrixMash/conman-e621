import os, sys
import json
import time

import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
personal_path = os.path.join(script_dir, 'personal.txt')
cache_dir = os.path.join(script_dir, 'image_cache')

username = 'matrixmash10'
with open(personal_path) as personal_file:
    api_key = personal_file.read().splitlines()[0].strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

class ResourceManager:
    def __init__(self):
        self.cache_table = {511799:'511799.png'} # Downloaded from https://e621.net/posts/511799
    def get_image(self, post):
        image_id = post['id']
        if image_id in self.cache_table:
            cached_path = os.path.join(cache_dir, self.cache_table[image_id])
            return open(cached_path, 'rb').read()
        return self.get_url(post['file']['url']).content
    def get_url(self, url, **kwargs):
        time.sleep(1) # Rate limiting lol
        return requests.get(url, **kwargs, headers=HEADERS_BASE)
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

def run():
    search = LazySearch('duo', 19)
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        print(file_url)

if __name__ == '__main__':
    run()

