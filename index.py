import imagehash
import pandas as pd
from PIL import Image
from download_image import download_image

data_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxell/bukalapak_search_maxell_colored_test.csv'

data = pd.read_csv(data_path)

for i in range(len(data)):
    image_url = data.iloc[i]['Thumbnail Url']
    image_path = download_image(image_url)
    image = Image.open(image_path)
    ahash = imagehash.average_hash(image)
    dhash = imagehash.dhash(image)
    phash = imagehash.phash(image)
    whash = imagehash.whash(image)
    data.at[i, 'ahash'] = ahash
    data.at[i, 'dhash'] = dhash
    data.at[i, 'phash'] = phash
    data.at[i, 'whash'] = whash
    print('Finished No. %d' % i)

data.to_csv(data_path)