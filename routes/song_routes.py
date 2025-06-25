from flask import Blueprint
from controllers.song_controller import create_song, get_all_songs, search_songs

song_bp = Blueprint('songs', __name__)

song_bp.route('/api/songs', methods=['POST'])(create_song)
song_bp.route('/api/songs', methods=['GET'])(get_all_songs)
song_bp.route('/api/search')(search_songs)