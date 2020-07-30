import imagehash
import pandas as pd
import os
from PIL import Image
from collections import defaultdict
from download_image import download_image
from square_crop import square_crop

listings_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego/listings.csv'
image_hashes_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego/image_hashes2.csv'
lego_images_directory_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego_images/'
comparison_directory_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego/comparison2/'

listings = pd.read_csv(listings_path)
images = pd.read_csv(image_hashes_path)

def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

def find_closest_images(hash, hash_type='phash'):
    h = str(hash)
    distance_to_image_name = defaultdict(list)
    distance = float('inf')
    for i in range(len(images)):
        current_distance = hamming_distance(h, images.iloc[i][hash_type])
        image_name = images.iloc[i]['image_name']
        distance_to_image_name[current_distance].append(image_name)
        if current_distance < distance:
            distance = current_distance
    image_names = distance_to_image_name[distance]
    return (image_names, distance)

def v_merge(image_paths, new_image_path, height=500):
    total_width = 0
    for image_path in image_paths:
        image = Image.open(image_path)
        width, h = image.size
        total_width += int((width / h) * height)
    
    new_image = Image.new('RGB', (total_width, height))
    start_width = 0
    for image_path in image_paths:
        image = Image.open(image_path)
        width, h = image.size
        width = int((width / h) * height)
        image = image.resize((width, height))
        new_image.paste(image, (start_width, 0, start_width + width, height))
        start_width += width
    new_image.save(new_image_path)

# for i in range(64):
#     os.makedirs('/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego/comparison2/%d/' % (i))

for i in range(len(listings)):
    try:
        image_path = download_image(listings.iloc[i]['Thumbnail'])
        index = listings.iloc[i]['Item ID']
        image = Image.open(image_path)
        image = square_crop(image)
        phash = imagehash.phash(image)
        closest_image_names, minimum_distance = find_closest_images(phash)
        for closest_image_name in closest_image_names:
            v_merge([lego_images_directory_path + closest_image_name, image_path], comparison_directory_path + '%d/%s-%s' % (minimum_distance, str(index), closest_image_name))
        print(minimum_distance)
        print('Finished No. %d' % i)
    except Exception:
        continue