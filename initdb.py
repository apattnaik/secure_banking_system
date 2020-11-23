from app import models
from app import db

from datetime import datetime

if __name__ == '__main__':
    test_user_1 = models.User(
        user_name = 'tu1', full_name = 'Test User 1',
        is_merchant = False,
        email = 'test@test.com',
        phone = '100-1001-0000',
        address_street = '123 fake st',
        address_city = 'city',
        address_zip = '12345',
        creation_time = datetime.now())

    test_emp_1 = models.T1Employee(
        user_name = 'tt1e1', full_name = 'Test Tier 1 Employee 1',
        is_merchant = False,
        email = 'test@employee.com',
        phone = '100-1001-1111',
        address_street = '124 fake st',
        address_city = 'city',
        address_zip = '12345',
        creation_time = datetime.now())

    test_emp2_1 = models.T2Employee(
        user_name = 'tt2e1', full_name = 'Test Tier 2 Employee 1',
        is_merchant = False,
        email = 'test@employee2.com',
        phone = '100-2001-1111',
        address_street = '334 fake st',
        address_city = 'city',
        address_zip = '12345',
        creation_time = datetime.now())

    test_admin_1 = models.Administrator(
        user_name = 'ta1', full_name = 'Test Administrator 1',
        is_merchant = False,
        email = 'test@admin.com',
        phone = '222-2001-1111',
        address_street = '1600 Pennsylvania Ave.',
        address_city = 'Washington D.C.',
        address_zip = '69420',
        creation_time = datetime.now())

    us = [test_user_1, test_emp_1, test_emp2_1, test_admin_1]

    for u in us:
        print("creating user in %s with username: %s, password: %s" %
            (u.user_type, u.user_name, 'test'))
        u.set_password('test')
        db.session.add(u)

    db.session.commit()
