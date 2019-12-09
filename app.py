from decouple import config
from faker import Faker
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import *


def create_app():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
        app.config['ENV'] = config('ENV')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        DB.init_app(app)


        @app.route('/')
        def index():
            #figure out why users aren't displaying
            users = User.query.all()
            return render_template('base.html', title='homepage', users=users)

        @app.route('/result', methods=['POST', 'GET'])
        # This runs the function that adds user data to db, then shows said username.
        # TODO: Actually show user's ten latest tweets.
        def result():
            if request.method == 'POST':
                username = request.form
                user = TWITTER.get_user(username['handle'])
                embedded_tweet_to_db(user)
                return render_template('result.html', title='Results!', username=username)

        # DELETE THE FOLLOWING FOR PRODUCTION
        @app.route('/reset')
        def reset():
            DB.drop_all()
            DB.create_all()
            return render_template('base.html', title='DB Reset!', users=[])

        return app

"""
app = Flask(__name__)



@app.route('/user/<username>')
def show_user_profile(username):
    #show profile for user
    return f'User :: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    #show post with given id, id is int
    return 'Post %d' % (post_id+1)

if __name__ == "__main__":
    app.run()
"""
