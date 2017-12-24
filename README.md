# gps_classifier
classify photos according to GPS tag

# Code example
After running the script, each image from (base_unknown_dir) will be classified in this path : (base_dir)/country_long/state_long/city/road.  
GPSTags of images are extracted with PIL module.  
(country_long, state_long, city, road) information are extracted from (image_latitude, image_longitude) given from google API using (geocoder module).  
Samples must be in (base_unknown_dir).  
The script is written in python 3

# Installation
### Dependencies
#### pillow
```bash
$ pip3 install pillow
```
http://pillow.readthedocs.io/
#### gecoder
```bash
$ pip3 install geocoder
```
http://geocoder.readthedocs.io/

# Tests
#### samples are from https://readexifdata.com/


# what's next?
- get rid of geocoder
- use optional APIs to get location like **openstreetmap**, **bing** and **yandex**


# License
GNU General Public License v3.0
