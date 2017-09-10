from geopy.geocoders import Nominatim
geolocator = Nominatim()

x = 52.509669
y = 13.376294
location = geolocator.reverse((x,y))
print(location.address)