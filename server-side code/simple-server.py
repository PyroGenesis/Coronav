import crawler
from pprint import pprint
from flask import Flask
from flask import request
import requests
from flask_cors import CORS
import time
import xmlrpc.client
import json
import Helper

app = Flask(__name__)
CORS(app)
api_key_old = "AIzaSyBoNu3yqKSWgoTslBifyBPLZvoioLWdRZo"
api_key = "AIzaSyBulK8ZjV3NbE8w01vjlsI0YZlgS3bHuN8"

def getNearbyPlaceIdsHelper(lat, lng, first_call, pagetoken, limit=60):
	global api_key
	# print(type(lat))
	# print(lng)
	# print(first_call)
	# print(type(pagetoken))
	if first_call: 
		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&rankby=distance&key='+str(api_key)
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


# demo url: http://127.0.0.1:5000/getNearbyPlaceIds2?lat=33.6471628&lng=-117.8411294
@app.route('/getNearbyPlaceIds2')
def getNearbyPlaceIds2(lat=None, lng=None, limit=60):
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

	# while counter<3:
	fields = 'formatted_address,geometry,place_id,name,type'
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&fields='+fields+'&rankby=distance&key='+str(api_key)
	r = requests.get(url, auth=('user', 'pass'))
	# print('\n\n\n\n')
	# pprint(r.json())
	# print('\n\n\n\n')
	#result = getNearbyPlaceIdsHelper(lat, lng, counter==0, result['page_token'])
		# for place_id in result['nearbyPlaceIds']: 
		# 	ret.append(place_id)
		# print('ret.len: '+str(len(ret)))
		# print('result[page_token]: '+str(result['page_token']))
		# if result['page_token']==None:
			# print(counter)
			# print('breaking')
			# break
		# print('sleeping')
		# time.sleep(2)
		# print('sleeping done')
		# counter+=1	

	for r_item in r.json()['results']:
		ret_item = {}
		ret_item_details = {}
		address = r_item["formatted_address"] if "formatted_address" in r_item else r_item.get("vicinity", "")
		ret_item_details['address'] = address #r_item['formatted_address']
		ret_item_details['coordinates'] = r_item['geometry']['location']
		lat, lng = ret_item_details['coordinates']['lat'], ret_item_details['coordinates']['lng']
		ret_item_details['id'] = r_item['place_id']
		ret_item_details['types'] = r_item['types']
		ret_item_details['name'] = r_item['name']
		ret_item_details['populartimes'] = getDummyValueTest(lat, lng)['populartimes']
		ret_item['details'] = ret_item_details
		ret_item['place_id'] = r_item['place_id']
		

		ret.append(ret_item)
	return {'places':ret}


# demo url: http://127.0.0.1:5000/getNearbyPlaceIds3?lat=33.6471628&lng=-117.8411294
@app.route('/getNearbyPlaceIds3')
def getNearbyPlaceIds3(lat=None, lng=None, limit=60):
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

	# while counter<3:
	fields = 'formatted_address,geometry,place_id,name,type'
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&fields='+fields+'&rankby=distance&key='+str(api_key)
	r = requests.get(url, auth=('user', 'pass'))
	# print('\n\n\n\n')
	# pprint(r.json())
	# print('\n\n\n\n')
	#result = getNearbyPlaceIdsHelper(lat, lng, counter==0, result['page_token'])
		# for place_id in result['nearbyPlaceIds']: 
		# 	ret.append(place_id)
		# print('ret.len: '+str(len(ret)))
		# print('result[page_token]: '+str(result['page_token']))
		# if result['page_token']==None:
			# print(counter)
			# print('breaking')
			# break
		# print('sleeping')
		# time.sleep(2)
		# print('sleeping done')
		# counter+=1	

	for r_item in r.json()['results']:
		ret_item = {}
		ret_item_details = {}
		address = r_item["formatted_address"] if "formatted_address" in r_item else r_item.get("vicinity", "")
		ret_item_details['address'] = address #r_item['formatted_address']
		ret_item_details['coordinates'] = r_item['geometry']['location']
		lat, lng = ret_item_details['coordinates']['lat'], ret_item_details['coordinates']['lng']
		ret_item_details['id'] = r_item['place_id']
		ret_item_details['types'] = r_item['types']
		ret_item_details['name'] = r_item['name']
		ret_item_details['populartimes'] = getDummyValueTest2(lat, lng)['populartimes']
		ret_item['details'] = ret_item_details
		ret_item['place_id'] = r_item['place_id']
		

		ret.append(ret_item)
	return {'places':ret}




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

# @app.route('/getPopularTimesSpecial')
# def getPopularTimesSpecial(place_id=None):
# 	global api_key
# 	if place_id==None:
# 		place_id = request.args.get('placeId')
# 	# print('calling crawler')
# 	place_details = crawler.get_populartimes(api_key, place_id)
# 	try:
# 		place_details['populartimes']
# 		place_details['hasPopularTimes'] = True
# 	except:
# 		place_details['hasPopularTimes'] = False
# 	place_details['geometry'] = 
# 	return place_details


#demo url: http://127.0.0.1:5000/getNearbyPopularTimes?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes3')
def getNearbyPopularTimes(lat=None, lng=None):
	global dummy
	# return dummy
	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	print('debugging:')
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
			populartimes['hasPopularTimes'] = True
		except:
			populartimes['hasPopularTimes'] = False
			# continue
		#populartimesDict[place_id].append(populartimes)
		popularTime = {"place_id":place_id, "details":populartimes}
		populartimesDict.append(popularTime)
		# print(populartimes)
		# return dummy
		
		# s.insertData(populartimes)
		
		# limit-=1
		# except:
		# 	continue
	return {"places": populartimesDict}

#demo url: http://127.0.0.1:5000/getNearbyPopularTimes3?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes')
def getNearbyPopularTimes3(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		

	print(str(lat)+' '+str(lng))

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
	print('lat: {} lng: {}'.format(lat, lng))

	searchResultPlaceDetails = {}
	searchResultPlaceDetails['details'] = getPopularTimes(place_id)
	searchResultPlaceDetails['geometry'] = r.json()['candidates'][0]['geometry']
	try:
		searchResultPlaceDetails['details']['populartimes']
		searchResultPlaceDetails['hasPopularTimes'] = True
	except:
		searchResultPlaceDetails['hasPopularTimes'] = False
	# nearbyPlaces = getNearbyPopularTimes3(lat, lng)
	# near
	# for place in nearbyPlaces['places']:
	# 	if place['details']['id'] != place_id:
	# 		nearbyPlaces2['places'].
	# print('getSearchResults')
	# print('lat: '+str(lat))
	# print('lng: '+str(lng))
	temp_ = getNearbyPopularTimes3(lat, lng)['places']
	nearbyPlaces = [place for place in temp_ if place['details']['id']!=place_id]
	return {'searchResult': searchResultPlaceDetails, 'nearbyPlaces': nearbyPlaces}


# demo url: http://127.0.0.1:5000/getSearchResults2?text=Langson%20Library
@app.route('/getSearchResults2')
def getSearchResults2(text=None):
	global api_key
	if text==None:
		text = request.args.get('text')
	url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+text+'&inputtype=textquery&fields=geometry,place_id&key='+api_key
	r = requests.get(url, auth=('user', 'pass'))

	print('\n\n\n')
	print(r.json())
	print('\n\n\n')
	
	place_id = r.json()['candidates'][0]['place_id']
	lat, lng = r.json()['candidates'][0]['geometry']['location'].values()
	print('lat: {} lng: {}'.format(lat, lng))

	searchResultPlaceDetails = {}
	searchResultPlaceDetails['details'] = getPopularTimes(place_id)
	searchResultPlaceDetails['geometry'] = r.json()['candidates'][0]['geometry']
	try:
		searchResultPlaceDetails['details']['populartimes']
		searchResultPlaceDetails['hasPopularTimes'] = True
	except:
		searchResultPlaceDetails['hasPopularTimes'] = False
	# nearbyPlaces = getNearbyPopularTimes3(lat, lng)
	# near
	# for place in nearbyPlaces['places']:
	# 	if place['details']['id'] != place_id:
	# 		nearbyPlaces2['places'].
	# print('getSearchResults')
	# print('lat: '+str(lat))
	# print('lng: '+str(lng))
	temp_ = getNearbyPopularTimes6(lat, lng)
	# return {'--':temp_}
	# print(place['details'])
	nearbyPlaces = [place for place in temp_['places'] if place['details']['id']!=place_id]
	return {'searchResult': searchResultPlaceDetails, 'nearbyPlaces': nearbyPlaces}


# demo url: http://127.0.0.1:5000/getDummyValueTest?lat=34.048829&lng=-118.259248
@app.route('/getDummyValueTest')
def getDummyValueTest(lat=None, lng=None):

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	
	estimate = Helper.get_estimate(lat, lng)
	return {'populartimes':Helper.conversion(estimate)}

@app.route('/getDummyValueTest2')
def getDummyValueTest2(lat=None, lng=None):

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	
	estimate = Helper.get_varied_estimate(lat, lng)
	return {'populartimes':estimate}



#demo url: http://127.0.0.1:5000/getNearbyPopularTimes5?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes5')
def getNearbyPopularTimes5(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	print('lat: '+str(lat))
	print('lng: '+str(lng))
	# s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')

	# return dummy
	# lat = request.args.get('lat')
	# lng = request.args.get('lng')		
	place_details = getNearbyPlaceIds2(lat,lng)
	# print(place_ids)
	populartimesDict = place_details
	# populartimesDict = s.fetchDetails(place_ids)

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



#demo url: http://127.0.0.1:5000/getNearbyPopularTimes6?lat=33.6704072&lng=-117.8282598
@app.route('/getNearbyPopularTimes6')
def getNearbyPopularTimes6(lat=None, lng=None):
	global dummy

	if lat==None:
		lat = request.args.get('lat')
		lng = request.args.get('lng')		
	print('lat: '+str(lat))
	print('lng: '+str(lng))
	# s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')

	# return dummy
	# lat = request.args.get('lat')
	# lng = request.args.get('lng')		
	place_details = getNearbyPlaceIds3(lat,lng)
	# print(place_ids)
	populartimesDict = place_details
	# populartimesDict = s.fetchDetails(place_ids)

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


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__=="__main__":
	global dummy
	dummy = {
  	"places": [
	    {
	      "details": {
	        "address": "3810-3820 Michelson Dr, Irvine, CA 92612, USA", 
	        "coordinates": {
	          "lat": 33.6676238, 
	          "lng": -117.8292908
	        }, 
	        "id": "ChIJN3AGltfd3IAR4k2iiOgz0RU", 
	        "international_phone_number": "+1 949-786-5522", 
	        "name": "Rancho San Joaquin Driving Range", 
	        "populartimes": [
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              7, 
	              21, 
	              40, 
	              59, 
	              65, 
	              58, 
	              48, 
	              46, 
	              55, 
	              70, 
	              80, 
	              80, 
	              75, 
	              79, 
	              84, 
	              62, 
	              25, 
	              0
	            ], 
	            "name": "Monday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              40, 
	              68, 
	              84, 
	              80, 
	              69, 
	              68, 
	              81, 
	              91, 
	              91, 
	              88, 
	              82, 
	              55, 
	              20, 
	              0
	            ], 
	            "name": "Tuesday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              5, 
	              26, 
	              55, 
	              67, 
	              56, 
	              46, 
	              49, 
	              59, 
	              65, 
	              67, 
	              66, 
	              68, 
	              74, 
	              80, 
	              75, 
	              56, 
	              32, 
	              0
	            ], 
	            "name": "Wednesday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              7, 
	              25, 
	              52, 
	              70, 
	              70, 
	              61, 
	              56, 
	              59, 
	              62, 
	              63, 
	              65, 
	              73, 
	              88, 
	              95, 
	              83, 
	              55, 
	              26, 
	              0
	            ], 
	            "name": "Thursday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              6, 
	              26, 
	              53, 
	              64, 
	              62, 
	              68, 
	              80, 
	              83, 
	              77, 
	              70, 
	              70, 
	              74, 
	              76, 
	              68, 
	              51, 
	              32, 
	              16, 
	              0
	            ], 
	            "name": "Friday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              11, 
	              39, 
	              69, 
	              80, 
	              76, 
	              77, 
	              83, 
	              87, 
	              89, 
	              90, 
	              88, 
	              78, 
	              62, 
	              43, 
	              25, 
	              11, 
	              3, 
	              0
	            ], 
	            "name": "Saturday"
	          }, 
	          {
	            "data": [
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              0, 
	              10, 
	              28, 
	              50, 
	              64, 
	              63, 
	              55, 
	              56, 
	              70, 
	              89, 
	              100, 
	              95, 
	              77, 
	              53, 
	              32, 
	              21, 
	              15, 
	              6, 
	              0
	            ], 
	            "name": "Sunday"
	          }
	        ], 
	        "rating": 4.3, 
	        "rating_n": 80, 
	        "types": [
	          "point_of_interest", 
	          "establishment"
	        ]
	      }, 
	      "place_id": "ChIJN3AGltfd3IAR4k2iiOgz0RU"
	    }
	  ]
	}
	with open('larger-nearby-result.json') as f:
		dummy2 = json.load(f)
	dummy = dummy2
	app.run(host="0.0.0.0")

