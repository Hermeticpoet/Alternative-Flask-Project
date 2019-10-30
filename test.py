from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_loads(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertTrue(b"Please Login" in response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post("/login", data=dict(username="admin", password="admin"),
        follow_redirects=True)
        self.assertIn(b"You are now logged in!", response.data)

    # Ensure login behaves correctly given the wrong credentials
    def test_invalid_login_credentials(self):
        tester = app.test_client(self)
        response = tester.post("/login", data=dict(username="wrong", password="wrong"), follow_redirects=True)
        self.assertIn(b"Invalid Credentials. Please try again.", response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post("/login", data=dict(username="admin", password="admin"),
        follow_redirects=True)
        response = tester.get("/logout", follow_redirects=True)
        self.assertIn(b"You are now logged out!", response.data)

    # Ensure main home page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get("/", follow_redirects=True)
        self.assertTrue(b"You need to log in first." in response.data)

    # Ensure that recipes show up on the main page
    def test_recipes_show_up_on_main_page(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Title', response.data)

if __name__ == "__main__":
    unittest.main()