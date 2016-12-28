from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reviews(db.Model):
   review_id = db.Column('review_id', db.Integer, primary_key = True)
   review_hotel = db.Column(db.String(100))
   review_city = db.Column(db.String(50))
   review_body = db.Column(db.String(200))
   review_rating = db.Column(db.String(200))


def __init__(self, review_hotel, review_city, review_body, review_rating):

   self.review_hotel = review_hotel
   self.review_city = review_city
   self.review_body = review_body
   self.review_rating = review_rating


class Users(db.Model):
   user_id = db.Column('user_id', db.Integer, primary_key = True)
   user_name = db.Column(db.String(100))
   user_username = db.Column(db.String(50))
   user_password = db.Column(db.String(200))


def __init__(self, user_id, user_name, user_username, user_password):
   self.user_id = user_id
   self.user_name = user_name
   self.user_username = user_username
   self.user_password = user_password