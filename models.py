from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
  __tablename__ = "Users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(200), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profiles = db.relationship('userProfile', back_populates='user')
  
  def __repr__(self):
    return f"{self.username} -> {self.password}"

class userProfile(db.Model):
  __tablename__ = "profile"
  
  id = db.Column(db.Integer, primary_key=True)
  genre = db.Column(db.String(100), nullable=False)
  rated = db.Column(db.String(15), nullable=False)
  language = db.Column(db.String(100), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey(User.id))
  user = db.relationship('User', back_populates='profiles')

  def __repr__(self):
    return f"{self.genre} {self.rated} {self.language} {self.location}"