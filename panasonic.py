import imagehash
import pandas as pd
import os
from PIL import Image
from collections import defaultdict
from download_image import download_image
from square_crop import square_crop

listings_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/panasonic/panasonic_all_colored.csv'
image_hashes_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/panasonic/panasonic_blue_colored.csv'
listings = pd.read_csv(listings_path)
images = pd.read_csv(image_hashes_path)

def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

def find_smallest_distance(max_pct_r, max_pct_g, max_pct_b, phash):
    smallest_distance = 1000000
    for i in range(len(images)):
        if abs(max_pct_r-images.iloc[i]['max_pct_r']) <= 10 and abs(max_pct_g-images.iloc[i]['max_pct_g']) <= 10 and abs(max_pct_b-images.iloc[i]['max_pct_b']) <= 10:
            distance = hamming_distance(phash, images.iloc[i]['phash'])
            if distance < smallest_distance:
                smallest_distance = distance
    return smallest_distance

for i in range(len(listings)):
    smallest_distance = find_smallest_distance(listings.iloc[i]['max_pct_r'], listings.iloc[i]['max_pct_g'], listings.iloc[i]['max_pct_b'], listings.iloc[i]['phash'])
    listings.at[i, 'smallest_distance'] = smallest_distance
    print(smallest_distance)
    print('Finished No. %d' % i)

listings = listings.sort_values(by=['smallest_distance'])

listings.to_csv('/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/panasonic/panasonic_all_colored.csv')