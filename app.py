from flask import Flask, render_template, redirect, url_for, request
import omdb
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

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
    if request.method == 'POST':
        user_search = request.form.get('search')
        try:
            response = omdb.request(t=user_search, apikey='a7a81366')
            data = response.json()
            return render_template('search.html', data=data)
        except Exception:
            message = "Could not find anything on " + user_search
            return render_template('search.html', message=message)
        
    return render_template('search.html')

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