from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from random import choice
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Fox Finder!')

@app.route('/animals')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())



if __name__ == '__main__':
    app.run(debug=True)
