class ImageData(object):
    # Base class for all images to store the meta data of Images.
    def __init__(self,id, owner, title, date_taken, tags, latitude, longitude):
        self.id = id
        self.owner = owner
        self.title = title
        self.date_taken = date_taken
        self.tags = tags
        self.latitude = latitude
        self.longitude = longitude
        self.gn = 0

def mapper(tuple):

    image_data_var = ImageData(tuple[0],tuple[1],tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])

    return image_data_var
