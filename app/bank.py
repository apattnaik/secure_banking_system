from app import db
from app.models import User, T1Employee, T2Employee, Administrator, Account, Request, InfoChangeRequest, NewAccountRequest
from app import errors

critical_transaction_threshold = 1000.0

def dominates(u1, u2):
    """Returns True if u1 dominates u2, False otherwise."""
    if u1.user_type == 'users': return False
    if u1.user_type == 't1employees' or u1.user_type == 't2employees':
        return u2.user_type == 'users'
    if u1.user_type == 'administrators':
        return u2.user_type == 't1employees' or u2.user_type == 't2employees'

def approval_class(user):
    if user.user_type == 'users':
        return 't1employees'
    else:
        return 'administrators'

def user_by_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise errors.NonexistantUserError(user_id, "could not find user")
    return user

def request_by_id(request_id):
    request = Request.query.get(request_id)
    if request is None:
        raise errors.NonexistantRequestError(request_id, "could not find request")
    return request

def user_by_id_and_type(user_id, user_type):
    """Retrieve an user by its id, and assert that it is of a certain type

    This function retrieves an user with id `user_id`, but also
    asserts that its type is `user_type`. If the second check fails,
    PermissionError is raised.

    """
    user = user_by_id(actor_id)
    if user is actor_type:
        return user
    else:
        raise PermissionError("permission denied, user is not %s" % user_type)

def get_customer_accounts(customer_id):
    """Retrieve a list of accounts belonging to a user."""
    return Account.query.filter_by(owner_id = customer_id).all()

def get_pending_requests(actor_id):
    """Retrieve a list of requests applicable to this actor.

    Returns a list of Request objects. These may be of any type. The
    only requests returned are those that this user has authorization
    to approve. For tier 1 employees, this means all customer requests.

    """
    actor = user_by_id(actor_id)
    actor_type = actor.user_type
    return Request.query.filter_by(approved = False, approval_needed_from = actor_type).all()

def get_pending_critical_transactions(actor_id):
    """Retrieve a list of pending critical transactions.

    Returns a list of Transaction objects. The actor must be a tier 2
    employee."""

    actor = user_by_id_and_type(actor_id, T2Employee)
    return Transaction.query.filter_by(amount > critical_transaction_threshold, approved = False).all()

def request_info_change(actor_id, new_full_name = None,
                        new_email = None, new_phone = None,
                        new_address_street = None,
                        new_address_city = None,
                        new_address_zip = None):
    actor = user_by_id(actor_id)
    approver = approval_class(actor)
    ir = InfoChangeRequest(requester_id = actor_id,
                           approval_needed_from = approver,
                           approved = False,
                           new_full_name = new_full_name,
                           new_email = new_email, new_phone = new_phone,
                           new_address_street = new_address_street,
                           new_address_city = new_address_city,
                           new_address_zip = new_address_zip)
    db.session.add(ir)
    db.session.commit()
    return ir

def request_new_account(actor_id, account_name, account_type):
    actor = user_by_id(actor_id)
    approver = approval_class(actor)
    nar = NewAccountRequest(requester_id = actor_id,
                            approval_needed_from = approver,
                            approved = False,
                            account_name = account_name,
                            account_type = account_type)
    db.session.add(nar)
    db.session.commit()
    return nar

def approve_request(actor_id, request_id):
    actor = user_by_id(actor_id)
    request = request_by_id(request_id)
    if request.approval_needed_from != actor.user_type:
        return errors.PermissionError('cannot approve or deny request: permission denied')
    request.approved = True
    request.apply_to(request.requester)

    db.session.commit()
    return request

def deny_request(actor_id, request_id):
    actor = user_by_id(actor_id)
    request = request_by_id(request_id)
    if request.approval_needed_from != actor.user_type:
        return errors.PermissionError('cannot approve or deny request: permission denied')
    db.session.delete(request)
    db.session.commit()
    return request

def modify_user(actor_id, user_id, change_request):
    """Modify a user's account.

    `actor_id` is the id of the user making the modification.
    `user_id` is the id of the user account being modified.
    `change_request` is an object of type InfoChangeRequest. Even if a
    request wasn't involved, this is the object that will hold all the
    relevant information that can be changed.

    PermissionError will be raised if the actor does not dominate the user."""

    actor = user_by_id(actor_id)
    user = user_by_id(user_id)
    if not dominates(actor, user):
        raise errors.PermissionError("cannot modify account of non-dominated user")

    change_request.apply_to(user)
