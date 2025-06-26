from models.db import db

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    album_cover = db.Column(db.String(255))  # 🔁 Replaced genre
    url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album_cover": self.album_cover,
            "url": self.url,
            "user_id": self.user_id
        }
