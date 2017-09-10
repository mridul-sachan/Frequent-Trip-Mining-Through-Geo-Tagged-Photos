import sqlite3
import math

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
    image_data_var = ImageData(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])
    return image_data_var
'''
Function to calculate Time Gap between two consecutive images.
'''

def calculateTimeGap (time_from , time_to):
    t_gap = time_from - time_to
    if (t_gap) > 0:  # If t2-t1 is zero, then math.log function is throwing an error, so to avoid that we are taking only non-zero values.
        timegap = math.log10(t_gap)
    else:
        timegap = 0
    return timegap
'''
Function to calculate Tag Gap.
'''
def calculateTagGap (tag_list1 , tag_list2):
    set1 = set(tag_list1)
    set2 = set(tag_list2)
    set3 = set1 & set2
    if set1 == set() and set2 == set():
        tag_gap = 0.5
    elif set3 == set():
        tag_gap = 0
    else:
        tag_gap = len(set3) * 1.0 / len(set1)
    return tag_gap

'''
Function to calculate Distance Gap between two consecutive images.
'''
def calculateDistanceGap(source_latitude, source_longitude, dest_latitude, dest_longitude):

    del_delta = source_latitude - dest_latitude

    # Computing the difference between longitudes of two images.
    # del_lambda = longitude difference
    del_lambda = source_longitude - dest_longitude

    # arcsin_arg is calculating the argument value of arcsin() as given in equation 4 under Photo Collection Segmentation.
    arcsin_arg = math.sqrt(
        math.sin(del_delta / 2) ** 2 + (math.cos(source_latitude) * math.cos(dest_latitude) * math.sin(del_lambda / 2) ** 2))

    phi_rad = 2 * math.asin(arcsin_arg)  # Equation 4 -- page 136

    if phi_rad == 0:  # if phi_rad will be zero then log function will throw an error so changing to non-zero value.
        phi_rad = 0.1

    # Calculating the value of distance gaps :
    # 6370Km is D i.e. radius of the Earth.
    return math.log10(6370 * phi_rad)  # Equation 3 second part


event_set = []
image_info_db = []

# Making connection with database.
conn = sqlite3.connect('Flickr.db')
print "Opened database successfully"

#Connecting cursor/filehandler with database.
cursor = conn.execute("SELECT *  from ProcessedData_out order by datetaken DESC")
for row in cursor:
    # Taking the values from Database row by row and appending to a list 'image_info_db'.
    image_info_db.append(mapper(row))

Gn_list = []  # List to store the values of Gn for each image.

for i in image_info_db:
    print i.date_taken



k=1.5
d= 5
alpha = 0.2
beta = 0.1


#Reading values from the above made list, i is index and j is the value.
for i, j in enumerate(image_info_db):
    if i != len(image_info_db) - 1: #Here we are not reading data of last row
        if i < len(image_info_db) - 1:
            next_row = image_info_db[i + 1]

        '''
        Calculating the value of time gap for 2 consecutive images.
        '''

        tgap = calculateTimeGap(j.date_taken, next_row.date_taken)

        '''
        Now we will calculate the distance gap after calculating time gap.
        '''

        #print next_row.latitude


        distGap = calculateDistanceGap(float(j.latitude),float(j.longitude),float(next_row.latitude),float(next_row.longitude))

        # Calling calculateTagGap function through object tagGap.
        tagGap = calculateTagGap(j.tags.split(" "), next_row.tags.split(" "))

        # Calculating value of gn(considered as a change of events)
        j.gn = (1 - alpha - beta) * tgap + alpha * distGap + beta * tagGap

        Gn_list.append(j.gn)


event = []

###################
for index, value in enumerate(image_info_db):
    sum_gn_d = 0
    for i in range(-d, d):
        if ((index + i) >= 0) and (index + i) < len(image_info_db):
            sum_gn_d = sum_gn_d + image_info_db[index + i].gn

    avg_gn_d = (1.0/(2*d + 1)) * sum_gn_d
    if image_info_db[index].gn > k + avg_gn_d:
        if len(event) == 0:
            event.append(value)
            continue
        event_set.append(event)
        event = list()
        #event.append(value)
    else:
        event.append(value)

###################


for p in event_set:
    for x in p:
        print str(x.date_taken),
        print str(x.owner),
        print str(x.title),
        print str(x.date_taken)
    print "%s, %s " %(x.latitude , x.longitude)
    print "."
    print "\n"
    Event_latitude = x.latitude
    Event_longitude = x.longitude




