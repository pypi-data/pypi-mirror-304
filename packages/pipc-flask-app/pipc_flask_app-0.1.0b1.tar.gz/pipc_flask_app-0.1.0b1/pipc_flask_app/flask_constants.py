# FLASK APP TEMPLATE =========================================================

import os
import time
from pipcreator.constants import tic
from textPlay.colors import *

# FLASK APP TEMPLATE
def flask_structure(project_name, test=False, framework='advanced'):
    if framework in  ["react", "next", "vite", 'others']:
        framework = 'Frameworks'
    if test and framework == 'Advanced':
        flask_app = f'''
{project_name}/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── layout.html
│       └── home.html
│
├── config.py
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
├── venv/
├── instance/
│   └── config.py
├── migrations/
├── tests/
│   ├── test_basic.py
│   └── conftest.py
└── .env or .flaskenv
'''
    elif not test and framework == 'Advanced':
        flask_app = f'''
{project_name}/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── layout.html
│       └── home.html
│
├── config.py
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
├── venv/
├── instance/
│   └── config.py
├── migrations/
└── .env or .flaskenv
'''
    elif test and framework == 'Basic':
        flask_app = f'''
{project_name}/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
├── templates/
│   ├── layout.html
│   └── home.html
├── test/
│   ├── test_basic.py
│   └── conftest.py
├── venv/
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
'''

    elif not test and framework == 'Basic':
        flask_app = f'''
{project_name}/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
├── templates/
│   ├── layout.html
│   └── home.html
├── venv/
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
'''
    elif test and framework == 'Frameworks':
        flask_app = f'''
{project_name}/
│
├── client/
│   └── <framework>/
│ 
├── server/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── layout.html
│       └── home.html
├── tests/
│   ├── test_basic.py
│   └── conftest.py
├── venv/
├── config.py
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
'''
    elif not test and framework == 'Frameworks':
        flask_app = f'''
{project_name}/
│
├── client/
│   └── <framework>/
│ 
├── server/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── layout.html
│       └── home.html
│
├── venv/
├── config.py
├── README.md
├── run.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
'''
    else:
        flask_app = " "
    return flask_app



# app/__init__.py
app_init = '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load the configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Import and register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
'''

# app/routes.py
app_routes = '''
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

'''

# app/models.py
app_models = '''
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

'''

# app/forms.py
app_forms = '''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

'''

# app/static/css/style.css
app_static_css = '''
* {
  box-sizing: border-box;
  margin: 0;
}
body {
  background: #222222;
}

.desktop-1 {
    display: flex;
    justify-content: center; /* Horizontal centering */
    align-items: center;    /* Vertical centering */
    height: 100vh;
    padding: 20px;
}
.content {
  display: flex;
  flex-direction: column;
  gap: 82px;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}
.logos {
  display: flex;
  flex-direction: row;
  gap: 50px;
  align-items: center;
  justify-content: center;
  align-self: stretch;
  flex-shrink: 0;
  position: relative;
  flex-wrap: wrap;
}

.logo {
  flex-shrink: 0;
  width: 135px;
  height: 135px;
  position: relative;
  transition: all 0.5s ease-in-out;
}
.logo:hover{
    transform: scale(1.1);
  filter: drop-shadow(0 0 50px rgba(255, 255, 255, 0.5));
    }

.title {
  color: #ffffff;
  text-align: center;
  font-family: "Inter-Bold", sans-serif;
  font-size: 38px;
  line-height: 39px;
  font-weight: 700;
  position: relative;
  align-self: stretch;
}
.counter {
  display: flex;
  flex-direction: column;
  gap: 64px;
  align-items: center;
  justify-content: center;
  align-self: stretch;
  flex-shrink: 0;
  position: relative;
}
.count {
  border-radius: 13px;
  border-style: solid;
  background-color: #222222;
  border-color: #ffffff;
  border-width: 1px;
  padding: 0px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex-shrink: 0;
  position: relative;
  transition: all 0.5s ease-in-out;
}
.count:hover {
    filter: drop-shadow(0 0 9px rgba(225, 210, 66, 0.5));
    border-color: rgba(225, 210, 66, 0.5);
    
}
.counter2 {
    border-radius: 13px;
  color: #ffffff;
  background-color: #1a1a1a;
  border: none;
  padding: 15px 20px 15px 20px;
  text-align: left;
  font-family: "Inter-Regular", sans-serif;
  font-size: 20px;
  line-height: 19px;
  font-weight: 400;
  position: relative;
  cursor: pointer;
}


.small-text {
  color: #ffffff80;
  text-align: center;
  font-family: "Inter-Regular", sans-serif;
  font-size: 18px;
  line-height: 19px;
  position: relative;
  align-self: stretch;
}
'''

# app/static/js/script.js
app_static_js = '''
let count = 0;
const button = document.getElementById('countup');

button.addEventListener('click', () => {
  count++;
  button.textContent = `Count is ${count}`;
});
'''

# app/templates/layout.html
app_template_layout = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>PipCreator + Flask</title>
</head>
<body>
        {% block content %}{% endblock %}
</body>
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
</html>
'''

# app/templates/home.html
app_template_home = '''
{% extends 'layout.html' %}

{% block content %}
    <div class="desktop-1">
        <div class="content">
          <div class="logos">
            <a href="https://pypi.org/project/pipcreator/" target="_blank">
            <img class="logo" src="{{ url_for('static', filename='images/logoDark.svg') }}" />
            </a>
            <a href="https://flask.palletsprojects.com/" target="_blank">
            <img class="logo" src="{{ url_for('static', filename='images/flask.svg') }}" />
            </a>
          </div>
          <div class="title">PipCreator + Flask</div>
          <div class="counter">
            <div class="count">
                <button id="countup" class="counter2">Count is 0</button>
            </div>
            <div class="small-text">
              Click on the PipCreator and Flask logos to learn more
            </div>
          </div>
        </div>
      </div>
{% endblock %}
'''

# config.py
config = '''
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''

# run.py
run = '''
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

'''

# requirements.txt
flask_requirements = "Flask==2.3.2 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4 Flask-WTF==1.0.1 pytest python-dotenv"

# instance/config.py
instance_config = '''
# This is used for instance-specific configuration
# Do not add this file to version control
SECRET_KEY = 'instance-specific-secret-key'
'''

# tests/test_basic.py
test_basic = '''
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home Page' in response.data

'''

# tests/conftest.py
tests_conftest = '''
# This file can be used to define common test configurations
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def new_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(new_app):
    return new_app.test_client()

@pytest.fixture(scope='module')
def init_database(new_app):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
'''

# .flaskenv
flask_env = '''
FLASK_APP=app.py
FLASK_ENV=development
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0
'''

# Basic Flask App =========================================================
basic_flask_app = '''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title='Home')

if __name__ == '__main__':
    app.run(debug=True)

'''
