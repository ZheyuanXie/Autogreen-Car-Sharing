import requests
import json
import time
import operator
import lotListGen
import threading

# Id = 7 SEIEE building
# Id = 13 Third Dining Hall
# Id = 19 New Library
# Id = 28 Fourth Dining Hall / Li Zheng Dao Library
# Id = 29 Second Dining Hall
# Id = 38 Student Service Centre


def reserve_car(dotid):   # not functioning
    url = 'http://121.199.28.63/autogreen_api/v1/dot/cars'  #

    # http://121.199.28.63/autogreen_api/v1/timeshare/reserve

    url = 'http://121.199.28.63/autogreen_api/v1/timeshare/reserve'
    payload = {'token':'7a396906efd249a9bfa8e720164a7b3a','sign':'73A2784E79536BB417C1F9B46A237970'}



def get_lots():
    url = 'http://121.199.28.63/autogreen_api/v1/dot/all'
    print 'Requesting All Lots at %s ...' % time.strftime("%Y-%m-%d %X", time.localtime())
    res = requests.get(url)
    print 'Responded at %s' % time.strftime("%Y-%m-%d %X", time.localtime())
    j = json.loads(res.content)
    print 'Total Lots: %d' % (len(j['dataList']))
    listl = []
    for item in j['dataList']:
        if int(item['carNumber']) > 0:
            data = query_lot_by_id(item['id'])
            if data:
                data['carNumber'] = item['carNumber']
                listl.append(data)
                # print 'Id:%d | Add:%s | Dist:%.2f | CarNum:%d' % (item['id'], data['address'], data['distance'], item['carNumber'])
            else:
                # print 'Id:%d | Add:? | Dist:? | CarNum:%d' % (item['id'], item['carNumber'])
                pass
    return listl  # Return A List of All Lots Info (Packed in Dict)

def carinfo(car):
    plate = car['plateNumber']
    model = car['modelDescp']
    lon = car['longitude']
    lat = car['latitude']
    dist = lotListGen.haversine(lon,lat,lotListGen.home_lon,lotListGen.home_lat)
    totalM = car['totalMileage']
    restM = car['restMileage']
    f = open('lotlist.txt', 'r')
    j = json.loads(f.readline())
    f.close()
    mindist = 100000
    address = ''
    for item in j:
        edist = lotListGen.haversine(lon,lat,item['lon'],item['lat'])
        # if dist < 1600: print item['address'],edist
        if edist < mindist:
            mindist = edist
            address = item['address']
    return {'plate':plate, 'model':model, 'dist':dist, 'totalM':totalM, 'restM':restM, 'address':address}

def get_cars():
    url = 'http://121.199.28.63/autogreen_api/v1/cars'
    print 'Requesting All Cars at %s ...' % time.strftime("%Y-%m-%d %X", time.localtime())
    res = requests.get(url)
    print 'Responded at %s' % time.strftime("%Y-%m-%d %X", time.localtime())
    j = json.loads(res.content)
    print 'Total Cars: %d' % (len(j['dataList']))
    return j['dataList']  # Return A List of All Available Cars Info (Packed in Dict)

def get_lot_by_id(id,slience = False):
    url = "http://121.199.28.63/autogreen_api/v1/dot"
    payload = {'dotId': id}
    if not slience: print 'Requesting Lot ID=%d... at %s' % (id, time.strftime("%Y-%m-%d %X", time.localtime()))
    res = requests.get(url, payload)
    if not slience: print 'Responded at %s' % time.strftime("%Y-%m-%d %X", time.localtime())
    j = json.loads(res.content, encoding='utf-8')
    str = json.dumps(j, encoding='utf-8', ensure_ascii=False, indent=4)
    try:
        if not slience: print 'Result: There are %d cars at %s' % (j['data']['carNumber'], j['data']['address'])
    except:
        if not slience: print 'Not Avaiable'
    return j['data']  # Return A Dict of the selected lot info


def query_lot_by_id(id):
    f = open('lotlist.txt', 'r')
    j = json.loads(f.readline())
    f.close()
    for item in j:
        if item['id'] == id:
            return item
    return False

def get_lots_by_distance():
    # dist = int(raw_input('Distance (m) >'))
    # print '------Available cars within %d m-------'%dist
    listl = get_lots()
    listl_sorted = sorted(listl, key=operator.itemgetter('distance'))
    for item in listl_sorted:
        print item['id'],item['address'],item['carNumber'],item['distance']
    # f = open('lotlist.txt', 'r')
    # j = json.loads(f.readline())
    # f.close()
    # j_sorted = sorted(j, key=operator.itemgetter('distance'))
    # dist = int(raw_input('Distance (m) >'))
    # print '------Cars within %d m-------'%dist
    # for item in j_sorted:
    #     if (item['distance'] < dist):  # filter by distance
    #         carNum = get_lot_by_id(item['id'],slience = True)['carNumber']
    #         if carNum != 0:
    #             print 'Id:%d | Distance:%.2fm | Address:%s | Cars:%d **' % (item['id'], item['distance'], item['address'],carNum)
    #         else:
    #             print 'Id:%d | Distance:%.2fm | Address:%s | Cars:%d' % (item['id'], item['distance'], item['address'], carNum)

def get_cars_by_distance(dist = 300):
    cars = get_cars()
    listd = []
    for item in cars:
        listd.append(carinfo(item))
    listd = sorted(listd, key=operator.itemgetter('dist'))
    found = False
    for item in listd:
        if item['dist'] < dist:
            print '\a\a\a'
            found = True
        print '%s %.0fm %s %.0fkm/%.0fkm'%(item['plate'],item['dist'],item['address'],item['totalM'],item['restM'])
    print '(The location is estimated, may not be accurate)'
    return found


# repeatedly send requests until a car is found within desired range
def constant_query():
    interval = 5
    dist = 2000
    while 1:
        if get_cars_by_distance(dist):
            print 'Car found within %.0fm'%dist
            return
        print 'Waiting %d seconds...'%interval
        time.sleep(interval)


def display_menu():
    print
    print '-------MENU-------'
    print '1 - check total cars'
    print '2 - check total lots'
    print '3 - query lot by id'
    print '4 - query lots by cars'
    print '5 - query all cars'
    print '6 - constant query'
    print 'q - exit'
    print '------------------'


if __name__ == "__main__":
    display_menu()
    while 1:
        try:
            cmd = raw_input('>')
        except:
            print 'Invalid Command'
            continue
        if cmd == 'q':
            exit()
        elif cmd == '1':
            get_cars()
        elif cmd == '2':
            get_lots()
        elif cmd == '3':
            id = int(raw_input('id >'))
            get_lot_by_id(id)
        elif cmd == '4':
            get_lots_by_distance()
        elif cmd == '5':
            get_cars_by_distance()
        elif cmd == '6':
            constant_query()
        elif cmd == 'h':
            display_menu()
        else:
            print 'Invalid Command'
