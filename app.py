from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/myanimals')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
animals = db.myanimals


app = Flask(__name__)

# @app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg="Welcome to Noah's Ark!" )

@app.route('/')
def animals_index():
    """Show all animals."""
    return render_template('animals_index.html',animals=animals.find())

@app.route('/animals/<animal_id>',methods=['GET'])
def show_animal(animal_id):
    """Show a single animal."""
    animal = animals.find_one({'_id': ObjectId(animal_id)})
    return render_template('show_animal.html', animal=animal)





if __name__ == '__main__':
    app.run(debug=True)
