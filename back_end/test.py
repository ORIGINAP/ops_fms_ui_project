import unittest
import time
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient
from api_main import api, socketio, robots, start_robot_threads


class RobotAPITestCase(unittest.TestCase):

    def setUp(self):
        # 테스트 중에도 로봇 상태 쓰레드가 실행되도록 설정
        start_robot_threads()

        # HTTP 및 SocketIO 클라이언트 초기화
        self.client: FlaskClient = api.test_client()
        self.socketio_client: SocketIOTestClient = socketio.test_client(api)

    def test_robots_have_required_fields(self):
        """각 로봇이 필수 키값을 포함하는지 확인"""
        self.assertGreaterEqual(len(robots), 1)
        for robot_id, state in robots.items():
            with self.subTest(robot=robot_id):
                self.assertIn("battery", state)
                self.assertIn("velocity", state)
                self.assertIn("route", state)
                self.assertIn("network", state)

    def test_network_range(self):
        """네트워크 상태가 정상 범위인지 확인 (0~100)"""
        for robot_id, state in robots.items():
            with self.subTest(robot=robot_id):
                self.assertGreaterEqual(state["network"], 0)
                self.assertLessEqual(state["network"], 100)

    def test_socketio_connect(self):
        """SocketIO 연결 확인"""
        self.assertTrue(self.socketio_client.is_connected())

    def test_socketio_robot_status_update_event(self):
        """서버에서 로봇 상태 이벤트를 emit하는지 확인"""
        time.sleep(1.5)  # 로봇 쓰레드가 emit할 시간 확보

        received = self.socketio_client.get_received()
        update_events = [e for e in received if e['name'] == 'robot_status_update']

        self.assertTrue(
            len(update_events) > 0,
            "robot_status_update 이벤트를 수신하지 못했습니다."
        )

    def tearDown(self):
        self.socketio_client.disconnect()


if __name__ == '__main__':
    unittest.main()
