import imagehash
import pandas as pd
import os
from PIL import Image
from collections import defaultdict

directory_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego_images/'
data_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/lego/image_hashes.csv'

data_dict = defaultdict(list)

for image_name in os.listdir(directory_path):
    image_path = directory_path + image_name
    image = Image.open(image_path)
    ahash = imagehash.average_hash(image)
    dhash = imagehash.dhash(image)
    phash = imagehash.phash(image)
    whash = imagehash.whash(image)
    data_dict['image_name'].append(image_name)
    data_dict['ahash'].append(ahash)
    data_dict['dhash'].append(dhash)
    data_dict['phash'].append(phash)
    data_dict['whash'].append(whash)
    print('Finished No. %s' % image_name)

data = pd.DataFrame(data_dict)
data.to_csv(data_path)