from urllib2 import urlopen
import json
components=''
def getplace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    #print j['results'][0]['address_components']
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return str(town), str(country)

#print components

print getplace(52.1, 11.1)
a, b = getplace(51.1, 0.1)
print a, b

print getplace(52.1, 10.1)

