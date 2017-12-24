# This script helps classifying photos based on GPSTags.
# After running this script, each image from (base_unknown_dir) will be classified
# in this root : (base_dir)/country_long/state_long/city/road.
# GPSTags of images are extracted with PIL module.
# (country_long, state_long, city, road) information are extracted
# from (image_latitude, image_longitude) given by google API using (geocoder module).
# Samples must be in (base_unknown_dir).


import os
import geocoder
from PIL import ExifTags, Image


def convert_to_deg(value, ref):
    """
    convert latitude or longitude value to degree
    :param value: latitude or longitude
    :param ref: latitude : ['N', 'S']; longitude['E', 'W']
    :return result: latitude or longitude on degree form rounded to round_n
    """
    round_n = 6
    result = 0
    k = 1
    for v_1, v_2 in value:
        result += v_1 / (v_2 * k)
        k *= 60.0
    if (ref == 'S') | (ref == 'W'):
        result *= -1
    return round(result, round_n)


def get_gps_tags():
    """
    :return gps_tags: dictionary containing necessary tags
    """
    gps_tags = {}
    gps_tags['GPS_info'] = 0
    tags = ExifTags.TAGS
    for tag in tags.items():
        if gps_tags['GPS_info']: break
        if tag[1] == 'GPSInfo': gps_tags['GPS_info'] = tag[0]
    for tag in ExifTags.GPSTAGS.items():
        if tag[1] == 'GPSLatitude':
            gps_tags['GPS_lat'] = tag[0]
        elif tag[1] == 'GPSLatitudeRef':
            gps_tags['GPS_lat_ref'] = tag[0]
        elif tag[1] == 'GPSLongitude':
            gps_tags['GPS_lon'] = tag[0]
        elif tag[1] == 'GPSLongitudeRef':
            gps_tags['GPS_lon_ref'] = tag[0]

    return gps_tags

# base_dir : the base directory
base_dir = 'base'
# base_unknown_dir : the base directory
base_unknown_dir = os.path.join(base_dir, 'unknown')

# number of requests to do if nothing happen
n_tests = 5
# None folder name
none_name = 'other'
gps_tags = get_gps_tags()
# img_no_gps : number of images without gps tags
img_no_gps = 0
# img_no_class : number of images with gps tags without classification
img_no_class = 0

if __name__ == "__main__":
    try:
        os.listdir(base_unknown_dir)
    except OSError:
        print('the base dir %s must exist to continue' % base_unknown_dir)
        exit()

    k = input('please put all the samples in %s then press <enter>\n' % os.path.abspath(base_unknown_dir))
    print('make sure you have internet connection')

    for img_name in os.listdir(base_unknown_dir):
        # considering all images are type
        if not img_name.upper().endswith('JPG'):
            continue
        img = Image.open(os.path.join(base_unknown_dir, img_name))

        img_exif = img._getexif()
        if img_exif:
            try:
                img_gps_info = img_exif[gps_tags['GPS_info']]
                img_gps_lat = convert_to_deg(img_gps_info[gps_tags['GPS_lat']],
                                             img_gps_info[gps_tags['GPS_lat_ref']])
                img_gps_lon = convert_to_deg(img_gps_info[gps_tags['GPS_lon']],
                                             img_gps_info[gps_tags['GPS_lon_ref']])
            except:
                img_no_gps += 1
                continue

            print('==>', img_name, (img_gps_lat, img_gps_lon))
            k = 0
            n_requests = n_tests
            values = []
            while (n_requests != 0) & (k == 0):
                print('%d tests remaining' % n_requests)
                n_requests -= 1
                g = geocoder.google([img_gps_lat, img_gps_lon], method='reverse')
                values = [base_dir, g.country_long, g.state_long, g.city, g.road]
                k = len(values) - 1
                for i in range(1, len(values)):
                    if values[i] is None:
                        k -= 1
                        values[i] = none_name
            # if response is valid
            if k > 0:
                src = os.path.join(base_unknown_dir, img_name)
                dst = '/'.join(values)
                try: os.makedirs(dst)
                except OSError: pass
                img.close()
                print('moving image from \'%s\' to \'%s\'' % (src, os.path.join(dst, img_name)))
                os.rename(src, os.path.join(dst, img_name))
            # if all results are None after n_tests try
            else:
                img_no_class += 1
        # if the image has no exif tags
        else:
            img_no_gps += 1

    print('# images without gps tag = %d' % img_no_gps)
    print('# images with gps tags without classification = %d' % img_no_class)
