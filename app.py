from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRES_URI)
db = SQLAlchemy(app)


