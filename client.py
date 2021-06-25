import os, sys
import json
import requests
import time

import logging
logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.dirname(os.path.abspath(__file__))
personal_path = os.path.join(script_dir, 'personal.txt')

with open(personal_path) as personal_file:
    api_key = next(iter(personal_file)).strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

def get(url, **kwargs):
    time.sleep(1)
    return requests.get(url, **kwargs, headers=HEADERS_BASE)

class Search:
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
        self.cache = get(URL_BASE + 'posts.json', params=params).json()
    def posts(self):
        for _ in range(3):
            #r = get(URL_BASE + 'posts.json?limit=10')
            #jso = r.json()
            #jso = json.load(open('toy.txt'))
            yield from self.cache['posts'] #jso['posts']
            if len(self.cache['posts']) != self.cache_limit:
                break
            self.before_id = self.cache['posts'][-1]['id']
            self.load()
    

def run():
    #json.dump(jso, open('toy.txt', 'w'))
    search = Search('duo')
    
    for p in search.posts():
        file_metadata = p['file']
        file_url = file_metadata['url']
        file_width = file_metadata['width']
        file_height = file_metadata['height']
        print(file_url)
        #print(p['sample']['url'])
        #print(p['preview']['url'])
    
    
    #from pprint import pprint
    #pprint(jso)
    

if __name__ == '__main__':
    run()

