from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded user credentials for testing
correct_email = "testing@email.com"
correct_password = "2024"

# Serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')  # Replace this with the path to your HTML file

# Handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email and password match the correct values
    if email == correct_email and password == correct_password:
        return redirect(url_for('welcome'))  # Redirect to a welcome page on success
    else:
        return "Invalid credentials", 401  # Return an error message on failure

@app.route('/welcome')
def welcome():
    return "<h1>Welcome to the Healthcare Chatbot!</h1>"  # This is where a successful login will redirect

if __name__ == '__main__':
    app.run(debug=True)

