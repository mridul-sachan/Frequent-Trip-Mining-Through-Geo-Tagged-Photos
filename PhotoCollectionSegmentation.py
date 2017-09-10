
#Implementing Photo Collection Segmentation phase of awt paper given in page number 136.

import math

lat1 = 0
lat2 = 0
delta = 0
lamda1 = 0

def distance_gap():
    ''' Function math.asin(x) Returns the arc sine of x, in radians.
    Refer https://docs.python.org/2/library/math.html for more details.'''
    # arcsin_arg is calculating the argument value of arcsin() as given in equation 4 under Photo Collection Segmentation.
    #delta and lambda1  is the difference of latitude and longitude of these photos i.e. two consecutive photos.
    #lat2 and lat1 are the latitudes of Photo k+1 and Photo K.
    arcsin_arg = math.sqrt( math.sin(delta/2) ** 2 + (math.cos(lat2) * math.cos(lat1) * math.sin(lambda1 / 2) **2 ))

    phi_rad = 2 * math.asin(arcsin_arg)                    # Equation 4 -- page 136

    # 6370Km is D i.e. radius of the Earth.
    return math.log10(6370 * phi_rad)                      # Equation 3 second part

Lpk1 = []
Lpk2 = []

def tag_gap():
    if Lpk1 > 0 :
        ''' Implementing equation 5 under Photo Collection Segmentation.
        Python Intersection i.e. Lpk intersection Lpk+1 - https://docs.python.org/2/library/sets.html
        Here I have taken Lpk = Lpk1 and Lpk+1 = Lpk2
        '''
        mod_value1 = math.modf(Lpk1 & Lpk2) / math.modf(Lpk1)
        return int(1- mod_value1)
    elif Lpk1 == 0 & Lpk2 == 0 :
        return int(0.5)

    else :
        return int(0)

def time_gap():
    timegap = math.log10(t2 - t1)  #t2 = T base pk+1 and t1 = t base pk in equation 3 -- page 136

    return timegap

# Gn = change of events
g_n = []
for i in list_1:
    alpha = 0
    beta = 0
    value_of_time_gap = 0
    value_of_distance_gap = 0
    value_of_tag_gap = 0
    g_n[i] = (1- alpha - beta) * value_of_time_gap + alpha * value_of_distance_gap + beta * value_of_tag_gap




event_set = []
image_info_db = []
"""
conn = sqlite3.connect('Flickr.db')
print "Opened database successfully"

cursor = conn.execute("SELECT *  from OUT")
for row in cursor:
    image_info_db.append(mapper(row))

for i, j in enumerate(image_info_db):
    if i != len(image_info_db) - 1:
        j.gn = calculateGap(image_info_db,i)

image_info_db[len(image_info_db) - 1] = ??

// gn
// if gn >
//      push current set into list
//      put currennt element into new set

"""


for x in g_n:
    for i in range(-d, d ):
        temp_Gn = x
        temp_Gn += 1

    if x >= (K + (1/(2D + 1) ) * temp_Gn):
        print 'Event Changed.'  #But now problem is how to classify it,. means whatever we are getting from this module where to store it
                            # and what to do with it. ?