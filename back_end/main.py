from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from db import logs_collection

app = Flask(__name__)
CORS(app)

#패스워드 평문이라 나중에 암호화 해야 함
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message":"누락"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message":"중복"}), 409

    new_user = User(username=username,password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "회원가입 완료"}), 201

@app.route('/login', methods=['POST'])
def login():
    data =  request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return jsonify({"message":"로그인 성공"}), 200
    else:
        return jsonify({"message": "로그인 실패"}), 401

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit

        total_logs = logs_collection.count_documents({})
        logs_cursor = logs_collection.find({}, {'_id': 0}).skip(skip).limit(limit)
        logs = list(logs_cursor)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)