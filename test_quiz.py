import pytest
from quiz import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form' in response.data  # Check for form in response

def test_correct_answer(client):
    """Test submitting a correct answer"""
    # First request sets up the session
    client.get('/')
    
    # Get correct answer from session
    with client.session_transaction() as session:
        correct_answer = session['correct_answer']
    
    # Submit correct answer
    response = client.post('/check', data={'answer': correct_answer})
    assert b'Correct!' in response.data

def test_wrong_answer(client):
    """Test submitting a wrong answer"""
    client.get('/')
    
    with client.session_transaction() as session:
        wrong_answer = session['correct_answer'] + 1  # Guaranteed wrong answer
    
    response = client.post('/check', data={'answer': wrong_answer})
    assert b'Wrong!' in response.data
    assert str(wrong_answer - 1).encode() in response.data  # Shows correct answer

def test_no_answer(client):
    """Test submitting without an answer"""
    response = client.post('/check', data={})
    assert response.status_code == 400
