import os
import requests
import random 
import json
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

movie_ids = [539681, 361743, 857]
movie_imgs = [
                'https://upload.wikimedia.org/wikipedia/en/0/09/DC_League_of_Super-Pets.jpg',
                'https://upload.wikimedia.org/wikipedia/en/1/13/Top_Gun_Maverick_Poster.jpg',
                'https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg'
            ]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.secret_key = 'beets_baxter_turnips_wasabi'
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    user = db.Column(db.String(80), unique=True, nullable = False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)

with app.app_context():
    db.create_all()


def get_rand():
    num_of_movies = len(movie_ids) - 1
    return random.randint(0, num_of_movies)


def get_tmdb_data(movie_id):
    TMDB_API_REQUEST = f'https://api.themoviedb.org/3/movie/{movie_id}?'

    response = requests.get(
        TMDB_API_REQUEST, params = {'api_key': os.getenv('TMDB_API_KEY')}
    )

    return response.json()


def get_wiki_link(title):
    WIKI_API_REQUEST = "https://en.wikipedia.org/w/api.php"
    response = requests.get(
        WIKI_API_REQUEST, params = {
            "action": "opensearch",
            "namespace": "0",
            "search": f"{title}",
            "limit": "5",
            "format": "json"
        }
    )

    wiki_json_data = response.json()
    return wiki_json_data[3][0]


def get_genre_string(genre_list):
    base_string = "Genres: "
    for i in genre_list:
        base_string += f'{i["name"]}, ' 
    return base_string[:-2]
        

def get_movie_data():
    movie_data = []
    num = get_rand()
    tmdb_data = get_tmdb_data(movie_ids[num])
   
    movie_data.append(tmdb_data['title'])
    movie_data.append(tmdb_data['tagline'])
    movie_data.append(get_genre_string(tmdb_data['genres']))
    movie_data.append(movie_imgs[num])
    movie_data.append(get_wiki_link(movie_data[0]))
    return movie_data

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sign.html')

@app.route('/login/check', methods = ["POST"])
def login_check():
    data = request.form
    user = data.get('username')
    if user == "":
        flash('Please enter a username before hitting submit genius')
        return redirect(url_for('login'))
    return user

@app.route('/signup/check', methods = ["POST"])
def signup_check():
    data = request.form
    user = data.get('username')
    if user == "":
        flash('Please enter a username before hitting submit genius')
        return redirect(url_for('signup'))
    return user

@app.route('/movies/submitted', methods = ["POST"])
def review_check():
    data = request.form
    rating = data.get("rating")
    comments = data.get("comments")
    
    if rating == "":
        flash('Enter a rating before you click submit')
        return redirect(url_for('movies'))
    elif not(rating.isnumeric() and 1 <= rating and rating <= 10):
        flash('Make sure your rating is a number between 1 and 10')
        return redirect(url_for('movies'))


@app.route('/movies', methods = ["POST"])
def movies():
    mov_data = get_movie_data()
    return render_template('index.html', 
                            title = mov_data[0],
                            tagline = mov_data[1],
                            genre = mov_data[2],
                            img = mov_data[3],
                            link = mov_data[4])

app.run()