class UserControllerErrors(Exception):
    def __init__(self, user_idnr):
        self.user_idnr = user_idnr
        super().__init__()


class UserNotExistingError(UserControllerErrors):

    def __str__(self):
        return "User does not exist."


class UserAlreadyExistsError(UserControllerErrors):

    def __str__(self):
        return "User already exists."


class UserNotActivatedError(UserControllerErrors):

    def __str__(self):
        return "User is not activated"


class UserAlreadyActive(UserControllerErrors):

    def __str__(self):
        return "User is already activated"


class WrongUnlockCodeError(UserControllerErrors):

    def __str__(self):
        return "Wrong unlock code entered for user"


class WrongDateOfBirthError(UserControllerErrors):

    def __str__(self):
        return "Wrong date of birth entered for user"
