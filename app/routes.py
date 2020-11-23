from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from app import app
from app import db
from app import bank
from app.forms import LoginForm, NewAccountForm, ApproveRequestForm, DenyRequestForm
from app.models import User, AccountType, Request

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/main') #should be the same as '/' ?
@login_required
def main():
    if current_user.user_type == 'users':
        accounts = bank.get_customer_accounts(current_user.id)
        return render_template('main-user.html', title='Main',
                               user = current_user,
                               accounts = accounts)
    else:
        requests = bank.get_pending_requests(current_user.id)
        arf = ApproveRequestForm()
        drf = DenyRequestForm()
        
        return render_template('main-employee.html', title='Main',
                               user = current_user,
                               requests = requests,
                               approve_request_form = arf,
                               deny_request_form = drf)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('main'))

    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name = form.id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        user.most_recent_login = datetime.now()
        db.session.add(user)
        db.session.commit()

        flash('Login requested for user {}'.format(
            form.id.data))
        return redirect(url_for('main'))
    return render_template('login.html', title='Log In', form=form)

@app.route('/approve_request', methods=['POST'])
@login_required
def approve_request():
    if current_user is None or not current_user.is_authenticated:
        return redirect(url_for('main'))
    
    arf = ApproveRequestForm()
    if arf.validate_on_submit():
        request_id = arf.request_id.data
        request = bank.approve_request(current_user.id, request_id)
        flash('Approved request for user %s' % request.requester.full_name)
        return redirect(url_for('main'))
    else:
        flash('Failed due to errors: %s' % drf.errors)
        return redirect(url_for('main'))


@app.route('/deny_request', methods=['POST'])
@login_required
def deny_request():
    if current_user is None or not current_user.is_authenticated:
        return redirect(url_for('main'))
    
    drf = DenyRequestForm()
    if drf.validate_on_submit():
        request_id = drf.request_id.data
        request = bank.deny_request(current_user.id, request_id)
        flash('Denied request')
        return redirect(url_for('main'))
    else:
        flash('Failed due to errors: %s' % drf.errors)
        return redirect(url_for('main'))

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/request_new_account', methods=['GET', 'POST'])
@login_required
def request_new_account():
    if current_user.user_type != 'users':
        flash('Only customers are allowed to request new accounts')
        return redirect(url_for('main'))

    new_account_form = NewAccountForm()
    if request.method == 'GET':
        return render_template('new_account.html', new_account_form=new_account_form)

    print("HI")
    if new_account_form.validate_on_submit():
        account_type = None
        account_type_str = new_account_form.account_type.data
        account_name = new_account_form.account_name.data
        if account_type_str == 'checking':
            account_type = AccountType.checking
        elif account_type_str == 'savings':
            account_type = AccountType.savings
        bank.request_new_account(current_user.id, account_name, account_type)
        flash('Your request for a %s account has been filed.' % account_type_str)
        return redirect(url_for('main'))
    else:
        flash(new_account_form.errors)
        return redirect(url_for('main'))

@app.route('/inttrans', methods=['POST'])
def inttrans():
    inttrans_form = InternalTransForm()
    if inttrans_form.validate_on_submit():
        flash('Transaction submitted')
        return redirect(url_for('main'))
    else:
        flash('Transaction not valid') 
        return redirect(url_for('transaction'))
    return render_template('transaction.html', title='Transaction', inttrans_form=inttrans_form)

@app.route('/exttrans', methods=['POST'])
def exttrans():
    exttrans_form = ExternalTransForm()
    if exttrans_form.validate_on_submit():
        flash('Transaction submitted')
        return redirect(url_for('main'))
    else:
        flash('Transaction not valid') 
        return redirect(url_for('transaction'))
    return render_template('transaction.html', title='Transaction', exttrans_form=exttrans_form)

@app.route('/quicktrans', methods=['POST'])
def quicktrans():
    quick_form = QuickpayForm()
    if quicktrans_form.validate_on_submit():
        flash('Transaction submitted')
        return redirect(url_for('main'))
    else:
        flash('Transaction not valid') 
        return redirect(url_for('transaction'))
    return render_template('transaction.html', title='Transaction', quick_form=quick_form)

@app.route('/cashCheck')
def cashCheck():
    cashCheck_form= CashierCheckForm()
    if cashCheck_form.validate_on_submit():
        flash('Cashier Check Created')
        return redirect(url_for('main'))
    else:
        flash('Transaction not valid') 
        return redirect(url_for('transaction'))
    return render_template()#Cashier check html page




#@app.route('/settings')
#@app.route('/open')
#@app.route('/statement')


#@app.route('/tier1')
#@app.route('/tier2')
#@app.route('/admin')
