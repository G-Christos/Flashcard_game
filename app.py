from flask import Flask, render_template, url_for, redirect, Blueprint, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
# from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os, random

app = Flask(__name__) # package that contain the application, new app
db = SQLAlchemy(app) # create database instance
bcrypt = Bcrypt(app)
# import database //// --> absolute path VS /// --> relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' # 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False,   # default="male" check(gender in ('Female', 'Male', 'Other'))
    age = db.Column(db.Integer, nullable=False)
    date_signup = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route('/') # route decorator
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = bcrypt.generate_password_hash(password) # 1st appr.
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password): # 1st appr.
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    login_user(user, remember=remember)
    return redirect(url_for('dashboard'))

#### built the game here ####
bag_of_words = {
    'die Anmerkung': 'simeiosi',
    'die Auflage': 'stroma',
    'die Aufklärung': 'eksigisi',
    'aufschreiben - notieren': 'simeiono',
    'die Dichtung': 'poiisi',
    'die Reinheit': 'agnotita',
    'derentwillen': 'eksaitias tis thelisis tous',
    'die Neigung - Vorliebe': 'protimisi',
    'die Poesie': 'poiisi',
    'umstritten': 'epimaxos',
    'die Grausamkeit': 'thiriodia'
}
current_word = ''
current_word_translation = ''

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    global current_word, current_word_translation
    if request.method == 'POST':
        answer = request.form['answer']
        if answer.lower() == current_word_translation.lower():
            result = 'Correct!'
        else:
            result = 'Wrong! The correct answer is "{}".'.format(current_word_translation)
        current_word, current_word_translation = random.choice(list(bag_of_words.items()))
        return render_template('dashboard.html', word=current_word, result=result)
    else:
        current_word, current_word_translation = random.choice(list(bag_of_words.items()))
        return render_template('dashboard.html', word=current_word)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@ app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@ app.route('/signup')
def signup():
    return render_template('signup.html')

@ app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists.')
        return redirect(url_for('login')) # signup
    hashed_password = bcrypt.generate_password_hash(password) # 1st appr.
    new_user = User(email=email, name=name, password=hashed_password) # 1st appr.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    flash('New account created successfully! Please login.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

## Open terminal ##
# conda activate projects && cd C:\Users\chris\Downloads\flashcard_game && python app.py
# http://127.0.0.1:5000/

# sqlite3 db.sqlite3
# select * from user;

