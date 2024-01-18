from flask import Flask
from pymongo import MongoClient
import json
from flask import jsonify
from flask import render_template

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wildfires_db']
collection = db['wildfires']


def load_data():
    file_path = './Resources/Wildfires 2.geojson'
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
            print("Data already loaded in the database.")
    return


load_data()


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1/wildfires'>/api/v1/wildfires</a> - List wildfires JSON data, loaded in a MongoDB server. First 5 results.<br/>"
        f"<a href='/api/v1/mapbox'>/api/v1/mapbox</a><br>"
    )


@app.route('/api/v1/wildfires')
def get_wildfires_data():
    # Retrieve data from MongoDB
    data_cursor = collection.find().limit(5)

    # Convert cursor to list
    data_list = list(data_cursor)

    # Convert ObjectId to string, because MongoDB uses ObjectId type and JSON does not support it
    for document in data_list:
        document['_id'] = str(document['_id'])

    return jsonify(data_list)


@app.route('/api/v1/mapbox')
def show_html():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
