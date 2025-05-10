import unittest
from datetime import datetime
from app import create_app, db
from app.models import Score, User


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            user = User(userName='TestUser')
            db.session.add(user)
            score = Score(name='Alice', score=100, dateSubmitted=datetime.utcnow())
            db.session.add(score)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_submit_form_get(self):
        response = self.client.get('/submit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit', response.data)

    def test_submit_score_post_valid(self):
        response = self.client.post('/submit', data={
            'name': 'Bob',
            'score': '150'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leaderboard', response.data)

    def test_submit_score_post_invalid(self):
        response = self.client.post('/submit', data={}, follow_redirects=True)
        self.assertIn(b'Submit', response.data)

    def test_get_scores_api(self):
        response = self.client.get('/api/scores')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.data)

    def test_add_score_api(self):
        response = self.client.post('/api/scores', json={
            'name': 'Charlie',
            'score': 200
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Score added!', response.data)

    def test_add_score_api_invalid(self):
        response = self.client.post('/api/scores', json={})
        self.assertEqual(response.status_code, 400)

    def test_add_user_get(self):
        response = self.client.get('/add_user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username', response.data)

    def test_leaderboard_page(self):
        response = self.client.get('/leaderboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.data)


if __name__ == '__main__':
    unittest.main()
