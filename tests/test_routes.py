import unittest
from app import app
from models.db import db

class BasicRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = postgresql://music_user:tqkBfrBNKZPN3ATdLgKDczKTzq92thMQ@dpg-d1elqommcj7s73eghevg-a/music_player_db_6x7x

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_home_route(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Music Player Backend", res.data)

if __name__ == "__main__":
    unittest.main()
