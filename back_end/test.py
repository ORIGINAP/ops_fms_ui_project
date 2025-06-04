from flask import Flask,request

api = Flask(__name__)

@api.route('/robot', methods=['GET'])
def robot():
    robot= {
        "name": "Robot",
        "version": "1.0",
        "description": "This is a robot API",
    }
    return robot, 200, {"Content-Type": "application/json"}

if __name__ == '__main__':
    api.run(debug=True, port=5000)