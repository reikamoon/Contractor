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

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg="Welcome to Noah's Ark!" )

@app.route('/animals')
def animals_index():
    """Show all animals."""
    return render_template('animals_index.html',animals=animals.find())


@app.route('/animals/<animal_id>',methods=['GET'])
def show_animal(animal_id):
    """Show a single animal."""
    animal = animals.find_one({'_id': ObjectId(animal_id)})
    return render_template('show_animal.html', animal=animal)

@app.route('/edit/<animal_id>')
def animal_edit(animal_id):
    """Show the edit form for an animal."""
    animal = animals.find_one({'_id': ObjectId(animal_id)})
    return render_template('animal_edit.html', animal=animal, title='Edit Animal')

@app.route('/edit/<animal_id>', methods=['POST'])
def animal_update(animal_id):
    """Submit an edited animal."""
    updated_animal = {
        'name': request.form.get('name'),
        'species': request.form.get('species'),
        'breed': request.form.get('breed'),
        'color': request.form.get('color'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    animals.update_one(
        {'_id': ObjectId(animal_id)},
        {'$set': updated_animal})
    return redirect(url_for('show_animal', animal_id=animal_id))

@app.route('/animals/new')
def listings_new():
    """Create a new listing."""
    return render_template('animals_new.html', animal={}, title='Add a Listing')

@app.route('/animals/<animal_id>', methods=['POST'])
def animals_submit():
    """Submit a new animal."""
    animal = {
    'name': request.form.get('name'),
    'species': request.form.get('species'),
    'breed': request.form.get('breed'),
    'color': request.form.get('color'),
    'price': request.form.get('price'),
    'image': request.form.get('image')

    }
    print(animal)
    animal_id = animals.insert_one(animal).inserted_id
    return redirect(url_for('animals_index', animal_id=animal_id))

@app.route('/animals/<animal_id>/delete', methods=['POST'])
def animals_delete(animal_id):
    """Delete one animal."""
    animals.delete_one({'_id': ObjectId(animal_id)})
    return redirect(url_for('animals_index'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
