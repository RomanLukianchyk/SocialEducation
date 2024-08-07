import io
from PIL import Image


def create_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'JPEG')
    file.name = 'test_image.jpg'
    file.seek(0)
    return file