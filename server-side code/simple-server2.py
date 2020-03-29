import crawler
from pprint import pprint
from flask import Flask
from flask import request
import requests
from flask_cors import CORS
import time
import xmlrpc.client
import json

app = Flask(__name__)
# CORS(app)
api_key_old = "AIzaSyBoNu3yqKSWgoTslBifyBPLZvoioLWdRZo"
api_key = "AIzaSyBulK8ZjV3NbE8w01vjlsI0YZlgS3bHuN8"

def getNearbyPlaceIdsHelper(lat, lng, first_call, pagetoken, limit=60):
	global api_key
	# print(type(lat))
	# print(lng)
	# print(first_call)
	# print(type(pagetoken))
	if first_call: 
		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&radius=1000&key='+str(api_key)
	else:
		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+pagetoken+'&key='+str(api_key)

	# print(url)
	r = requests.get(url, auth=('user', 'pass'))
	# print('\n\n\n\n')
	# try:
	# 	print(r.json()['results'])
	# except:
	# 	print('except')
	# 	pass
	# print('\n\n\n\n')
	# return r.json()
	place_ids = [result['place_id'] for result in r.json()['results']]

	page_token = None
	try:
		# print(r.json())
		page_token = r.json()['next_page_token']
		# print(page_token)
	except:
		# print(r.json().keys())
		page_token = None
	return {'nearbyPlaceIds':place_ids, 'page_token':page_token}


# demo url: http://127.0.0.1:5000/getNearbyPlaceIds?lat=33.6471628&lng=-117.8411294
@app.route('/getNearbyPlaceIds')
def getNearbyPlaceIds(lat=None, lng=None, limit=60):
	# global api_key
	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')
	# # print(type(lat))
	# # print(lng)
	# url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&radius=500&key='+str(api_key)
	# # print(url)
	# r = requests.get(url, auth=('user', 'pass'))
	# # return r.json()
	# place_ids = [result['place_id'] for result in r.json()['results']]
	ret = []
	result = {'nearbyPlaceIds':[], 'page_token':'dummy_value'}
	counter = 0

	while counter<3:
		result = getNearbyPlaceIdsHelper(lat, lng, counter==0, result['page_token'])
		for place_id in result['nearbyPlaceIds']: 
			ret.append(place_id)
		print('ret.len: '+str(len(ret)))
		print('result[page_token]: '+str(result['page_token']))
		if result['page_token']==None:
			# print(counter)
			# print('breaking')
			break
		print('sleeping')
		time.sleep(2)
		print('sleeping done')
		counter+=1

	return {'nearbyPlaceIds':ret}

#demo url: http://127.0.0.1:5000/getPopularTimes?placeId=ChIJkb-SJQ7e3IARTDp600BRFUM
@app.route('/getPopularTimes')
def getPopularTimes(place_id=None):
	global api_key
	if place_id==None:
		place_id = request.args.get('placeId')
	# print('calling crawler')
	place_details = crawler.get_populartimes(api_key, place_id)
	# print('crawling done')
	# print('\n\n\n')
	# print(place_details)
	# print('\n\n\n')
	# popular_times = place_details['populartimes']

	return place_details

#demo url: http://127.0.0.1:5000/getNearbyPopularTimes?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes')
def getNearbyPopularTimes(lat=None, lng=None):
	global dummy
	# return dummy
	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	print('lat: '+str(lat))
	print('lng: '+str(lng))
	
	return dummy
	place_ids = getNearbyPlaceIds(lat,lng,10)['nearbyPlaceIds']
	populartimesDict = []
	# limit = 2
	for place_id in place_ids:
		# if limit==0:
			# break

		#try:
		# TODO: call Ankitesh's db function here
		populartimes = getPopularTimes(place_id)

		try:
			populartimes['populartimes']
		except:
			continue
		#populartimesDict[place_id].append(populartimes)
		popularTime = {"place_id":place_id, "details":populartimes}
		populartimesDict.append(popularTime)
		# print(populartimes)
		# return dummy
		# limit-=1
		# except:
		# 	continue
	return {"places": populartimesDict}

#demo url: http://127.0.0.1:5000/getNearbyPopularTimes2?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes2')
def getNearbyPopularTimes2(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		

	s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')

	# return dummy
	# lat = request.args.get('lat')
	# lng = request.args.get('lng')		
	place_ids = getNearbyPlaceIds(lat,lng)['nearbyPlaceIds']
	populartimesDict = []
	# limit = 2
	for place_id in place_ids:
		# if limit==0:
			# break

		#try:
		# TODO: call Ankitesh's db function here
		populartimes = getPopularTimes(place_id)

		try:
			populartimes['populartimes']
		except:
			continue
		popularTime = {"place_id":place_id, "details":populartimes}
		populartimesDict.append(popularTime)
		
		try:
			s.insertData(populartimes)
		except:
			continue
		

		# limit-=1
		# except:
		# 	continue
	return {"places": populartimesDict}

#demo url: http://127.0.0.1:5000/getNearbyPopularTimes3?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes3')
def getNearbyPopularTimes3(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		

	s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')

	# return dummy
	# lat = request.args.get('lat')
	# lng = request.args.get('lng')		
	place_ids = getNearbyPlaceIds(lat,lng)['nearbyPlaceIds']
	print(place_ids)
	populartimesDict = []
	populartimesDict = s.fetchDetails(place_ids)
	# limit = 2
	# for place_id in place_ids:
	# 	# if limit==0:
	# 		# break

	# 	#try:
	# 	# TODO: call Ankitesh's db function here
	# 	populartimes = getPopularTimes(place_id)

	# 	try:
	# 		populartimes['populartimes']
	# 	except:
	# 		continue
	# 	#populartimesDict[place_id].append(populartimes)
	# 	popularTime = {"place_id":place_id, "details":populartimes}
	# 	populartimesDict.append(popularTime)
	# 	# print(populartimes)
	# 	# return dummy
		
	# 	s.insertData(populartimes)
		
		# limit-=1
		# except:
		# 	continue
	return populartimesDict


#demo url: http://127.0.0.1:5000/getNearbyPopularTimes4?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes4')
def getNearbyPopularTimes4(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	print('lat: '+str(lat))
	print('lng: '+str(lng))
	s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')

	# return dummy
	# lat = request.args.get('lat')
	# lng = request.args.get('lng')		
	place_ids = getNearbyPlaceIds(lat,lng)['nearbyPlaceIds']
	print(place_ids)
	populartimesDict = []
	populartimesDict = s.fetchDetails(place_ids)
	# limit = 2
	# for place_id in place_ids:
	# 	# if limit==0:
	# 		# break

	# 	#try:
	# 	# TODO: call Ankitesh's db function here
	# 	populartimes = getPopularTimes(place_id)

	# 	try:
	# 		populartimes['populartimes']
	# 	except:
	# 		continue
	# 	#populartimesDict[place_id].append(populartimes)
	# 	popularTime = {"place_id":place_id, "details":populartimes}
	# 	populartimesDict.append(popularTime)
	# 	# print(populartimes)
	# 	# return dummy
		
	# 	s.insertData(populartimes)
		
		# limit-=1
		# except:
		# 	continue
	return populartimesDict


# demo url: http://127.0.0.1:5000/getSearchResults?text=Langson%20Library
@app.route('/getSearchResults')
def getSearchResults(text=None):
	global api_key
	if text==None:
		text = request.args.get('text')
	url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+text+'&inputtype=textquery&fields=geometry,place_id&key='+api_key
	r = requests.get(url, auth=('user', 'pass'))
	place_id = r.json()['candidates'][0]['place_id']
	lat, lng = r.json()['candidates'][0]['geometry']['location'].values()
	return {'searchResult': getPopularTimes(place_id), 'nearbyPlaces':getNearbyPopularTimes2(lat, lng)}





@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__=="__main__":
	# global dummy
	# with open('larger-nearby-result.json') as f:
	# 	dummy2 = json.load(f)
	# dummy = dummy2
    lines = None
    ckpt = 21
    with open('emulations2.txt') as f:
        lines = f.readlines()
    for line in lines[ckpt:]:
        # print(line.split())
        split_ = line.split()
        lat = split_[1]
        lng = split_[3]
        getNearbyPopularTimes2(lat, lng)
        # break
    # app.run(host="0.0.0.0")