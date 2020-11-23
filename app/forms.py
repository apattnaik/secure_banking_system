from flask_wtf import FlaskForm
from app.models import AccountType
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DecimalField, HiddenField
from wtforms.validators import DataRequired

#specific validators need to be added for all fields

class LoginForm(FlaskForm):
    id = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit1 = SubmitField('Sign In')#submit button

class ApproveRequestForm(FlaskForm):
    request_id = HiddenField('request_id', validators=[DataRequired()])
    submit = SubmitField('approve')
class DenyRequestForm(FlaskForm):
    request_id = HiddenField('request_id', validators=[DataRequired()])
    submit = SubmitField('deny')

class NewAccountForm(FlaskForm):
    account_name = StringField('Account name', valdiators=[DataRequired()])
    account_type = SelectField('Account type',
                               choices=[('checking', 'checking'),
                                        ('savings', 'savings')],
                               validators=[DataRequired()])
    submit = SubmitField('Request')

class InternalTransForm(FlaskForm):
    account_from =  IntegerField('From', validators=[DataRequired()])
    account_to = SelectField('To', coerce = int)#for this there is code needed to dynamically populate the options that goes with this part
    amount = DecimalField('Amount',places = 2, validators=[DataRequired()])
    submit2 = SubmitField('InternalTrans')
    
class ExternalTransForm(FlaskForm):
    account_to = IntegerField('To', validators=[DataRequired()])
    account_to_validate = IntegerField('Confirm account', validators=[DataRequired()])
    account_type = StringField('Type',validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    name = StringField('Type',validators=[DataRequired()])
    submit3 = SubmitField('ExternalTrans')
    
class QuickpayForm(FlaskForm):
    email_to = StringField('Email')
    phone_to = IntegerField('Phone')
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit4 = SubmitField('Qquickpay')

class CashierCheckForm(FlaskForm):
    account_from =  IntegerField('From', validators=[DataRequired()])
    account_to = IntegerField('To', validators=[DataRequired()])
    amount = DecimalField('Amount',places = 2, validators=[DataRequired()])
    submit5 = SubmitField('Create_Cashier_Check')