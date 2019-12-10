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
            DB.create_all()
            return render_template('base.html', title='homepage')

        # DELETE THE FOLLOWING FOR PRODUCTION
        @app.route('/reset')
        def reset():
            DB.drop_all()
            DB.create_all()
            return render_template('base.html', title='DB Reset!', users=[])

        @app.route('/user', methods=['POST'])
        @app.route('/user/<handle>', methods=['GET'])
        def user(handle=None, message=''):
            handle = handle or request.values['handle']

            try:
                if request.method == 'POST':
                    add_or_update_user(handle)
                    # Returns the User object so we can do stuff with it
                    user = User.query.filter(User.handle == handle).one()
                    message = f"{handle} successfully added! Here are {user.name}'s tweets:"
                tweets = user.tweets
            except Exception as e:
                message = f'Error adding {handle}: {e}'
                tweets = []
            return render_template('user.html', title=handle,
                                    tweets=tweets, message=message)


        return app
