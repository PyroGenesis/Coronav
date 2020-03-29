from math import sin, cos, sqrt, atan2, radians
import json
import operator

d = None
estimations_per_day_of_the_week_per_hr_per_station = None
d_loaded = False
estimations_loaded = False

def lat_lon_dist(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance



# write a function that, given a lat, long pair, will return the closest station
def get_closest_station(lat, lng):
    global d_loaded, d
    if not d_loaded:
        with open('lat_lon_per_station.json') as f:
            d = json.load(f)
        d_loaded = True
    l = [(key, d[key]) for key in d.keys()]
    distances = [0] * len(l)
    for i in range(len(l)):
        distances[i] = lat_lon_dist( lat, lng, l[i][1][0], l[i][1][1])
    min_idx = distances.index(min(distances))
    return l[min_idx][0]



# write a function that given a lat, lng pair will return the estimate
def get_estimate(lat, lng):
    global estimations_loaded, estimations_per_day_of_the_week_per_hr_per_station
    # day_of_the_week = None
    if not estimations_loaded:
        with open('estimations_per_day_of_the_week_per_hr_per_station.json') as f:
            estimations_per_day_of_the_week_per_hr_per_station = json.load(f)
        estimations_loaded = True
    station = get_closest_station(lat, lng)
    # print(station)
    # temp = str(day_of_the_week) +' '+ str(time_)
    # print(temp)
    if station not in estimations_per_day_of_the_week_per_hr_per_station:
        return 0
    # if temp not in estimations_per_day_of_the_week_per_hr_per_station[station]:
    #     return 0
    return estimations_per_day_of_the_week_per_hr_per_station[station]


def get_estimate2(lat, lng,station):
    global estimations_loaded, estimations_per_day_of_the_week_per_hr_per_station
    # day_of_the_week = None
    if not estimations_loaded:
        with open('estimations_per_day_of_the_week_per_hr_per_station.json') as f:
            estimations_per_day_of_the_week_per_hr_per_station = json.load(f)
        estimations_loaded = True
    # station = get_closest_station(lat, lng)
    # print(station)
    # temp = str(day_of_the_week) +' '+ str(time_)
    # print(temp)
    if station not in estimations_per_day_of_the_week_per_hr_per_station:
        return 0
    # if temp not in estimations_per_day_of_the_week_per_hr_per_station[station]:
    #     return 0
    return estimations_per_day_of_the_week_per_hr_per_station[station]




#convert estimations to populartime

def conversion(estimate):
    times = ['{:0>2}'.format(i)+':00:00' for i in range(24)]
    populartimes = []
    week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    for i in range(7):
        populartimes.append({"data":[0]*24, "name":week_days[i]})
    
    for i in range(7):
        for j, time_ in enumerate(times):
            try:
                populartimes[i]["data"][j] = estimate[str(i)+' '+time_] * 4.5
            except Exception as e:
                continue

    return populartimes

# write a function that, given a lat, long pair, will return the closest station
def get_closest_stations(lat, lng):
    global d_loaded, d
    if not d_loaded:
        with open('lat_lon_per_station.json') as f:
            d = json.load(f)
        d_loaded = True
    l = [(key, d[key]) for key in d.keys()]
    distances = [0] * len(l)
    for i in range(len(l)):
        distances[i] = (i,lat_lon_dist( lat, lng, l[i][1][0], l[i][1][1]))
    distances_sorted = sorted(distances, key=operator.itemgetter(1))
    
#     min_idx = distances.index(min(distances))
    return [l[x[0]][0] for x in distances_sorted[:5]]

def get_varied_estimate(lat, lng):
    stations = get_closest_stations(lat, lng)
    print(stations)
    week_days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    ans = [{'data':[0]*24, 'name':week_days[i]} for i in range(7)]
    for station in stations:
        x = conversion(get_estimate2(lat,lng, station))
        # pprint(x)
        # break
        for i, day in enumerate(x):
            for j, hr in enumerate(day['data']):
                ans[i]['data'][j] += hr
    # print('\n\n\n')
    # print(ans)
    # print('\n\n\n')
    for i, day in enumerate(x):
        for j, hr in enumerate(day['data']):
            ans[i]['data'][j] /= len(stations)
    # print('\n\n\n')
    # print(ans)
    # print('\n\n\n')
            
    return ans
    # ans
