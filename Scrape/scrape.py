# Scraping
import time

import utilities as u # Scraping utilities

url = 'https://www.yr.no/place/Norway/Oslo/Oslo/Oslo/'
#data = u.generate_HTML_string(url)
#data = u.extract_between(data, "Temperature: ", "\xc2\xb0.  Feels")
#print(data)

print(time.mktime(time.gmtime()))
# print(time.ctime(time.gmtime()))

#print(time.asctime(time.gmtime()))