from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session

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

@app.route('/search', strict_slashes=False)
def search():
    """show page for recent recommendations"""
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