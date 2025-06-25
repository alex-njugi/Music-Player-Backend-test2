from db import db

class Song(db.Model):  
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)  
    url = db.Column(db.String, nullable=False)    
    user_id = db.Column(db.String, nullable=False)
    
    user = db.relationship('User', back_populates='songs')  
    
    def __repr__(self): 
        return f'<Song {self.id} | {self.title} | {self.artist} | {self.genre} | {self.url}>'