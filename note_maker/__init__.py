from flask import Flask
from waitress import serve
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# creation of sqlalchemy session and db engine
engine = create_engine(f'sqlite:///{BASE_DIR}/db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

from note_maker import urls

def run():
    app.run(debug=True)
    #serve(app, port=5000, host='0.0.0.0')
   