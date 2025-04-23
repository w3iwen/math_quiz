# test_quiz.py
import pytest
from app import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-key-123'  
    return app.test_client()

def test_index_route(client):
    """Test the home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'form' in response.data.lower()

def test_answer_submission(client):
    """Test answer submission flow"""
    # First request to set up session
    client.get('/')
    
    # Get the correct answer from session
    with client.session_transaction() as sess:
        correct_answer = sess['correct_answer']
        test_answer = correct_answer + 1  # Wrong answer
    
    # Test correct answer
    response = client.post('/check', data={'answer': str(correct_answer)})
    assert b'Invalid!' in response.data
    
    # Test wrong answer
    response = client.post('/check', data={'answer': str(test_answer)})
    assert b'Wrong!' in response.data
