from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import RegisterForm, LoginForm, profileForm
from get_movies import get_movie_by_params, get_trending_movies
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, userProfile
from datetime import timedelta
from caching import Cache
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.permanent_session_lifetime = timedelta(days=1)
API_KEY = os.getenv('API_KEY')
cache = Cache()
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Renders login page to the user"""
    if 'user' in session:
        return redirect(url_for('home', username=session['user']))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            flash("Invalid username or password")
            form.email.data = ''
            form.password.data = ''
            return redirect(url_for('login'))

        password_is_valid = check_password_hash(user.password, password)
        if not password_is_valid:
            flash("Invalid username or password")
            form.email.data = ''
            form.password.data = ''
            return render_template('login.html', form=form)
        
        session['user'] = user.username
        session.permanent = True
        return redirect(url_for('home', username=user.username))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders register page to the user"""
    username = None
    email = None
    password = None
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            hashed_password = generate_password_hash(password, 'sha256')
            user = User(username=username,
                        email=email, password=hashed_password)

            db.session.add(user)
            db.session.commit()
            session['user'] = username
            session.permanent = True
            return redirect(url_for('home', username=username))
        else:
            flash("User with email already exists")
            return redirect(url_for('register', form=form))
    
    return render_template('register.html',
                           form=form,
                           username=username)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """show homepage of website"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    
    # check cache for data
    if 'result' in cache.cached_data and 'trending' in cache.cached_data:
        return render_template('home.html', username=username,
                               result=cache.get('result'),
                               trending=cache.get('trending'))
    
    user = User.query.filter_by(username=username).first()
    profile = userProfile.query.filter_by(user_id=user.id).first()
    
    result = None

    if profile is None:
        # show action movies as default
        data = get_movie_by_params(28, 'en')
        result = list(filter(lambda x: x['poster_path'] != '',
                             data['results']))
    else:
        # fetch movies with posters from api based on user profile
        data = get_movie_by_params(int(profile.genre), profile.language)
        result = list(filter(lambda x: x['poster_path'] != '',
                             data['results']))
    
    # get trending movies with posters from api
    trending = get_trending_movies(os.getenv('API_KEY2'))
    trending_movies = list(filter(lambda x: x['poster_path'] != '',
                                  trending))
    
    cache.put('result', result)
    cache.put('trending', trending_movies)
    return render_template('home.html', username=username,
                           result=result,
                           trending=trending_movies)

@app.route('/search')
def search():
    """show page for movie search"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('search.html')


@app.route('/search_item', methods=['POST'])
def search_item():
    """searches for movie content"""
    base_url = f'https://api.themoviedb.org/3/search/movie'
    query = request.get_json()
    item = query['value']
    
    # check cache for query
    if item in cache.cached_data:
        return cache.get(item)
    params = {
        'query': item,
        'api_key': os.getenv('API_KEY2')
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    result = data['results']
    cache.put(item, result)
    return result


@app.route('/preference', methods=['GET', 'POST'])
def preference():
    """contains logic for preference page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    genre = None
    language = None
    form = profileForm()

    if form.validate_on_submit():
        cache.cached_data = {}

        genre = form.genre.data
        language = form.language.data
        
        logged_in_user = session['user']
        user = User.query.filter_by(username=logged_in_user).first()
        logged_in_user_id = user.id

        profile = userProfile.query.filter_by(user_id=logged_in_user_id).first()
        if profile is None:
            profile = userProfile(genre=genre,language=language,
                                  user_id=logged_in_user_id)
            profile.user = user
            db.session.add(profile)
            db.session.commit()
            flash('Created Successfully')

        else:
            profile.genre = genre
            profile.language = language
            db.session.add(profile)
            db.session.commit()
            flash('Created Successfully')

    return render_template('preference.html',form=form)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html'), 500

@app.route('/logout')
def logout():
    """Logs user out of website"""
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)