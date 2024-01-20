from flask import Flask, Response
from flask import render_template
from flask import request
from pymongo import MongoClient
import json

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wildfires']

if '1992-1999' in db.list_collection_names():
    db['1992-1999'].drop()
if '2000-2007' in db.list_collection_names():
    db['2000-2007'].drop()
if '2008-2015' in db.list_collection_names():
    db['2008-2015'].drop()

if '2000-2004' in db.list_collection_names():
    db['2000-2004'].drop()
if '2005-2009' in db.list_collection_names():
    db['2005-2009'].drop()
if '2010-2015' in db.list_collection_names():
    db['2010-2015'].drop()

# Create new collections based on appropriate years
collection1 = db['2000-2004']
collection2 = db['2005-2009']
collection3 = db['2010-2015']

file_paths = [
    './Resources/first_years.geojson',
    './Resources/second_years.geojson',
    './Resources/third_years.geojson'
]


def load_data(file_paths, collections):
    for file_path, collection in zip(file_paths, collections):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Check if data is already loaded in the database to avoid duplicate entries
            if collection.count_documents({}) == 0:
                if isinstance(data, list):  # Check if data is a list of records
                    collection.insert_many(data)  # Use insert_many for list
                else:
                    # Use insert_one for a single record
                    collection.insert_one(data)
            else:
                print(
                    f"Data already loaded in the collection {collection.name}.")


collections = [collection1, collection2, collection3]

load_data(file_paths, collections)

# Function to get GeoJSON data for a specific collection


def get_geojson_data(collection):
    data_cursor = collection.find({}, {"features": 1})
    data_list = list(data_cursor)
    formatted_data = []
    for data in data_list:
        for feature in data['features']:
            formatted_data.append(feature)
    response = json.dumps(formatted_data, indent=4)
    return Response(response, mimetype='application/json')


# gets the first 5 wildfires from the database for a collection


def get_sample_wildfires_data(collection):
    # Retrieve data from MongoDB
    data_cursor = collection.find({}, {"features": 1})

    # Convert cursor to list
    data_list = list(data_cursor)

    # Extract relevant fields from each document and construct the GeoJSON object
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for data in data_list:
        for feature in data['features']:
            geojson_data['features'].append(feature)
            if len(geojson_data['features']) >= 5:
                break
        if len(geojson_data['features']) >= 5:
            break

    response = json.dumps(geojson_data, indent=4)
    return Response(response, mimetype='application/json')


def get_all_wildfires_data_paginated(collection, page, per_page):
    # Retrieve all documents (this may need to be optimized for very large collections)
    data_cursor = collection.find({}, {"features": 1})
    data_list = list(data_cursor)

    # Flatten the features from all documents
    all_features = [
        feature for data in data_list for feature in data['features']]

    # Apply pagination to the flattened list of features
    start = (page - 1) * per_page
    end = start + per_page
    paginated_features = all_features[start:end]

    # Construct the GeoJSON object with paginated features
    geojson_data = {
        "type": "FeatureCollection",
        "features": paginated_features
    }

    response = json.dumps(geojson_data, indent=4)
    print(f"Page: {page}, Per page: {per_page}, Start: {start}, End: {end}")
    return Response(response, mimetype='application/json')


@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br><br/>"
        f"<a href='/api/v1/wildfires/2000-2004/sample'>/api/v1/wildfires/2000-2004/sample</a> - 2000 - 2004. Sample data for first 5 results.<br/>"
        f"<a href='/api/v1/wildfires/2005-2009/sample'>/api/v1/wildfires/2005-2009/sample</a> - 2005 - 2009. Sample data for first 5 results.<br/>"
        f"<a href='/api/v1/wildfires/2010-2015/sample'>/api/v1/wildfires/2010-2015/sample</a> - 2010 - 2015. Sample data for first 5 results.<br/>"
        f"<br><br/>"
        f"<a href='/api/v1/wildfires/2000-2004/all'>/api/v1/wildfires/2000-2004/all</a> - 2000 - 2004. Pagination results. Limited to 500 per page.<br/>"
        f"<a href='/api/v1/wildfires/2005-2009/all'>/api/v1/wildfires/2005-2009/all</a> - 2005 - 2009. Pagination results. Limited to 500 per page.<br/>"
        f"<a href='/api/v1/wildfires/2010-2015/all'>/api/v1/wildfires/2010-2015/all</a> - 2010 - 2015. Pagination results. Limited to 500 per page.<br/>"
        f"<br><br/>"
        f"Usage: <br><br/>"
        f"To retrieve the first page of 10 results for 2000 - 2004: <a href='/api/v1/wildfires/2000-2004/all?page=1&per_page=10'>/api/v1/wildfires/2000-2004/all?page=1&per_page=10</a><br/>"
        f"To retrieve the first page of 10 results for 2005 - 2009: <a href='/api/v1/wildfires/2005-2009/all?page=1&per_page=10'>/api/v1/wildfires/2005-2009/all?page=1&per_page=10</a><br/>"
        f"To retrieve the first page of 10 results for 2010 - 2015: <a href='/api/v1/wildfires/2010-2015/all?page=1&per_page=10'>/api/v1/wildfires/2010-2015/all?page=1&per_page=10</a><br/>"
        f"<br><br/>"
        f"Mapbox:<br><br/>"
        f"<a href='/api/v1/mapbox'>/api/v1/mapbox</a><br>"
    )


@app.route('/api/v1/wildfires/2000-2004/sample')
def wildfires_2000_2004():
    return get_sample_wildfires_data(collection1)


@app.route('/api/v1/wildfires/2005-2009/sample')
def wildfires_2005_2009():
    return get_sample_wildfires_data(collection2)


@app.route('/api/v1/wildfires/2010-2015/sample')
def wildfires_2010_2015():
    return get_sample_wildfires_data(collection3)


@app.route('/api/v1/wildfires/2000-2004/all')
def wildfires_2000_2004_all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 500, type=int)
    return get_all_wildfires_data_paginated(collection1, page, per_page)


@app.route('/api/v1/wildfires/2005-2009/all')
def wildfires_2005_2009_all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 500, type=int)
    return get_all_wildfires_data_paginated(collection2, page, per_page)


@app.route('/api/v1/wildfires/2010-2015/all')
def wildfires_2010_2015_all():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 500, type=int)
    return get_all_wildfires_data_paginated(collection3, page, per_page)


@app.route('/api/v1/mapbox')
def show_html():
    return render_template("index.html")


@app.route('/api/v1/geojson/2000-2004')
def geojson_2000_2004():
    return get_geojson_data(collection1)


@app.route('/api/v1/geojson/2005-2009')
def geojson_2005_2009():
    return get_geojson_data(collection2)


@app.route('/api/v1/geojson/2010-2015')
def geojson_2010_2015():
    return get_geojson_data(collection3)


if __name__ == '__main__':
    app.run()
