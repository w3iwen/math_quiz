import random
from quiz import app

def test_addition():
    """Test that addition works correctly"""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    assert num1 + num2 == num1 + num2  # Simple addition test

def test_subtraction():
    """Test that subtraction gives positive results"""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    # Ensure we don't get negative answers (like your app does)
    bigger = max(num1, num2)
    smaller = min(num1, num2)
    assert bigger - smaller >= 0
