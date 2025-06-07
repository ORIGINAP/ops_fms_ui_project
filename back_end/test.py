import unittest
import time
from api_main import api, socketio, robots, start_robot_threads
from flask_socketio import SocketIOTestClient


class RobotServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_robot_threads()

    def setUp(self):
        self.client = api.test_client()
        self.socketio_client = socketio.test_client(api)

    def tearDown(self):
        self.socketio_client.disconnect()

    def test_get_robots(self):
        """GET /robots: 모든 로봇 ID 반환"""
        res = self.client.get('/robots')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, list)
        self.assertIn("robotA", data)

    def test_update_robot_valid(self):
        """정상적인 로봇 업데이트"""
        res = self.client.post('/update_robot', json={
            "robot_id": "robotA",
            "battery": 88,
            "route": "A#B#C"
        })
        self.assertEqual(res.status_code, 200)
        updated = res.get_json()['robot']
        self.assertEqual(updated["battery"], 88)
        self.assertEqual(updated["route"], "A#B#C")

    def test_update_robot_partial(self):
        """배터리는 유지하고 경로만 업데이트"""
        old_battery = robots["robotB"]["battery"]

        res = self.client.post('/update_robot', json={
            "robot_id": "robotB",
            "route": "B#C#D"
        })
        self.assertEqual(res.status_code, 200)
        robot = res.get_json()['robot']
        self.assertEqual(robot['route'], "B#C#D")
        self.assertEqual(robot['battery'], old_battery)

    def test_update_robot_invalid_id(self):
        """존재하지 않는 로봇 ID로 요청"""
        res = self.client.post('/update_robot', json={
            "robot_id": "robotZ",
            "battery": 100
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_socket_connect_initial_events(self):
        """소켓 연결 시 모든 로봇 상태 수신 확인"""
        events = self.socketio_client.get_received()
        status_events = [e for e in events if e['name'] == 'robot_status_update']
        self.assertGreaterEqual(len(status_events), len(robots))

    def test_socket_periodic_emit(self):
        """1초마다 상태 emit이 오는지 확인"""
        time.sleep(2.5)
        events = self.socketio_client.get_received()
        names = [e['name'] for e in events]
        self.assertIn('robot_status_update', names)
        self.assertIn('network', names)
        self.assertIn('network_mini', names)


if __name__ == '__main__':
    unittest.main()
