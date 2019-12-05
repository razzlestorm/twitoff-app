from faker import Faker
from flask import Flask
from .models import db, User, Tweet
import uuid


def create_app():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
        db.init_app(app)


        @app.route('/')
        def index():
            rand_name = str(uuid.uuid4())
            rand_u = User(name=rand_name)
            rand_tweet = Faker()
            db.session.add(rand_u)
            #db.session.add(rand_tweet.text())
            db.session.commit()
            return 'Index Page'

        @app.route('/hello')
        def hello():
            return render_template('base.html', title='hello')

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
