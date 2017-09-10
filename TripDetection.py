import sqlite3
import csv
import math

from urllib2 import urlopen
import json

#from geopy.geocoders import Nominatim
#geolocator = Nominatim()


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

class TripsData(object):
    #Class for storing data of all Trips
    def __init__(self, trip_images_metadata):
        p = trip_images_metadata
        trip_city = getplace(p[len(p) - 1].latitude, p[len(p) - 1].longitude)
        self.trip_images_metadata = trip_images_metadata
        self.duration = (p[0].date_taken - p[len(p) - 1].date_taken) / (60 * 60.0)
        self.trip_city = trip_city

    def tostring(self):
        return



#mapper is a function to take the data of ImageData object as a tuple.
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
        tag_gap = len(set3) * 1.0 / len(set1)  # multiplied by 1.0 to avoid data loss from float to int conversion
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

'''
Using Python's inbuilt geopy module/library to detect the City name from available longitude and latitude.


def CityNameDetection(Event_latitude, Event_longitude):
    location = geolocator.reverse((Event_latitude, Event_longitude))
    json_loc_data = location.raw    #location.raw is an in built fxn of geopy which gives output in the form of json file.
    addr_dict =  json_loc_data['address']  #taking the value of only address in json file is in the form of dictionary. so here "address" is the key in json dictionary
    try :                                  # 'address' key also contains a dictionary ion its value, which has keys like, city, state, country etc.
        return (addr_dict['city'], addr_dict['state'])

    except KeyError:
        pass

'''

def getplace(lat, lon):
    try:
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false" % (lat, lon)
        v = urlopen(url).read()
        j = json.loads(v)
        components = j['results'][0]['address_components']
        country = town = None
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
            if "administrative_area_level_2" in c['types']:
                town = c['long_name']
        return str(town), str(country)
    except UnicodeEncodeError:
        return 'Fetch Error'






'''Event Set is a list which is a list of list, inside which events are present
i.e. in one listthere is a set of Images which are coming within one event.
Similarly 2nd item of this is also containing a list of images of another event.
'''
event_set = []

"""
image_info_db is a list which will contain the data of images(tuples) read from Database, to do further operations.
this list contaions the information of all images in the form of ImageData object, i.e. it is holding ImageData objects in it.
"""
image_info_db = []

# Making connection with database.
conn = sqlite3.connect('Flickr.db')
print "Opened Flickr database successfully"

#Connecting cursor/filehandler with database.
print "Sorting the images of Database in descending order. "
cursor = conn.execute("SELECT *  from ProcessedData_out order by datetaken DESC")

for row in cursor:
    # Taking the values from Database row by row and appending to a list 'image_info_db'.
    image_info_db.append(mapper(row))

print "Sorted the data according to date in descending order Successfully and stored the tuples in a list in Memory."
Gn_list = []  # List to store the values of Gn for each image.

'''
We have assumed all these values namely k, d, alpha and beta as nothing is given about them in the research paper.
'''

k = 1.5
d = 5
alpha = 0.1
beta = 0.3


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
        # distGap variable is taking the value of distance gap from function call.
        distGap = calculateDistanceGap(float(j.latitude),float(j.longitude),float(next_row.latitude),float(next_row.longitude))

        # Calling calculateTagGap function through object tagGap.
        tagGap = calculateTagGap(j.tags.split(" "), next_row.tags.split(" "))

        # Calculating value of gn(considered as a change of events)
        j.gn = (1 - alpha - beta) * tgap + alpha * distGap + beta * tagGap

        Gn_list.append(j.gn)


event = []

###################
print "Detecting the events of a users from available photos with geo-tagged information."
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
        event.append(value)
        event_set.append(event)
        event = list()
    else:
        event.append(value)

##################################
Trips = []
#################################


outfile = open("outputfileofevents_withoutDuration.txt", "w")
i=0
for p in event_set:
    print 'Event Number %d :'%i
    for images in p:
        #print images.id, images.owner, images.title, images.date_taken, images.tags, images.latitude, images.longitude
        outfile.write(images.id + " " + images.owner + " " + images.title + " " + str(images.date_taken) + " " + images.tags + " " + str(images.latitude) + str(images.longitude) + "\n")
    i += 1
    #print '\n'
    outfile.write("\n")

outfile.close()

print "Segmentation of events done successfully, and saved the result in text file with name outputfileofevents_withoutDuration.txt"
print "Total %d events found for this user from the available photos.." %i



#for p in event_set:
    #city_name = getplace(p[len(p) - 1].latitude, p[len(p) - 1].longitude)
    #city_name0 = getplace(p[0].latitude, p[0].longitude)
    #title_name_of_last_img = p[len(p) - 1].title
    #title_name_of_1st_img = p[0].title
    #id_last = p[len(p) - 1].id,
    #id_first = p[0].id
    #event_duration = (p[0].date_taken - p[len(p) - 1].date_taken) / (60 * 60.0)

    #print city_name, asd
    #asd = asd+1
    #print city_name0



'''
    #print id_first,
    #print id_last
    #print title_name_of_1st_img
    #print title_name_of_last_img

    print 'New Event detected :'
    city_name_con = str(city_name0)
    print 'City Name: %s ' %city_name_con
    #print city_name,
    print 'Event duration %f hours' %event_duration, "\n"

    # open file for appending or it will create a new file if file is not present
    outfile = open("output.txt", "w")

'''




print "Detecting Event duration and City name of each event."
for p in event_set:
    trip = TripsData(p)
    Trips.append(trip)


outfile2 = open("Trips3.txt", "w")
for demo_item in Trips:
    for img in demo_item.trip_images_metadata:
        print demo_item.duration, demo_item.trip_city,  img.title, img.tags
        outfile2.write(str(demo_item.duration) +','+ str(demo_item.trip_city) +',' + str(img.title) +',' + str(img.tags))
        outfile2.write("\n")
    outfile2.write("\n")

outfile2.close()


#Trips ===> (List of Trip(Event)) ===> Trip ===> List of Image metadata and duration and city ==> Image metadata ===> ImageDataObject