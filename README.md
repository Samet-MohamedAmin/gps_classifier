# gps_classifier
classify photos according to GPS tag

# what does this module do ?
This script helps classifying photos based on GPSTags.
After running this script, each image from (base_unknown_dir) will be classified in this root : (base_dir)/country_long/state_long/city/road.
GPSTags of images are extracted with PIL module.
(country_long, state_long, city, road) information are extracted from (image_latitude, image_longitude) given from google API using (geocoder module).
Samples must be in (base_unknown_dir).

# Dependencies
### pillow module
$ pip3 install pillow
### gecoder
( I will get rid of it as soon as possible)
$ pip3 install geocoder
http://geocoder.readthedocs.io/


# what's next?
#### get rid of geocoder
#### use other api for classifying like bing and yandex

## samples are from https://readexifdata.com/
