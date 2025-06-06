from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'shit'

#패스워드 평문이라 나중에 암호화 해야 함
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20), unique=True)


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
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({"message":"로그인 성공"}), 200
    else:
        return jsonify({"message": "로그인 실패"}), 401

@app.route('/me')
def me():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username
        }), 200

""" @app.route('/update-profile', methods=['POST'])
def update_profile():
    data =  request.get_json()
    new_username = data.get('username')
    new_email """
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)