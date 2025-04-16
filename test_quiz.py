import pytest
from quiz import app as flask_app
import random

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-key-123"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    """Test that the index route returns a successful response"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form' in response.data  # Check if there's a form in the response

def test_index_session_variables(client):
    """Test that session variables are set correctly"""
    with client:
        response = client.get('/')
        assert 'correct_answer' in session
        assert 'num1' in session
        assert 'num2' in session
        assert 'operator' in session
        
        # Verify the calculation is correct
        num1 = session['num1']
        num2 = session['num2']
        operator = session['operator']
        
        if operator == '+':
            assert session['correct_answer'] == num1 + num2
        else:
            assert num1 >= num2  # Ensure no negative results
            assert session['correct_answer'] == num1 - num2

def test_check_correct_answer(client):
    """Test submitting a correct answer"""
    with client:
        # First get the index to set session variables
        client.get('/')
        
        # Get the correct answer from session
        correct_answer = session['correct_answer']
        
        # Submit the correct answer
        response = client.post('/check', data={'answer': correct_answer})
        
        assert response.status_code == 200
        assert b'Correct!' in response.data
        assert b'🎉' in response.data

def test_check_wrong_answer(client):
    """Test submitting a wrong answer"""
    with client:
        # First get the index to set session variables
        client.get('/')
        
        # Get the correct answer from session
        correct_answer = session['correct_answer']
        
        # Submit a wrong answer (just add 1 to correct answer)
        wrong_answer = correct_answer + 1
        response = client.post('/check', data={'answer': wrong_answer})
        
        assert response.status_code == 200
        assert b'Wrong!' in response.data
        assert str(correct_answer).encode() in response.data

def test_check_no_answer(client):
    """Test submitting without an answer"""
    response = client.post('/check', data={})
    assert response.status_code == 400  # Bad Request

def test_check_non_numeric_answer(client):
    """Test submitting a non-numeric answer"""
    response = client.post('/check', data={'answer': 'not a number'})
    assert response.status_code == 400  # Bad Request

# Helper to access session during tests
@pytest.fixture
def session(client):
    with client.session_transaction() as session:
        yield session
