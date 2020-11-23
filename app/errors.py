class BankingSystemError(Exception):
    pass

class NonexistantUserError(BankingSystemError):
    def __init__(self, nonexistant_id, message):
        self.nonexistant_id = nonexistant_id
        self.message = message

class NonexistantRequestError(BankingSystemError):
    def __init__(self, nonexistant_id, message):
        self.nonexistant_id = nonexistant_id
        self.message = message


class PermissionError(BankingSystemError):
    def __init__(self, message):
        self.message = message
