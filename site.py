import os
import requests
import random 
import json
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
app.secret_key = 'beets_baxter_turnips_wasabi'
login_manager = LoginManager()
login_manager.init_app(app)



movie_ids = [539681, 361743, 857]
movie_imgs = [
                'https://upload.wikimedia.org/wikipedia/en/0/09/DC_League_of_Super-Pets.jpg',
                'https://upload.wikimedia.org/wikipedia/en/1/13/Top_Gun_Maverick_Poster.jpg',
                'https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg'
            ]


class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    user = db.Column(db.String(80), nullable = False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(80), unique=True, nullable = False)


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
    movie_data.append(movie_ids[num])
    return movie_data

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sign.html')

@app.route('/login/check', methods = ["GET", "POST"])
def login_check():
    data = request.form
    username = data.get('username')
    if username == "":
        flash('Please enter a username before hitting submit genius.')
        return redirect(url_for('login'))
    check = User.query.filter_by(user=username).first()
    if check:
        login_user(check)
        return redirect(url_for('movies'))
    flash("That user does not exist. Please sign up or try again with a different username.")
    return redirect(url_for('login'))


@app.route('/signup/check', methods = ["GET", "POST"])
def signup_check():
    data = request.form
    username = data.get('username')
    if username == "":
        flash('Please enter a username before hitting submit genius.')
        return redirect(url_for('signup'))
    check = User.query.filter_by(user=username).first()
    if check:
        flash("That username is taken. Please enter a different one.")
        return redirect(url_for('signup'))
    
    new_user = User(user = username)
    db.session.add(new_user)
    db.session.commit()
    flash("You have been sucessfully signed up.")
    return redirect(url_for('login'))

@app.route('/movies/submitted', methods = ["GET", "POST"])
def review_check():
    data = request.form
    movie_id = data.get("movie_id")
    user = current_user.user
    rating = data.get("rating")
    comment = data.get("comments")
    
    if rating == "":
        flash('Enter a rating before you click submit')
        return redirect(url_for('movies'))
    elif not(rating.isnumeric() and 1 <= int(rating) and int(rating) <= 10):
        flash('Make sure your rating is a number between 1 and 10')
        return redirect(url_for('movies'))
    if comment == "":
        comment = "(No comments)"
    
    movie_review = Review(movie_id = movie_id, user = user, rating = rating, comment = comment)
    db.session.add(movie_review)
    db.session.commit()
    flash("Your response has been recorded.")
    return redirect(url_for('movies'))


@app.route('/movies', methods = ["GET", "POST"])
@login_required
def movies():
    mov_data = get_movie_data()
    review_array = []
    review_data = Review.query.filter_by(movie_id = mov_data[5]).all()
    for i in review_data:
        review_array.append(i)
    return render_template('index.html', 
                            title = mov_data[0],
                            tagline = mov_data[1],
                            genre = mov_data[2],
                            img = mov_data[3],
                            link = mov_data[4],
                            movie_id = mov_data[5],
                            reviews = review_array)

