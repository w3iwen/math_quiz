# test_quiz.py
import pytest
from quiz import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_index_route(client):
    """Test that the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'form' in response.data.lower()  # Check for form element

def test_session_variables(client):
    """Test that session variables are set correctly"""
    with client:
        client.get('/')
        assert 'num1' in session
        assert 'num2' in session
        assert 'operator' in session
        assert 'correct_answer' in session

def test_calculation_logic(client):
    """Test the math logic works correctly"""
    with client:
        client.get('/')
        num1 = session['num1']
        num2 = session['num2']
        operator = session['operator']
        
        if operator == '+':
            assert session['correct_answer'] == num1 + num2
        else:
            assert session['correct_answer'] == max(num1, num2) - min(num1, num2)

# Helper to access session during tests
@pytest.fixture(autouse=True)
def session(client):
    with client.session_transaction() as sess:
        yield sess
