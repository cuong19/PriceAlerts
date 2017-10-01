class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass
