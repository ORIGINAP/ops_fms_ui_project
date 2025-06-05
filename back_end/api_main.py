from flask import Flask, request,jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time


api = Flask(__name__)
CORS(api)  # 모든 출처 허용
socketio = SocketIO(api, cors_allowed_origins='*')

robots = {
    "robotA": {
        "name": "Robot-A",
        "version": "1.0",
        "velocity": "1",
        "battery": 100,
        "route": "A#B",
    },
    "robotB": {
        "name": "Robot-B",
        "version": "1.0",
        "velocity": "1",
        "battery": 70,
        "route": "B#C",
    },
    "robotC": {
        "name": "Robot-C",
        "version": "1.0",
        "velocity": "1",
        "battery": 90,
        "route": "C",
    },
    "robotD": {
        "name": "Robot-D",
        "version": "1.0",
        "velocity": "1",
        "battery":  10,
        "route": "D",
    }
}


def update_robot_status(robot_id):
    while True:
        state = robots[robot_id]
        state['battery'] = max(0, state['battery'] - 1)  # 배터리 감소
        socketio.emit('robot_status_update', {robot_id: state})
        print(f"Updated {robot_id} status: {state}")
        time.sleep(5)

@socketio.on('connect')
def handle_connect():
    for robot_id, state in robots.items():
        socketio.emit('robot_status_update', {robot_id: state})
    print('Client connected')

@api.route('/robotA', methods=['GET'])
def robotA():
    robot= {
        "name": "Robot-A",
        "version": "1.0",
        "velocity": "1",
        "battery": "100%",
        "route": "A#B",
    }
    return output(robot)
    
@api.route('/robotB', methods=['GET'])
def robotB():
    robot= {
        "name": "Robot-B",
        "version": "1.0",
        "velocity": "1",
        "battery": "70%",
        "route": "B#C",
    }
    return output(robot)

@api.route('/robotC', methods=['GET'])
def robotC():
    robot= {
        "name": "Robot-C",
        "version": "1.0",
        "velocity": "1",
        "battery": "90%",
        "route": "C",
    }
    return output(robot)

@api.route('/robotD', methods=['GET'])
def robotD():
    robot= {
        "name": "Robot-D",
        "version": "1.0",
        "velocity": "1",
        "battery": "10%",
        "route": "D",
    }
    return output(robot)

def output(robot):
    field = request.args.get('field', default='name', type=str)
    if field == 'name':
        return robot['name'], 200, {'Content-Type': 'text/plain'}
    elif field == 'version':
        return robot['version'], 200, {'Content-Type': 'text/plain'}
    elif field == 'description':
        return robot['description'], 200, {'Content-Type': 'text/plain'}
    elif field == 'robot':
        return robot, 200, {'Content-Type': 'application/json'}
    else:   
        return {"error": "Field not found"}, 404


if __name__ == '__main__':
    for robot_id in robots.keys():
        threading.Thread(target=update_robot_status, args=(robot_id,), daemon=True).start()
    socketio.run(api, debug=True, port=5002, host='0.0.0.0')
    api.run(debug=True, port=5001, host='0.0.0.0')