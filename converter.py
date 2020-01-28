# coding: utf-8

"""
Geolocataion conversion between WGS84, BD09 and GCJ02.
WGS84 / BD09 / GCJ02 / MapBar 经纬度坐标互转。

- WGS84: GPS coordinates for Google Earth (GPS坐标，谷歌地球使用)
- GCJ02: national coordinate system developed by China (国测局坐标，谷歌中国地图、腾讯地图、高德地图使用)
- BD09: Baidu coordinates (百度坐标系，百度地图使用)
- MapBar: MapBar coordinates (图吧坐标系，图吧地图使用)

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
    if out_of_china(lng, lat):
        return lng, lat
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
    if out_of_china(lng, lat):
        return lng, lat
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


def mapbar_to_wgs84(lng, lat):
    """MapBar -> WGS84"""
    lng = lng * 100000.0 % 36000000
    lat = lat * 100000.0 % 36000000
    lng1 = int(lng - math.cos(lat / 100000.0) * lng / 18000.0 - math.sin(lng / 100000.0) * lat / 9000.0) 
    lat1 = int(lat - math.sin(lat / 100000.0) * lng / 18000.0 - math.cos(lng / 100000.0) * lat / 9000.0)
    lng2 = int(lng - math.cos(lat1 / 100000.0) * lng1 / 18000.0 - math.sin(lng1 / 100000.0) * lat1 / 9000.0 + (1 if lng > 0 else -1))
    lat2 = int(lat - math.sin(lat1 / 100000.0) * lng1 / 18000.0 - math.cos(lng1 / 100000.0) * lat1 / 9000.0 + (1 if lat > 0 else -1)) 
    lng, lat = lng2 / 100000.0, lat2 / 100000.0
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


def out_of_china(lng, lat):
    """No offset when coordinate out of China."""
    if lng < 72.004 or lng > 137.8437:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


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


def mapbar_to_gcj02(lng, lat):
    """MapBar -> GCJ02"""
    lng, lat = mapbar_to_wgs84(lng, lat)
    lng, lat = wgs84_to_gcj02(lng, lat)
    return lng, lat


def mapbar_to_bd09(lng, lat):
    """MapBar -> BD09"""
    lng, lat = mapbar_to_wgs84(lng, lat)
    lng, lat = wgs84_to_bd09(lng, lat)
    return lng, lat


if __name__ == '__main__':
    blng, blat = 121.4681891220,31.1526609317
    print('BD09:', (blng, blat))
    print('BD09 -> GCJ02:', bd09_to_gcj02(blng, blat))
    print('BD09 -> WGS84:',bd09_to_wgs84(blng, blat))
    wlng, wlat = 121.45718237717077, 31.14846209914084
    print('WGS84:', (wlng, wlat))
    print('WGS84 -> GCJ02:', wgs84_to_gcj02(wlng, wlat))
    print('WGS84 -> BD09:', wgs84_to_bd09(wlng, wlat))
    mblng, mblat = 121.4667323772, 31.1450420991
    print('MapBar:', (mblng, mblat))
    print('MapBar -> WGS84:', mapbar_to_wgs84(mblng, mblat))
    print('MapBar -> GCJ02:', mapbar_to_gcj02(mblng, mblat))
    print('MapBar -> BD09:', mapbar_to_bd09(mblng, mblat))
