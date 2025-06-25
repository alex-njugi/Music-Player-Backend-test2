from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship



db = SQLAlchemy()

class Song(db.model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Interger , primary_key = True)
    title = db.Column(db.String, nullable = False)
    artist = db.Column(db.String , nullable = False)
    genre = db.column(db.String , nullable = False)
    url= db.Column(db.STring, nullable = False)
    user_id = db.Column(db.String, nullable = False)
    
    user = db.relationship('User' , back_populates = 'Song')
    
def __rep__(self):
    return f'<song {self.id} , {self.title} , {self.artist} , {self.genre} , {self.url}>'