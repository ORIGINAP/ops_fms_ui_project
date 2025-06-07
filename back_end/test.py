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

    def test_update_robot_partial_update(self):
        """POST /update_robot: 일부 필드만 업데이트 (battery 생략)"""
        payload = {
            "robot_id": "robotB",
            "route": "Z#Y"
        }
        response = self.client.post('/update_robot', json=payload)
        self.assertEqual(response.status_code, 200)
        updated = response.get_json()["robot"]
        self.assertEqual(updated["route"], "Z#Y")
        self.assertEqual(updated["battery"], 70)  # 기존 값 유지

    def test_update_robot_invalid_id(self):
        """POST /update_robot: 존재하지 않는 로봇 ID"""
        payload = {
            "robot_id": "invalid_robot",
            "battery": 90
        }
        response = self.client.post('/update_robot', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_socket_connect_initial_status(self):
        """소켓 연결 시 모든 로봇 상태 수신"""
        received = self.socket_client.get_received()
        status_events = [e for e in received if e['name'] == 'robot_status_update']
        self.assertGreaterEqual(len(status_events), len(robots))

    def test_socket_periodic_updates(self):
        """로봇 상태 업데이트 주기적 전송 테스트"""
        time.sleep(2)  # emit 대기 시간 확보
        events = self.socket_client.get_received()
        
        # 세 가지 이벤트 모두 포함되는지 확인
        names = [e['name'] for e in events]
        self.assertIn('robot_status_update', names)
        self.assertIn('network', names)
        self.assertIn('network_mini', names)
    
    


if __name__ == '__main__':
    unittest.main()
