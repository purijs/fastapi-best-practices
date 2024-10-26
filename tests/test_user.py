import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_user(self):
        response = self.client.post(
            "/users",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.user_id = data["id"]

    # Additional tests can be added here

if __name__ == '__main__':
    unittest.main()
