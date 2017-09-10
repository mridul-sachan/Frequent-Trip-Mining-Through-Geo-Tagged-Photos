import urllib
import xml.etree.ElementTree as ET
from BeautifulSoup import *

sum1 = 0

url = raw_input('Enter URL - ')
# html = urllib.urlopen(url).read()
uh = urllib.urlopen(url)
data = uh.read()

commentinfo = ET.fromstring(data)
list1 = commentinfo.findall('photos/photo')
print 'user count :', len(list1)
for item in list1:
    print 'ID :', item.get("id"),
    print 'Owner ID :', item.get("owner"),
    print 'Title :', item.get("title"),
