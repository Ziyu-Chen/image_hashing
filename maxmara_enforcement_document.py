from collections import defaultdict
import os
import pandas as pd 

enforcement_document_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara/enforcement_document.csv'
comparison_directory_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara/comparison/'
listings_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara/taobao_store_seller/bulk_upload_data.xlsx'
new_bulk_upload_data_path = '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara/taobao_store_seller/new_bulk_upload_data.xlsx'
image_urls_paths = [
    '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara_image_urls/weekendmaxmara.csv',
    '/Users/Ziyu/OneDrive - Clarivate Analytics/Desktop/maxmara_image_urls/weekendmaxmara2.csv'
]
language = 'CN'



listings = pd.read_excel(listings_path)
selector = [False for _ in range(len(listings))]

enforcement_document_dict = defaultdict(list)

image_urls = pd.concat([pd.read_csv(image_urls_path) for image_urls_path in image_urls_paths])
for _, _, file_names in os.walk(comparison_directory_path):
    for file_name in file_names:
        first_hyphen_position = file_name.index('-')
        listing_index = file_name[:first_hyphen_position]
        image_name = file_name[first_hyphen_position+1:]

        listing_url = None
        image_url = None
        image_source = None

        for i in range(len(listings)):
            if listing_index == str(listings.iloc[i]['Item ID (Required|Non-editable)']):
                selector[i] = True
                listing_url = listings.iloc[i]['URL (Required)']
                break
        
        for i in range(len(image_urls)):
            url = image_urls.iloc[i]['url']
            source = image_urls.iloc[i]['source']
            if image_name in url:
                image_url = url
                image_source = source
                break
        
        if language == 'EN':
            enforcement_document_dict['listing_url'].append(listing_url)
            enforcement_document_dict['image_url'].append(image_url)
            enforcement_document_dict['image_source'].append(image_source)
        
        elif language == 'CN':
            enforcement_document_dict['商品链接'].append(listing_url)
            enforcement_document_dict['图片链接'].append(image_url)
            enforcement_document_dict['图片来源'].append(image_source)
        
pd.DataFrame(enforcement_document_dict).to_csv(enforcement_document_path, encoding='utf-8')

listings[selector].to_excel(new_bulk_upload_data_path)