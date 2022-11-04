import os
import requests
import random 
import json
from flask import Flask, render_template
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
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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
    return random.randint(0, 2)


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

def main():
    mov_data = get_movie_data()
    return render_template('index.html', 
                            title = mov_data[0],
                            tagline = mov_data[1],
                            genre = mov_data[2],
                            img = mov_data[3],
                            link = mov_data[4])