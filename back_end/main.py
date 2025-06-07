from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from db import logs_collection

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'shit'

#패스워드 평문이라 나중에 암호화 해야 함
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)

    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message":"누락"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message":"중복"}), 409

    new_user = User(email=email,password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "회원가입 완료"}), 201

@app.route('/login', methods=['POST'])
def login():
    data =  request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session['user_id'] = user.id
        session['username'] = user.username
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

        return jsonify({
            'logs': logs,
            'total': total_logs,
            'page': page,
            'limit': limit
        })
    except Exception as e:
        return jsonify({'message': '서버 오류', 'error': str(e)}), 500
@app.route('/me')
def me():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username
        }), 200

@app.route('/update-profile', methods=['POST'])
def update_profile():
    data =  request.get_json()
    new_username = data.get('username')
    new_email = data.get('email')
    new_phone = data.get('phone')
    
    user = User.query.get(1)
    
    if not user:
        return jsonify({'message': '사용자 없음'}), 404
    
    if new_username:
        user.username = new_username
    if new_email:
        user.email = new_email
    if new_phone:
        user.phone = new_phone

    db.session.commit()

    return jsonify({'message': '프로필 수정 완료'})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)