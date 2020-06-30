import requests
from PIL import Image
from choose_headers_randomly import choose_headers_randomly

directory_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxell/'

def download_image(url):
    image_path = directory_path

    # Generate the correct image type according to the given URL
    if url.endswith('.jpg'):
        image_path += 'temp.jpg'
    elif url.endswith('.png'):
        image_path += 'temp.png'
    elif url.endswith('.webp'):
        image_path += 'temp.webp'
    else:
        image_path += 'temp.jpg'

    # Save the image
    response = requests.get(url, stream=True, headers=choose_headers_randomly())
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)

    # Convert the image if its type is webp.
    if image_path.endswith('.webp'):
        img = Image.open(image_path).convert('RGB')
        image_path = image_path.replace('.webp', '.jpg')
        img.save(image_path, 'jpeg')

    return image_path
