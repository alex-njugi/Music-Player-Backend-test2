from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Song
from utils.cloudinary import upload_mp3


@jwt_required()
def create_song():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    title = request.form.get('title')
    artist = request.form.get('artist')
    genre = request.form.get('genre')

    if not file or not title or not artist or not genre:
        return jsonify({"error": "Missing required fields"}), 400

  
    try:
        url = upload_mp3(file)
    except Exception as e:
        return jsonify({"error": "Upload failed", "details": str(e)}), 500
    
    user_id = get_jwt_identity()

    song = Song(title=title, artist=artist, genre=genre, url=url, user_id=user_id)
    db.session.add(song)
    db.session.commit()

    return jsonify({
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "url": song.url,
        "user_id": song.user_id
    }), 201


def get_all_songs():
    songs = Song.query.all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "artist": s.artist,
            "genre": s.genre,
            "url": s.url,
            "user_id": s.user_id
        }
        for s in songs
    ]), 200


def search_songs():
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify([]), 200

    songs = Song.query.filter(
        (Song.title.ilike(f'%{q}%')) | (Song.artist.ilike(f'%{q}%'))
    ).all()

    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "artist": s.artist,
            "genre": s.genre,
            "url": s.url,
            "user_id": s.user_id
        }
        for s in songs
    ]), 200