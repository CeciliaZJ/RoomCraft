from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = []  # simple in-memory "database"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    # This is your Python logic for handling the login form
    email = request.form['email']
    password = request.form['password']
    users.append({'email': email, 'password': password})
    return redirect(url_for('home'))

@app.route('/craft')
def craft():
    return render_template('craft.html')

if __name__ == '__main__':
    app.run(debug=True)
