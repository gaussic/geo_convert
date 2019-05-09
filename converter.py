# coding: utf-8

"""
Geolocataion converting between WGS84, BD09 and GCJ02.
WGS84 / BD09 / GCJ02 经纬度坐标互转。

- WGS84: GPS coordinates for Google Earth (GPS坐标，谷歌地球使用)
- GCJ02: national coordinate system developed by China (国测局坐标，谷歌地图使用)
- BD09: Baidu coordinates (百度坐标系，百度地图使用)

Test website: http://gpsspg.com/maps.htm

Author: Gaussic
Date:   2019-05-09
"""

import math

PI = math.pi
PIX = math.pi * 3000 / 180
EE = 0.00669342162296594323
A = 6378245.0


def bd09_to_gcj02(lng, lat):
    """BD09 -> GCJ02"""
    x, y =  lng - 0.0065, lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PIX)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PIX)
    lng, lat = z * math.cos(theta), z * math.sin(theta)
    return lng, lat


def gcj02_to_bd09(lng, lat):
    """GCJ02 -> BD09"""
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * PIX)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * PIX)
    lng, lat = z * math.cos(theta) + 0.0065, z * math.sin(theta) + 0.006
    return lng, lat


def gcj02_to_wgs84(lng, lat):
    """GCJ02 -> WGS84"""
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    lng, lat = lng - dlng, lat - dlat
    return lng, lat


def wgs84_to_gcj02(lng, lat):
    """WGS84 -> GCJ02"""
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    lng, lat = lng + dlng, lat + dlat
    return lng, lat


def bd09_to_wgs84(lng, lat):
    """BD09 -> WGS84"""
    lng, lat = bd09_to_gcj02(lng, lat)
    lng, lat = gcj02_to_wgs84(lng, lat)
    return lng, lat


def wgs84_to_bd09(lng, lat):
    """WGS84 -> BD09"""
    lng, lat = wgs84_to_gcj02(lng, lat)
    lng, lat = gcj02_to_bd09(lng, lat)
    return lng, lat


def transform_lat(lng, lat):
    """GCJ02 latitude transformation"""
    ret = -100 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320.0 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def transform_lng(lng, lat):
    """GCJ02 longtitude transformation"""
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


if __name__ == '__main__':
    blng, blat = 121.4681891220,31.1526609317
    print('BD09:', (blng, blat))
    print('BD09 -> GCJ02:', bd09_to_gcj02(blng, blat))
    print('BD09 -> WGS84:',bd09_to_wgs84(blng, blat))
    wlng, wlat = 121.45718237717077, 31.14846209914084
    print('WGS84:', (wlng, wlat))
    print('WGS84 -> GCJ02:', wgs84_to_gcj02(wlng, wlat))
    print('WGS84 -> BD09:', wgs84_to_bd09(wlng, wlat))
