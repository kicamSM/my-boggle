from unittest import TestCase, main

from flask import session

from boggle.app import app
from boggle.boggle import Boggle

app.config['TESTING'] = True
app.config['Debug_TB_HOSTS'] = ['dont-show-debug-toolbar']


class TestBoggle(TestCase):
    
    def setUp(self):
        """Test Preperation"""
        # with app.test_client() as client:  
        #     # client represents server and it has methods we can use 
        #     import pdb
        #     pdb.set_trace()
        #     # app.config["TESTING"] = True
        print("inside set up")
    
    # def test_display_start_page(self):
    def tearDown(self):
        print("inside tear down")
        
    def test_start_page(self):
        with app.test_client() as client: 
            res = client.get("/")
            self.assertIn("Welcome to Boggle", res.text)
            
        
    def test_display_boggle_board(self):
        with app.test_client() as client: 
            res = client.get('/boggle')
            self.assertIn("Score: 0", res.text)
            # checking for "Score: 0" in html 
            self.assertIn("High Score: 0", res.text)
            # checking for "High Score: 0" in html 
            self.assertIn("You have found valid 0 words", res.text)
            self.assertIn('board', session)
            # checking to see if board is in session
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("score"))
    
    def test_valid_word(self): 
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [['B', 'O', 'Y', 'X', 'N'], ['J', 'F', 'Z', 'X', 'B'], ['T', 'W', 'Q', 'U', 'A'], ['G', 'J', 'B', 'V', 'W'], ['V', 'T', 'S', 'M', 'W']]
        response = client.get('/check-word?word=boy')
        self.assertEqual(response.json['result'], 'ok')
    
    def test_invalid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [['B', 'O', 'Y', 'X', 'N'], ['J', 'F', 'Z', 'X', 'B'], ['T', 'W', 'Q', 'U', 'A'], ['G', 'J', 'B', 'V', 'W'], ['V', 'T', 'S', 'M', 'W']]
        response = client.get('/check-word?word=boq')
        self.assertEqual(response.json['result'], 'not-word')
        
    def test_word_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [['B', 'O', 'Y', 'X', 'N'], ['J', 'F', 'Z', 'X', 'B'], ['T', 'W', 'Q', 'U', 'A'], ['G', 'J', 'B', 'V', 'W'], ['V', 'T', 'S', 'M', 'W']]
        response = client.get('/check-word?word=tub')
        self.assertEqual(response.json['result'], 'not-on-board')
            
    def test_end_game(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 56
                sess["number_plays"] = 30
        res = client.get('/boggle')
        # note that you have to get the boggle html after you post the high score to session otherwise it will just think that the highscore was what you set originally i.e. 0
        self.assertIn("High Score: 56", res.text)
        self.assertIn("You have played 30 times", res.text)
    # def try_check_for_word(self):
        
    

    if __name__ == '__main__':
        main()
