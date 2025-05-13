from flask import Flask, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key in production

# MongoDB connection
client = MongoClient('mongodb://mongodb:27017/')
db = client['user_db']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    
    user = users_collection.find_one({'username': username})
    
    if user and bcrypt.checkpw(password, user['password']):
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        # Check if user already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        # Hash password and store user
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({
            'username': username,
            'password': hashed_password
        })
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)