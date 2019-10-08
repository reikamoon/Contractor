from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Animals')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
animals = db.animals

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Fox Finder!')

@app.route('/animals/<animal_id>',methods=['GET'])
def show_animal(animal_id):
    """Show a single animal."""
    animal = animals.find_one({'_id': ObjectId(animal_id)})
    return render_template('show_animal.html', animal=animal)

# @app.route('/animals')
# def playlists_index():
#     """Show all playlists."""
#     return render_template('playlists_index.html', playlists=playlists.find())



if __name__ == '__main__':
    app.run(debug=True)
