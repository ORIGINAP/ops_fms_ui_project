import unittest
from main import app, db, User


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

        db.create_all()

        # 기본 유저 등록
        self.default_user = {
            "email": "test@example.com",
            "password": "pass123"
        }
        self.app.post('/register', json=self.default_user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_success(self):
        res = self.app.post('/register', json={
            "email": "new@example.com",
            "password": "newpass"
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn("회원가입 완료", res.get_json()["message"])

    def test_register_missing_fields(self):
        res = self.app.post('/register', json={
            "email": ""
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("누락", res.get_json()["message"])

    def test_register_duplicate_email(self):
        res = self.app.post('/register', json={
            "email": self.default_user["email"],
            "password": "otherpass"
        })
        self.assertEqual(res.status_code, 409)
        self.assertIn("중복", res.get_json()["message"])

    def test_login_success(self):
        res = self.app.post('/login', json=self.default_user)
        self.assertEqual(res.status_code, 200)
        self.assertIn("로그인 성공", res.get_json()["message"])

    def test_login_failure(self):
        res = self.app.post('/login', json={
            "email": "wrong@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(res.status_code, 401)
        self.assertIn("로그인 실패", res.get_json()["message"])

    def test_me_endpoint_after_login(self):
        with self.app as client:
            client.post('/login', json=self.default_user)
            res = client.get('/me')
            self.assertEqual(res.status_code, 200)
            self.assertIn("username", res.get_json())

    def test_update_profile_success(self):
        with self.app as client:
            client.post('/login', json=self.default_user)
            res = client.post('/update-profile', json={
                "username": "newname",
                "email": "new@email.com",
                "phone": "010-1111-2222"
            })
            self.assertEqual(res.status_code, 200)
            self.assertIn("프로필 수정 완료", res.get_json()["message"])

    def test_update_profile_user_not_found(self):
        # ID 1번 유저 삭제 후 테스트
        user = User.query.get(1)
        db.session.delete(user)
        db.session.commit()

        res = self.app.post('/update-profile', json={
            "username": "ghost"
        })
        self.assertEqual(res.status_code, 404)
        self.assertIn("사용자 없음", res.get_json()["message"])


if __name__ == '__main__':
    unittest.main()
