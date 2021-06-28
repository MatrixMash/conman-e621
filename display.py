from PIL import Image
from io import BytesIO

from resources import resource_manager

def show_data(data):
    stream = BytesIO(data)
    image = Image.open(stream)
    image.show()

def show_post(post):
    data = resource_manager.get_image(post)
    show_data(data)

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}
def run():
    for post in resource_manager.get_search('rating:s apple', 5):
        show_post(post)
        input('press enter to continue')
    
if __name__ == '__main__':
    run()

