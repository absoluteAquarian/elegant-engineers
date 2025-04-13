import unittest
from app import create_app, db
from app.models import Score, User, Leaderboard
from datetime import datetime
from io import BytesIO
import json

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')  # Use the 'testing' config
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        db.create_all()

    def tearDown(self):
        """Tear down the database after each test."""
        db.session.remove()
        db.drop_all()

    def test_submit_score(self):
        """Test that submitting a score adds a score to the database."""
        response = self.client.post('/submit', data=dict(
            name='Test User',
            score=500,
            file=(BytesIO(b"fake image data"), 'test_image.png')
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'leaderboard', response.data)  # Should redirect to leaderboard

        # Check if the score was added to the database
        score = Score.query.filter_by(name='Test User').first()
        self.assertIsNotNone(score)
        self.assertEqual(score.score, 500)

    def test_leaderboard_page(self):
        """Test that the leaderboard page displays correctly."""
        # Insert test data into the database
        test_score = Score(name='Test User', score=100, dateSubmitted=datetime.utcnow(), imageUrl='http://example.com')
        db.session.add(test_score)
        db.session.commit()

        # Request the leaderboard page
        response = self.client.get('/leaderboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leaderboard', response.data)
        self.assertIn(b'Test User', response.data)
        self.assertIn(b'100', response.data)

    def test_add_user(self):
        """Test that adding a user works correctly."""
        response = self.client.post('/add_user', data=dict(username='new_user'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'new_user', response.data)

        # Check that the user is in the database
        user = User.query.filter_by(userName='new_user').first()
        self.assertIsNotNone(user)

    def test_api_scores(self):
        """Test the API for fetching scores."""
        # Add test scores to the database
        test_scores = [
            Score(name='User 1', score=100, dateSubmitted=datetime.utcnow(), imageUrl='http://example.com'),
            Score(name='User 2', score=250, dateSubmitted=datetime.utcnow(), imageUrl='http://example.com'),
            Score(name='User 3', score=150, dateSubmitted=datetime.utcnow(), imageUrl='http://example.com'),
        ]
        db.session.add_all(test_scores)
        db.session.commit()

        # Test the API route to get scores
        response = self.client.get('/api/scores')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('scores', data)
        self.assertEqual(len(data['scores']), 3)  # We added 3 scores

        # Check if the scores are sorted in descending order
        scores = [score['score'] for score in data['scores']]
        self.assertEqual(sorted(scores, reverse=True), scores)

    def test_api_add_score(self):
        """Test adding a score via the API."""
        response = self.client.post('/api/scores', json=dict(
            name='API User',
            score=300
        ))

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Score added!')

        # Verify that the score was added to the database
        score = Score.query.filter_by(name='API User').first()
        self.assertIsNotNone(score)
        self.assertEqual(score.score, 300)

    def test_invalid_api_score_submission(self):
        """Test submitting invalid data to the API (missing score)."""
        response = self.client.post('/api/scores', json=dict(name='Invalid User'))
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid data')

    def test_submit_invalid_score(self):
        """Test submitting invalid data through the score form."""
        response = self.client.post('/submit', data=dict(
            name='Test User',
            score='invalid_score'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'leaderboard', response.data)

        # Ensure no score was added to the database
        score = Score.query.filter_by(name='Test User').first()
        self.assertIsNone(score)

    def test_index_page(self):
        """Test the index page (home page) renders properly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leaderboard', response.data)  # Ensure leaderboard is in the page content

    def test_add_user_invalid_post(self):
        """Test that submitting an empty username fails."""
        response = self.client.post('/add_user', data=dict(username=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username is required', response.data)

    def test_add_user_existing(self):
        """Test adding a user that already exists."""
        user = User(userName='existing_user')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/add_user', data=dict(username='existing_user'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exists', response.data)

    def test_upload_to_imgur(self):
        """Test the upload to Imgur functionality."""
        # This requires mocking the Imgur API to test without actual network calls.
        # You can use libraries like `unittest.mock` or `responses` to mock external requests.

        # For now, let's simulate the behavior of Imgur API.
        with unittest.mock.patch('app.routes.requests.post') as mocked_post:
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = {'data': {'link': 'http://fakeimage.com'}}
            
            with open('fake_image.png', 'rb') as f:
                image_url = upload_to_imgur(f)
                self.assertEqual(image_url, 'http://fakeimage.com')

    def test_leaderboard_data_insertion(self):
        """Test the correct insertion of leaderboard data in the database."""
        leaderboard_entry = Leaderboard(userId=1, userRank=1, userTopRank=1)
        db.session.add(leaderboard_entry)
        db.session.commit()

        # Check if the leaderboard entry exists in the database
        leaderboard = Leaderboard.query.filter_by(userId=1).first()
        self.assertIsNotNone(leaderboard)
        self.assertEqual(leaderboard.userRank, 1)
        self.assertEqual(leaderboard.userTopRank, 1)

if __name__ == '__main__':
    unittest.main()
