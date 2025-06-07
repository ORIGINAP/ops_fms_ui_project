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
        "velocity": 0.5,
        "battery": 100,
        "route": "A#B",
    },
    "robotB": {
        "name": "Robot-B",
        "version": "1.0",
        "velocity": 0.5,
        "battery": 70,
        "route": "B#C",
    },
    "robotC": {
        "name": "Robot-C",
        "version": "1.0",
        "velocity": 0.5,
        "battery": 90,
        "route": "C#A",
    },
    "robotD": {
        "name": "Robot-D",
        "version": "1.0",
        "velocity": 0.5,
        "battery":  10,
        "route": "A#B#C#D",
    }
}

def update_robot_status(robot_id):
    while True:
        state = robots[robot_id]
        state['battery'] = max(0, state['battery'] - 1)  # 배터리 감소
        socketio.emit('robot_status_update', {robot_id: state})
        print(f"Updated {robot_id} status: {state}")
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    for robot_id, state in robots.items():
        socketio.emit('robot_status_update', {robot_id: state})
    print('Client connected')

if __name__ == '__main__':
    for robot_id in robots.keys():
        threading.Thread(target=update_robot_status, args=(robot_id,), daemon=True).start()
    socketio.run(api, debug=True, port=5002, host='0.0.0.0')