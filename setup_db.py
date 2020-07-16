"""This script sets up a Postgres data base.

Run this code once on the server after you upload your app.

If you change your db structure you can run this code again but
remember that it will drop all existing tables.
"""

from app import app
from db import db

# initialize application to work with SQLAlchemy
# does not bind SQLAlchemy object to application
db.init_app(app)

# setup an application context to work outside a Flask view function
with app.app_context():
    db.drop_all()
    db.create_all()
