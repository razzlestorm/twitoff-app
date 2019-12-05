from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)

class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Unicode(280), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship("User", backref=db.backref('tweets', lazy=True))
