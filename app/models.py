from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)

    full_name = db.Column(db.String)
    is_merchant = db.Column(db.Boolean)
    password_hash = db.Column(db.String)

    user_type = db.Column(db.String)

    accounts = db.relationship('Account', back_populates='owner')

    email = db.Column(db.String)
    phone = db.Column(db.String)
    address_street = db.Column(db.String)
    address_city = db.Column(db.String)
    address_zip = db.Column(db.String)

    creation_time = db.Column(db.DateTime)

    most_recent_login = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type
    }

    # stuff for flask_login
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id

    # set and check password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class T1Employee(User):
    __tablename__ = 't1employees'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 't1employees',
    }

class T2Employee(User):
    __tablename__ = 't2employees'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 't2employees',
    }

class Administrator(User):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrators',
    }


class AccountType(enum.Enum):
    checking = 'checking'
    savings = 'savings'

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, db.Sequence('account_id_seq'), primary_key=True)
    name = db.Column(db.String, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', back_populates='accounts')

    name = db.Column(db.String)
    balance = db.Column(db.Numeric)
    account_type = db.Column(db.Enum(AccountType))
    debit_card_number = db.Column(db.String(16))
    credit_card_number = db.Column(db.String(16))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, db.Sequence('transaction_id_seq'), primary_key=True)
    account_from = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account_to = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    amount = db.Column(db.Numeric)

    initiation_time = db.Column(db.DateTime)

    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requester = db.relationship('User')

    approved = db.Column(db.Boolean)

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, db.Sequence('request_id_seq'), primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requester = db.relationship('User')
    # what kind of user do we need approval from?
    approval_needed_from = db.Column(db.String)
    approved = db.Column(db.Boolean)

    request_type = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'requests',
        'polymorphic_on': request_type
    }

class InfoChangeRequest(Request):
    __tablename__ = 'info_change_requests'
    id = db.Column(db.Integer, db.ForeignKey('requests.id'), primary_key=True)

    new_full_name = db.Column(db.String)
    new_password_hash = db.Column(db.String)
    new_email = db.Column(db.String)
    new_phone = db.Column(db.String)
    new_address_street = db.Column(db.String)
    new_address_city = db.Column(db.String)
    new_address_zip = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'info_change_requests',
    }

    def apply_to(self, user):
        if self.new_full_name is not None: user.full_name = self.new_full_name
        if self.new_password_hash is not None: user.password_hash = self.new_password_hash
        if self.new_email is not None: user.email = self.new_email
        if self.new_phone is not None: user.phone = self.new_phone
        if self.new_address_street is not None: user.address_street = self.new_address_street
        if self.new_address_city is not None: user.address_city = self.new_address_city
        if self.new_address_zip is not None: user.address_zip = self.new_address_zip
        db.session.add(user)
        db.session.commit()


class NewAccountRequest(Request):
    __tablename__ = 'new_account_requests'
    id = db.Column(db.Integer, db.ForeignKey('requests.id'), primary_key=True)

    account_name = db.Column(db.String, nullable=False)
    account_type = db.Column(db.Enum(AccountType))

    __mapper_args__ = {
        'polymorphic_identity': 'new_account_requests',
    }

    def apply_to(self, user):
        new_account = Account(owner_id = user.id, account_type = self.account_type,
                              name = self.account_name, balance = 0,
                              debit_card_number = None, credit_card_number = None)
        db.session.add(new_account)
        db.session.commit()


class SigninLogs(User): 
    __tablename__ = 'signin_logs'

    id = db.Column(db.Integer, db.Sequence('login_id_seq'), primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey('users.id'))
    login_attempt_time= db.Column(db.DateTime)
    login_status=db.Column(db.String)

class CashierCheck():
    __tablename__= 'cashier_check_request'

    id = db.Column(db.Integer, db.Sequence('cashier_check'), primary_key=True)
    account_from = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account_to = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount = db.Column(db.Numeric)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved = db.Column(db.Boolean)





    

    