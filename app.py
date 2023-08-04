from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import RegisterForm, LoginForm, recommendationForm
from recommendation import get_movie_by_params, get_trending_movies, get_popular_movies
from models import db, User, userProfile
from datetime import timedelta
from caching import Cache
import requests
import os
from dotenv import load_dotenv


# get environment variables
load_dotenv()

# initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.permanent_session_lifetime = timedelta(minutes=50)
cache = Cache()
db.init_app(app)

# create database
with app.app_context():
    db.create_all()

API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Renders login in page to user"""
    # take user to homepage if user is logged in
    if 'user' in session:
        return redirect(url_for('home'))

    password = None
    username = None
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username,
                                 password=password).first()
        if user is None:
            flash("Invalid username or password")
            form.username.data = ''
            form.password.data = ''
            return render_template('login.html', form=form)
        else:
            session['user'] = username
            session.permanent = True
            return redirect(url_for('home', username=username))

    return render_template('login.html',
                           username=username,
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders register page to user"""
    username = None
    email = None
    password = None
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        with app.app_context():
            print(user)
        if user is None:
            user = User(username=username,
                        email=email, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            session.permanent = True
            return redirect(url_for('home', username=username))
        else:
            flash("User with email already exists")
            return render_template('register.html',
                                   form=form)
    
    return render_template('register.html',
                           form=form,
                           username=username)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """show homepage of website"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # get user from session
    username = session['user']
    
    # check cache for data
    if 'result' in cache.cached_data and 'trending' in cache.cached_data and 'popular' in cache.cached_data:
        return render_template('home.html', username=username,
                               result=cache.get('result'),
                               trending=cache.get('trending'),
                               popular=cache.get('popular'))
    
    # get user details form db
    user = User.query.filter_by(username=username).first()
    
    # get user profile from db
    profile = userProfile.query.filter_by(user_id=user.id).first()
    
    # set default values for null profile
    result = None

    if profile is None:
        data = get_movie_by_params(28, 'en')
        result = list(filter(lambda x: x['poster_path'] != '',data['results']))
    else:
        # fetch movies with posters from api based on user profile
        data = get_movie_by_params(int(profile.genre), profile.language)
        result = list(filter(lambda x: x['poster_path'] != '',data['results']))
    
    # get trending movies with posters from api
    trending = get_trending_movies(os.getenv('API_KEY2'))
    trending_movies = list(filter(lambda x: x['poster_path'] != '', trending))
    
    # get popular movies with posters from api
    popular = get_popular_movies(os.getenv('API_KEY2'))
    popular_movies = list(filter(lambda x: x['poster_path'] != '', popular))
    
    cache.put('result', result)
    cache.put('trending', trending_movies)
    cache.put('popular', popular_movies)
    return render_template('home.html', username=username,
                           result=result,
                           trending=trending_movies,
                           popular=popular_movies)


@app.route('/info/<title>', methods=['GET', 'POST'])
def display_movie_info(title):
    """Displays movie info"""
    base_url = f'https://api.themoviedb.org/3/search/movie'
    
    # check cache for query
    if title in cache.cached_data:
        return cache.get(title)
    params = {
        'query': title,
        'api_key': os.getenv('API_KEY2')
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    result = data['results']
    cache.put(title, result)
    return render_template('info.html',
                           result=result)

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
    form = recommendationForm()

    if form.validate_on_submit():
        # clear cached data
        cache.cached_data = {}

        genre = form.genre.data
        language = form.language.data
        
        # retrieve user
        logged_in_user = session['user']
        user = User.query.filter_by(username=logged_in_user).first()
        logged_in_user_id = user.id

        # check if user has generated profile
        profile = userProfile.query.filter_by(user_id=logged_in_user_id).first()
        if profile is None:
            profile = userProfile(genre=genre,language=language,user_id=logged_in_user_id)
            db.session.add(profile)
            db.session.commit()
            flash('Created Successfully')
        else:
            # update current user profile
            profile.genre = genre
            profile.language = language
            db.session.add(profile)
            db.session.commit()
            flash('Created Successfully')

    return render_template('preference.html',form=form)

@app.route('/logout')
def logout():
    """Logs user out of website"""
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)