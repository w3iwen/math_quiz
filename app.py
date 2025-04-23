from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'temporary-dev-key-123'  # Needed for session

@app.route('/')
def index():
    # Generate two random numbers between 1 and 20
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    
    # Randomly choose between addition and subtraction
    operator = random.choice(['+', '-'])
    
    # Calculate the correct answer
    if operator == '+':
        correct_answer = num1 + num2
    else:
        # Ensure we don't get negative answers for subtraction
        num1, num2 = max(num1, num2), min(num1, num2)
        correct_answer = num1 - num2
    
    # Store the correct answer in the session
    session['correct_answer'] = correct_answer
    session['num1'] = num1
    session['num2'] = num2
    session['operator'] = operator
    
    return render_template('index.html', num1=num1, num2=num2, operator=operator)

@app.route('/check', methods=['POST'])
def check():
    user_answer = request.form.get('answer', type=int)
    correct_answer = session.get('correct_answer', 0)
    
    # Get the numbers and operator for displaying the question again
    num1 = session.get('num1', 0)
    num2 = session.get('num2', 0)
    operator = session.get('operator', '+')
    
    if user_answer == correct_answer:
        message = "Correct!"
        is_correct = True
    else:
        message = f"Wrong! The correct answer was {correct_answer}. Try again!"
        is_correct = False
    
    return render_template('result.html', 
                         message=message, 
                         is_correct=is_correct,
                         num1=num1,
                         num2=num2,
                         operator=operator)

if __name__ == '__main__':
    app.run(debug=True)
