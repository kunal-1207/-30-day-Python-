import unittest
from create_user import create_linux_user

class TestUserCreation(unittest.TestCase):
    def test_user_creation(self):
        self.assertTrue(
            create_linux_user("testuser", password="temp123", system_account=True)
        )

if __name__ == "__main__":
    unittest.main()
