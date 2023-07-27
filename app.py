from flask import Flask, render_template, redirect, url_for, request
from caching import Cache
import omdb
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
cache = Cache()

API_KEY = os.getenv('API_KEY')

@app.route('/', strict_slashes=False)
def login():
    """Renders login in page to user"""
    return render_template('login.html')

@app.get('/register', strict_slashes=False)
def register():
    """Renders register page to user"""
    return render_template('register.html')

@app.route('/home', strict_slashes=False)
def home():
    """show homepage of website"""
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """show page for movie search"""
    return render_template('search.html')

@app.route('/search_item', methods=['POST'])
def search_item():
    """searches for movie content"""
    query = request.get_json()
    item = query['value']
    
    # check cache for query
    if item in cache.cached_data:
        return cache.get(item)
    
    response = omdb.request(t=item, apikey=API_KEY, timeout=5)
    data = response.json()
    cache.put(item, data)
    return data

@app.route('/preference', strict_slashes=False)
def preference():
    """contains logic for preference page"""
    return render_template('preference.html')

@app.route('/logout', strict_slashes=False)
def logout():
    """Logs user out of website"""
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)