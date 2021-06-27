import os, sys
import json
import time

import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
personal_path = os.path.join(script_dir, 'personal.txt')

username = 'matrixmash10'
with open(personal_path) as personal_file:
    api_key = personal_file.read().splitlines()[0].strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

class ResourceManager:
    def get_url(self, url, **kwargs):
        time.sleep(1) # Rate limiting lol
        return requests.get(url, **kwargs, headers=HEADERS_BASE)

resource_manager = ResourceManager()

class LazySearch:
    def __init__(self, search_string):
        self.search_string = search_string
        self.cache_limit = 6
        self.before_id = None
        self.cache = []
        self.load()
    def load(self):
        params = {'limit':self.cache_limit, 'tags':self.search_string}
        if self.before_id is not None:
            params['page'] = 'b' + str(self.before_id)
        self.cache = resource_manager.get_url(URL_BASE + 'posts.json', params=params).json()
    def posts(self):
        for _ in range(3):
        #while True:
            yield from self.cache['posts']
            if len(self.cache['posts']) != self.cache_limit:
                break
            self.before_id = self.cache['posts'][-1]['id']
            self.load()

def run():
    search = LazySearch('duo')
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        print(file_url)

if __name__ == '__main__':
    run()

