from flask import Flask, g, jsonify, request, Response
import sqlite3
import requests

from myviews import requestviews, defaultviews, dbviews

app = Flask(__name__)
app.register_blueprint(requestviews.request_bp)
app.register_blueprint(defaultviews.default_bp)
app.register_blueprint(dbviews.db_bp)

# DB functions
DATABASE = 'mymodule/dbmodule/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("new db connection")
    else:
        print("db connection")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print("db close")
        db.close()

# initialize
with app.app_context():
  print("db init")
  dbviews.init_db()
