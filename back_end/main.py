from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

#패스워드 평문이라 나중에 암호화 해야 함
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"message":"모든 필드를 입력해주세요"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message":"이미 등록된 이메일입니다"}), 409
        
    if User.query.filter_by(username=username).first():
        return jsonify({"message":"이미 사용중인 아이디입니다"}), 409

    new_user = User(email=email, username=username, password=password)
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



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)