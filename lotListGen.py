import json
from math import radians, cos, sin, asin, sqrt
from autogreen import get_lot_by_id
import operator

# 3rd Dining Hall:  'longitude': 121.4331684297, u'latitude': 31.0268419338
# SEIEE Building: "longitude":121.4415578204,"latitude":31.0248415951
# we make the 3rd Dining Hall our home location
home_lon = 121.4331684297
home_lat = 31.0268419338
seiee_lon = 121.4415578204
seiee_lat = 31.0248415951


# haversine function covert gps coordinate to distance in metres
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000


# This function updates lotlist.txt, only need once
def getList():
    f = open('lots.txt', 'r')
    j = json.loads(f.readline())
    f.close()
    listd = []
    for item in j['dataList']:
        distance = haversine(item['longitude'], item['latitude'], home_lon, home_lat)
        id = item['id']
        details = get_lot_by_id(id,False)
        info = {'id': item['id'], 'distance': distance, 'address': details['address'],'lon':item['longitude'],'lat':item['latitude']}
        listd.append(info)
        print 'written %d' % int(id)

    str = json.dumps(listd, encoding='utf-8')
    f = open('lotList.txt', 'w')
    f.write(str)
    f.close()


def printList():
    f = open('lotlist.txt', 'r')
    j = json.loads(f.readline())
    j_sorted = sorted(j, key=operator.itemgetter('distance'))
    print '---------------------------------------------------------------------------------------------------------'
    for item in j_sorted:
        if (item['distance'] < 2000):  # filter by distance
            print 'Id:%d Distance:%.2fm | Address:%s' % (item['id'], item['distance'], item['address'])
