from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS,cross_origin
from bson import ObjectId
import json
from datetime import datetime
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

def custom_serializer(obj):
    #Changing the format of data for frontend
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def calculate_distance(lat1, lon1, lat2, lon2):

    #Finding the distance between restaurant and airbnb=
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = geodesic(coord1, coord2).miles

    return round(distance,2)

@app.route('/search_airbnb', methods=['POST'])
@cross_origin()
def connect_airbnb():

    #Connecting the database
    url = "mongodb://gvijaya5:fourthtask2@ac-e5wstzm-shard-00-00.7d3djjw.mongodb.net:27017,ac-e5wstzm-shard-00-01.7d3djjw.mongodb.net:27017,ac-e5wstzm-shard-00-02.7d3djjw.mongodb.net:27017/?ssl=true&replicaSet=atlas-956jhs-shard-0&authSource=admin&retryWrites=true&w=majority"
    print("inside the 1st api")
    client = MongoClient(url)
    db = client['sample_airbnb']
    collection = db['listingsAndReviews']
    
    #Fetching information from React
    data = request.json
    name = data.get('name')
    suburb = data.get('suburb')
    airbnb_id = data.get('id')

    selected_airbnb = []
    query = {}
    
    #if the input has airbnb_id in it
    if airbnb_id:
        query["id"] = airbnb_id
        selected_airbnb = list(collection.find(query))
    
    #if the airbnb name and airbnb suburb have been provided as well        
    if name and suburb:
        query["name"] = name
        query["address"] = {"suburb": suburb}
        selected_airbnb = list(collection.find(query))
        if len(selected_airbnb) > 1:
            print("Multiple")
            return jsonify({'response': 2, 'message': 'Multiple Airbnb found enter the id as well'})
    
    #if only the airbnb name has been provided
    elif name and not suburb:
        query["name"] = name
        selected_airbnb = list(collection.find(query))
        if len(selected_airbnb) > 1:
            print("Multiple")
            return jsonify({'response': 1, 'message': 'Multiple Airbnb found enter the suburb as well'})

    if len(selected_airbnb) == 0:
        print("NONE")
        return jsonify({'response': 3, 'message': 'No matching Airbnb found.'})

    selected_airbnb_item = selected_airbnb[0]
    latitude = selected_airbnb_item['address']['location']['coordinates'][1]
    longitude = selected_airbnb_item['address']['location']['coordinates'][0]
    if client:
        client.close()
    print(latitude,longitude)
    return jsonify({'response': 4, 'latitude': latitude, 'longitude': longitude})

@app.route('/api/restaurants', methods=['POST'])
@cross_origin()
def get_restaurants():
    print("inside the 2nd api")
    
    #Connecting the database
    url = "mongodb://gvijaya5:fourthtask2@ac-e5wstzm-shard-00-00.7d3djjw.mongodb.net:27017,ac-e5wstzm-shard-00-01.7d3djjw.mongodb.net:27017,ac-e5wstzm-shard-00-02.7d3djjw.mongodb.net:27017/?ssl=true&replicaSet=atlas-956jhs-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(url)
    db = client['sample_restaurants']
    collection = db['restaurants']

    #Fetching information from React
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    uri = 'mongodb+srv://gvijaya5:fourthtask2@cluster0.7d3djjw.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(uri, connect=True)
    print("Connected client")

    collection.create_index([("address.coord", "2dsphere")])    
    print("index has been created")
    query = {
        'address.coord': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                '$maxDistance': 3 * 1609.34  # Maximum distance in meters (e.g., 5000 meters = 5 km)
            }
        }
    }

    
    restaurants = list(collection.find(query))

    #Processing the data from database
    for restaurant in restaurants:
        restaurant['distance'] = calculate_distance(latitude, longitude, restaurant['address']['coord'][1], restaurant['address']['coord'][0])

        grades = restaurant.get('grades', [])
        if grades:
            ratings = [grade.get('score', 0) for grade in grades]
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = 0
        restaurant['averagerating'] = round(average_rating,2)

    json_restaurants = json.dumps(restaurants, default=custom_serializer)
    print(restaurants[0])
    if client:
        client.close()
    return json_restaurants

if __name__ == '__main__':
    app.run()
