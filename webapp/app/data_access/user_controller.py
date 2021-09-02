from typing import ByteString

from flask_login.utils import login_user

from app.extensions import db
from app.crypto.pw_hashing import indiv_salt_hash, global_salt_hash

from app.data_access.db_model.user import User
from app.data_access.user_controller_errors import UserAlreadyExistsError, UserNotExistingError, \
    UserNotActivatedError, WrongUnlockCodeError


def user_exists(user_id: str) -> bool:
    try:
        find_user(user_id)
    except UserNotExistingError:
        return False
    return True


def find_user(idnr: str) -> User:
    user = User.get(idnr)
    if not user:
        raise UserNotExistingError(idnr)
    return user


def create_user(idnr: str, dob: str, elster_request_id: str) -> User:
    if User.get(idnr):
        raise UserAlreadyExistsError(idnr)

    user = User(idnr, dob, elster_request_id)
    db.session.add(user)
    db.session.commit()

    return user


def delete_user(idnr: str) -> None:
    db.session.delete(find_user(idnr))
    db.session.commit()


def activate_user(idnr: str, unlock_code: str) -> User:
    user = find_user(idnr)
    user.activate(unlock_code)
    db.session.commit()
    return user


def store_pdf_and_transfer_ticket(user: User, pdf: ByteString, transfer_ticket: str):
    user.pdf = pdf
    user.transfer_ticket = transfer_ticket
    db.session.commit()


def verify_and_login(idnr, unlock_code):
    """
    This checks whether an active user with the idnr exists and then verifies the entered unlock_code.
    If everything is alright, the user is logged in.

    :return: The logged in user, if the unlock code was verified. If the code is incorrect None is returned.
    """
    user = find_user(idnr)
    if not user.is_active:
        raise UserNotActivatedError(idnr)
    if _check_unlock_code(user, unlock_code):
        return login_user(user)
    else:
        raise WrongUnlockCodeError(idnr)


def check_idnr(user, idnr):
    return global_salt_hash().verify(idnr, user.idnr_hashed)


def check_dob(user, dob):
    return indiv_salt_hash().verify(dob, user.dob_hashed)


def _check_unlock_code(user, unlock_code):
    return indiv_salt_hash().verify(unlock_code, user.unlock_code_hashed)
