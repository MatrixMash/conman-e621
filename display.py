from PIL import Image
from io import BytesIO

from resources import resource_manager

def show_data(data):
    stream = BytesIO(data)
    image = Image.open(stream)
    image.show()

def run():
    dummy_post = {'id':511799,
     'file':
        {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
    }
    data = resource_manager.get_image(dummy_post)
    show_data(data)
    #post_stream = resource_manager.get_search('rating:s')
    
    #for 
    
#   from resources import LazySearch
#    search = LazySearch('duo')
#    
#    for p in search.posts():
#        file_metadata = p['file']
#        file_url = file_metadata['url']
#        print(file_url)

if __name__ == '__main__':
    run()

