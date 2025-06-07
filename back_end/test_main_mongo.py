import unittest
from unittest.mock import patch, MagicMock
from main import app, db, User

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch("app.logs_collection")
    def test_get_logs(self, mock_logs):
        mock_logs.count_documents.return_value = 1
        mock_logs.find.return_value.skip.return_value.limit.return_value = [{"log": "test"}]

        response = self.app.get('/api/logs?page=1&limit=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("logs", response.get_json())

    def test_register_success(self):
        response = self.app.post("/register", json={"email": "a@b.com", "password": "pass"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("회원가입", response.get_json()["message"])

    def test_register_duplicate(self):
        db.session.add(User(email="a@b.com", password="pass"))
        db.session.commit()
        response = self.app.post("/register", json={"email": "a@b.com", "password": "pass"})
        self.assertEqual(response.status_code, 409)

    def test_register_missing(self):
        response = self.app.post("/register", json={"email": ""})
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        db.session.add(User(email="a@b.com", password="pass", username="abc"))
        db.session.commit()
        response = self.app.post("/login", json={"email": "a@b.com", "password": "pass"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("로그인", response.get_json()["message"])

    def test_login_failure(self):
        response = self.app.post("/login", json={"email": "wrong@a.com", "password": "pass"})
        self.assertEqual(response.status_code, 401)

    def test_me(self):
        user = User(email="a@b.com", password="pass", username="Tester")
        db.session.add(user)
        db.session.commit()

        with self.app.session_transaction() as sess:
            sess["user_id"] = user.id

        response = self.app.get("/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["username"], "Tester")

    def test_update_profile(self):
        user = User(email="old@a.com", password="pass", username="old", phone="123")
        db.session.add(user)
        db.session.commit()

        response = self.app.post("/update-profile", json={
            "username": "new",
            "email": "new@a.com",
            "phone": "456"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("수정", response.get_json()["message"])

        updated = User.query.get(user.id)
        self.assertEqual(updated.username, "new")
        self.assertEqual(updated.email, "new@a.com")
        self.assertEqual(updated.phone, "456")

if __name__ == "__main__":
    unittest.main()
