from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.model):
    __tablename__ = 'users'
    
    id = db.Column(db.Interger, primary_key = True)
    
    # rest 
    
    
    songs = db.relationship('song' , back_populates = 'User')