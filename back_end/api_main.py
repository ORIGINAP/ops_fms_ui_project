from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
import random  # ✅ 네트워크 상태용 랜덤값

# Flask 앱 및 소켓 설정
api = Flask(__name__)
CORS(api, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:5173"}})
socketio = SocketIO(api, cors_allowed_origins='*')

# 로봇 상태 정의 (배터리, 속도, 경로, 네트워크 상태 포함)
robots = {
    "robotA": {
        "name": "Robot-A",
        "version": "1.0",
        "velocity": 0.5,
        "battery": 100,
        "route": "A",
        "network": 50  # ✅ 네트워크 상태
    },
    "robotB": {
        "name": "Robot-B",
        "version": "1.0",
        "velocity": 1,
        "battery": 70,
        "route": "B#C",
        "network": 50
    },
    "robotC": {
        "name": "Robot-C",
        "version": "1.0",
        "velocity": 0.8,
        "battery": 90,
        "route": "C#A",
        "network": 50
    },
    "robotD": {
        "name": "Robot-D",
        "version": "1.0",
        "velocity": 0.6,
        "battery": 100,
        "route": "A#B#D",
        "network": 50
    },
    "robotE": {
        "name": "Robot-E",
        "version": "1.0",
        "velocity": 1.2,
        "battery": 100,
        "route": "C",
        "network": 50
    },
    "robotF": {
        "name": "Robot-F",
        "version": "1.0",
        "velocity": 0.9,
        "battery": 100,
        "route": "B#C#D",
        "network": 50
    },
    "robotG": {
        "name": "Robot-G",
        "version": "1.0",
        "velocity": 0.7,
        "battery": 100,
        "route": "A#B#C#D",
        "network": 50
    }
}

# 로봇 상태를 주기적으로 업데이트하는 함수
def update_robot_status(robot_id):
    while True:
        state = robots[robot_id]

        # 🔋 배터리 감소
        state['battery'] = max(0, state['battery'] - 1)

        # 📶 네트워크 상태를 랜덤하게 변경 (70~100)
        state['network'] = random.randint(30, 70)

        # 클라이언트에게 현재 상태 전송
        socketio.emit('robot_status_update', {robot_id: state})
        print(f"✅ Updated {robot_id} status: {state}")

        # 간단한 구조로 네트워크 송출
        socketio.emit('network_mini', state['network'])

        # 네트워크 상태도 robot_id와 함께 전송
        socketio.emit('network', {robot_id: state['network']})
        time.sleep(1)

# 클라이언트가 연결되었을 때 현재 모든 로봇 상태 전송
@socketio.on('connect')
def handle_connect():
    print('🌐 Client connected')
    for robot_id, state in robots.items():
        socketio.emit('robot_status_update', {robot_id: state})


def start_robot_threads():
    for robot_id in robots.keys():
        threading.Thread(target=update_robot_status, args=(robot_id,), daemon=True).start()


@api.route('/update_robot', methods=['POST'])
def update_robot():
    data = request.get_json()
    robot_id = data.get("robot_id")
    new_battery = data.get("battery")
    new_route = data.get("route")

    if robot_id not in robots:
        return jsonify({"error": "Invalid robot ID"}), 400

    # 값이 전달되었을 때만 업데이트
    if new_battery is not None:
        robots[robot_id]["battery"] = int(new_battery)

    if new_route is not None:
        robots[robot_id]["route"] = new_route

    # 클라이언트들에게 업데이트 전송
    socketio.emit('robot_status_update', {robot_id: robots[robot_id]})
    socketio.emit('network', {robot_id: robots[robot_id]["network"]})

    return jsonify({"message": "Robot updated", "robot": robots[robot_id]})


# 서버 실행
if __name__ == '__main__':
    start_robot_threads()
    socketio.run(api, debug=True, port=5002, host='0.0.0.0')

