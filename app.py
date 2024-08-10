from flask import Flask, g
import sqlite3
import dbviews
import chatbotviews

# register views
app = Flask(__name__)
app.register_blueprint(dbviews.db_bp)
app.register_blueprint(chatbotviews.chat_bp)

# DB connection
DATABASE = 'dbmodule/database.db'

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

@app.route('/')
def home():
  return 'Hello, this is the home page!'