# Scraping
# "Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK"
import time

import utilities as u # Scraping utilities

url = 'https://www.yr.no/place/Norway/Oslo/Oslo/Oslo/'
data = u.generate_HTML_string(url)
temperatureData = u.extract_between(data, "Temperature: ", "\xc2\xb0.  Feels")
windData = u.extract_between(data, 'txt-left" title="', "For the")

for l in windData:
    if "m/s" in l:
        print l

print(time.mktime(time.gmtime()))
# print(time.ctime(time.gmtime()))

#print(time.asctime(time.gmtime()))