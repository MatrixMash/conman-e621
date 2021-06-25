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

def run():
    r = requests.get(URL_BASE + 'posts.json?limit=1', headers=HEADERS_BASE)
    jso = r.json()
    json.dump(jso, sys.stdout)

if __name__ == '__main__':
    run()

