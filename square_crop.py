def square_crop(image):
    width, height = image.size
    half_width, half_height = int(width/2), int(height/2)
    cropped_image = None
    if width > height:
        area = (half_width-half_height, 0, half_width+half_height, height)
        cropped_image = image.crop(area)
    else:
        area = (0, half_height-half_width, width, half_height+half_width)
        cropped_image = image.crop(area)
    return cropped_image
