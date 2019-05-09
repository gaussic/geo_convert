# coding: utf-8

"""
Geolocataion converting between WGS84, BD09 and GCJ02.

- WGS84: GPS coordinates for Google Earth
- GCJ02: national coordinate system developed by China
- BD09: Baidu coordinates


Author: Gaussic
Date:   2019-05-09
"""

import math

PIX = math.pi * 3000 / 180


def bd09_to_gcj02(longtitude, latitude):
    x, y =  longtitude - 0.0065, latitude - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PIX)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PIX)
    lng, lat = z * math.cos(theta), z * math.sin(theta)
    return lng, lat


def gcj02_to_bd09(longitude, latitude):
    z = math.sqrt(longitude * longitude + latitude * latitude) * 0.00002 * math.sin(latitude * PIX)
    




def bd09_to_wgs84(longitude, latitude):
    pass


def wgs84_to_bd09(longitude, latitude):
    pass








def gcj02_to_wgs84(longitude, latitude):
    pass


def wgs84_to_gcj02(longitude, latitude):
    pass



