from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(80), unique=True, nullable=False)
    pw = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return "hi"

if __name__ == '__main__':
    app.run(debug=True)