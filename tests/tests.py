from flask_testing import TestCase
import app
from app import models
import unittest

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

    def create_app(self):
        return app.create_app(self)

    def setUp(self):
        app.db.init_app(self.app)
        app.db.create_all()

        self.init_admin = models.Administrator(user_name = 'admin')
        self.init_employee = models.T1Employee(user_name = 'emp1')
        self.init_customer = models.User(user_name = 'user1')
        app.db.session.add(self.init_admin)
        app.db.session.add(self.init_employee)
        app.db.session.add(self.init_customer)
        app.db.session.commit()


    def tearDown(self):
        app.db.session.remove()
        # no need to drop, it's an in-memory database
        app.db.drop_all()
        # but we'll do it anyways ;)
    

class CreateUserTest(MyTest):
    def test_create_user(self):
        assert True

    def test_get_requests():
        req = InfoChangeRequest(requester_id = self.init_customer.id,
                                new_email = "test@test.com")


if __name__ == '__main__':
    unittest.main()
