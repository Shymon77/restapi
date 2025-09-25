import unittest
from app.models import Contact, User


class TestContactModel(unittest.TestCase):
    def test_create_contact(self):
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="123456789",
        )
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.email, "john@example.com")


class TestUserModel(unittest.TestCase):
    def test_create_user(self):
        user = User(email="user@example.com", password="hashedpassword")
        self.assertEqual(user.email, "user@example.com")


from app import create_app

app = create_app()
