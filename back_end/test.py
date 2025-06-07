import unittest
import time
from api_main import api, socketio, robots, start_robot_threads
from flask_socketio import SocketIOTestClient


class RobotServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 로봇 상태 업데이트 쓰레드 실행 (한 번만)
        start_robot_threads()

    def setUp(self):
        self.client = api.test_client()
        self.socketio_client = socketio.test_client(api)

    def tearDown(self):
        self.socketio_client.disconnect()

    def test_get_robots(self):
        """GET /robots 요청이 로봇 목록을 반환해야 함"""
        response = self.client.get('/robots')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertIn("robotA", data)

    def test_update_robot_valid(self):
        """POST /update_robot: 유효한 로봇 ID로 상태 업데이트"""
        response = self.client.post('/update_robot', json={
            "robot_id": "robotA",
            "battery": 77,
            "route": "A#B"
        })
        self.assertEqual(response.status_code, 200)
        res = response.get_json()
        self.assertEqual(res['robot']['battery'], 77)
        self.assertEqual(res['robot']['route'], "A#B")

    def test_update_robot_partial(self):
        """POST /update_robot: 일부 필드만 업데이트 (예: route만)"""
        response = self.client.post('/update_robot', json={
            "robot_id": "robotB",
            "route": "Z#Y"
        })
        self.assertEqual(response.status_code, 200)
        updated = response.get_json()['robot']
        self.assertEqual(updated['route'], "Z#Y")
        self.assertEqual(updated['battery'], 70)  # 기존 값 유지

    def test_update_robot_invalid_id(self):
        """POST /update_robot: 잘못된 로봇 ID"""
        response = self.client.post('/update_robot', json={
            "robot_id": "robotX",
            "battery": 99
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_socket_connect_initial_events(self):
        """소켓 연결 시 초기 로봇 상태들을 수신하는지 확인"""
        events = self.socketio_client.get_received()
        robot_updates = [e for e in events if e['name'] == 'robot_status_update']
        self.assertGreaterEqual(len(robot_updates), len(robots))  # 최소 각 로봇 1개씩

    def test_socket_periodic_emit(self):
        """1초 간격 emit이 발생하는지 확인"""
        time.sleep(2.5)
        events = self.socketio_client.get_received()

        event_names = [e['name'] for e in events]
        self.assertIn('robot_status_update', event_names)
        self.assertIn('network', event_names)
        self.assertIn('network_mini', event_names)


if __name__ == '__main__':
    unittest.main()
