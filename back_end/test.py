import unittest
import time
from api_main import api, socketio, robots, start_robot_threads


class RobotServerTestCase(unittest.TestCase):

    def setUp(self):
        # 테스트용 클라이언트 생성
        self.client = api.test_client()
        self.socket_client = socketio.test_client(api)

        # 로봇 쓰레드 시작
        start_robot_threads()

    def tearDown(self):
        self.socket_client.disconnect()

    def test_get_robot_ids(self):
        """GET /robots: 전체 로봇 ID 리스트 반환"""
        response = self.client.get('/robots')
        self.assertEqual(response.status_code, 200)

        robot_ids = response.get_json()
        self.assertIsInstance(robot_ids, list)
        self.assertIn('robotA', robot_ids)

    def test_update_robot_valid(self):
        """POST /update_robot: 유효한 업데이트 요청"""
        payload = {
            "robot_id": "robotA",
            "battery": 80,
            "route": "A#B#C"
        }
        response = self.client.post('/update_robot', json=payload)
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertEqual(res_json["robot"]["battery"], 80)
        self.assertEqual(res_json["robot"]["route"], "A#B#C")

    
    


if __name__ == '__main__':
    unittest.main()
