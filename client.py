import os, sys
import json
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
personal_path = os.path.join(script_dir, 'personal.txt')

with open(personal_path) as personal_file:
    api_key = next(iter(personal_file)).strip()

URL_BASE = 'https://e621.net/'
USER_AGENT = "ConMan/1.2 (e621 tagging interface by MatrixMash)"
HEADERS_BASE = {'user-agent':USER_AGENT}

#class RequestsLimiter

def run():
    #r = requests.get(URL_BASE + 'posts.json?limit=10', headers=HEADERS_BASE)
    #jso = r.json()
    #json.dump(jso, open('toy.txt', 'w'))
    jso = json.load(open('toy.txt'))
    
    post_listing = jso
    posts = post_listing['posts']
    for p in posts:
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

