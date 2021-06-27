from PIL import Image
from io import BytesIO

from resources import resource_manager

def run():
    bytes = resource_manager.get_image(511799)
    stream = BytesIO(bytes)
    image = Image.open(stream)
    image.show()
    
#   from resources import LazySearch
#    search = LazySearch('duo')
#    
#    for p in search.posts():
#        file_metadata = p['file']
#        file_url = file_metadata['url']
#        print(file_url)

if __name__ == '__main__':
    run()

