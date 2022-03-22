from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, DateField, FileField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import sqlite3

# Sukuriama aplikacijos konfigūracija
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(25)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)

# Sukuriamas ryšys su duomenų baze
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Prisijungimo sesijų valdymas
user_login = LoginManager()
user_login.init_app(app)
user_login.login_view = 'login'

# /////////////////////////////////////////////////////////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------
#                                              FORMŲ KLASĖS
# -----------------------------------------------------------------------------------------------------
# -- Prisijungimo forma
class LoginForm(FlaskForm):
    username = StringField('Prisijungimo vardas', validators=[InputRequired(), Length(max=25)])
    password = PasswordField('Slaptažodis', validators=[InputRequired(), Length(max=30)])
# -----------------------------------------------------------------------------------------------------
# -- Registracijos forma
class RegistrationForm(FlaskForm):
    first_name = StringField('Vardas', validators=[InputRequired(), Length(min=3, max=20)])
    last_name = StringField('Pavardė', validators=[InputRequired(), Length(min=3, max=20)])
    personal_code = StringField('Asmens kodas', validators=[InputRequired(), Length(min=11, max=11)])
    birthday = DateField('Gimimo data',  validators=[InputRequired()], format='%Y-%m-%d')
    email = StringField('El. pašto adresas', validators=[Email(message='Neteisingas el. pašto adresas'), Length(max=50)])
    phone = StringField('Telefono numeris', validators=[InputRequired(), Length(min=5)])
    password = PasswordField('Slaptažodis', validators=[InputRequired(), Length(min=8, max=50)])
# -----------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////////////////////////////////////////////////////////
# -----------------------------------------------------------------------------------------------------
#                                            NAUDOTOJŲ KLASĖS
# -----------------------------------------------------------------------------------------------------
# -- Paciento duomenų klasė
class Patient(db.Model, UserMixin):
    unique_id = db.Column(db.Integer, primary_key = True, unique = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    personal_code = db.Column(db.String(11))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(50))
# -----------------------------------------------------------------------------------------------------
# -- Gydytojo duomenų klasė
class Doctor(db.Model, UserMixin):
    unique_id = db.Column(db.Integer, primary_key = True, unique = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    position = db.Column(db.String(50))
    working_hours = db.Column(db.String(300))
    password = db.Column(db.String(50))
    image_url = db.Column(db.String(100))
# -----------------------------------------------------------------------------------------------------
# -- Sistemos administratoriaus duomenų klasė
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(50))
# -----------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////////////////////////////////////////////////////////

# Vartotojų sesijų paleidimas
@user_login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/informacija")
def info():
    return render_template('info.html')

@app.route("/kontaktai")
def contacts():
    return render_template('contacts.html')

@app.route("/prisijungimas")
def login():
    return render_template('login.html')

@app.route("/registracija")
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.debug = True
    app.run()