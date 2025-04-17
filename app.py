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
    try:
        # Attempt to get the user answer and convert it to an integer
        user_answer = request.form.get('answer', type=int)
        
        if user_answer is None:  # Handle the case where the answer is missing
            raise ValueError("No answer provided")

        # Retrieve session data
        correct_answer = session.get('correct_answer')
        num1 = session.get('num1')
        num2 = session.get('num2')
        operator = session.get('operator')

        # Check for missing session data
        if correct_answer is None or num1 is None or num2 is None or operator is None:
            raise KeyError("Missing session data")

    except (ValueError, KeyError) as e:
        message = f"Error: {str(e)}"
        is_correct = False
        return render_template('result.html', message=message, is_correct=is_correct)

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        message = "Correct! 🎉"
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
