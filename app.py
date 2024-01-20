from flask import Flask, Response
from flask import render_template
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

# gets the first 5 wildfires from the database for a collection


def get_sample_wildfires_data(collection):
    # Retrieve data from MongoDB
    data_cursor = collection.find({}, {"features": 1})

    # Convert cursor to list
    data_list = list(data_cursor)

    # Extract relevant fields from each document
    formatted_data = []
    for data in data_list:
        for feature in data['features']:
            formatted_data.append(feature)
            if len(formatted_data) >= 5:
                break
        if len(formatted_data) >= 5:
            break
    response = json.dumps(formatted_data, indent=4)

    return Response(response, mimetype='application/json')


def get_all_wildfires_data(collection):
    # Retrieve data from MongoDB
    data_cursor = collection.find({}, {"features": 1})

    # Convert cursor to list
    data_list = list(data_cursor)

    # Extract relevant fields from each document
    formatted_data = []
    for data in data_list:
        for feature in data['features']:
            formatted_data.append(feature)
    response = json.dumps(formatted_data, indent=4)

    return Response(response, mimetype='application/json')


@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1/wildfires/2000-2004'>/api/v1/wildfires/2000-2004</a> - 00-04 MongoDB First 5 results in JSON.<br/>"
        f"<a href='/api/v1/wildfires/2005-2009'>/api/v1/wildfires/2005-2009</a> - 05-09 MongoDB First 5 results in JSON.<br/>"
        f"<a href='/api/v1/wildfires/2010-2015'>/api/v1/wildfires/2010-2015</a> - 10-15 MongoDB First 5 results in JSON.<br/>"
        f"<a href='/api/v1/mapbox'>/api/v1/mapbox</a><br>"
    )

# @app.route('/api/v1/wildfires(1992-1999)')


@app.route('/api/v1/wildfires/2000-2004')
def wildfires_2000_2004():
    return get_sample_wildfires_data(collection1)


@app.route('/api/v1/wildfires/2005-2009')
def wildfires_2005_2009():
    return get_sample_wildfires_data(collection2)


@app.route('/api/v1/wildfires/2010-2015')
def wildfires_2010_2015():
    return get_sample_wildfires_data(collection3)


@app.route('/api/v1/mapbox')
def show_html():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
