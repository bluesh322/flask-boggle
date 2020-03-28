from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Set up before running each test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_homepage(self):
        """Check information in the session and html is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<h3>Highscore:', response.data)
            self.assertIn(b'<h3>Plays:', response.data)
            self.assertIn(b'<h3>Timer:', response.data)

    def test_valid_word(self):
        """Test if word is valid with modified board"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['res'], 'ok')
    
    def test_invalid_word(self):
        """Test if word is in the dictionary, but can't be on board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['res'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board but not a word"""

        self.client.get('/')
        response = self.client.get('/check-word?word=abcdef')
        self.assertEqual(response.json['res'], 'not-word')