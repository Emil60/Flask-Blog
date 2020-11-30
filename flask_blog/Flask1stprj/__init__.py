from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Text
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY']="something"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbase.db'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'fakefake1478@gmail.com',
    MAIL_PASSWORD = 'fake01012020'
)

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from Flask1stprj import routes