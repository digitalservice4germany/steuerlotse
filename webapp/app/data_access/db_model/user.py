import datetime

from flask_login.mixins import UserMixin
from sqlalchemy import LargeBinary

from app.extensions import db
from app.crypto.pw_hashing import global_salt_hash, indiv_salt_hash
from app.data_access.user_controller_errors import UserAlreadyActive


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idnr_hashed = db.Column(db.String(), unique=True, nullable=False)
    dob_hashed = db.Column(db.String(), nullable=False)
    elster_request_id = db.Column(db.String(), nullable=False)
    unlock_code_hashed = db.Column(db.String())
    pdf = db.Column(LargeBinary())
    transfer_ticket = db.Column(db.String())
    last_modified = db.Column(db.TIMESTAMP(timezone=True), nullable=False, index=True,
                              onupdate=db.func.current_timestamp(),
                              default=datetime.datetime.utcnow)

    def __init__(self, idnr: str, dob: str, elster_request_id: str):
        """
        :param idnr: The Identification number of the user
        :param dob: The date of birth of the user
        :param request_id: The AntragsId for requesting the access to the user at Elster
        """
        super().__init__(
            idnr_hashed=global_salt_hash().hash(idnr),
            dob_hashed=indiv_salt_hash().hash(dob),
            elster_request_id=elster_request_id
        )

    def activate(self, unlock_code: str):
        """
        When the user requested the unlock code with Elster, got it via postal services and it is verified,
        the user can be activated. Only active users can log in because they have a set fsc,
        which can be used to verify them.

        :param unlock_code: The with Elster verified unlock code (Freischaltcode) of the user.
        """
        if self.is_active:
            raise UserAlreadyActive(self.idnr_hashed)

        self.unlock_code_hashed = indiv_salt_hash().hash(unlock_code)

    @property
    def is_active(self):
        return self.unlock_code_hashed is not None

    def get_id(self):
        return self.idnr_hashed

    @classmethod
    def get(cls, idnr):
        idnr_hash = global_salt_hash().hash(idnr)
        return cls.get_from_hash(idnr_hash)

    @classmethod
    def get_from_hash(cls, idnr_hash):
        return cls.query.filter_by(idnr_hashed=idnr_hash).first()

    def has_completed_tax_return(self):
        return self.pdf is not None
