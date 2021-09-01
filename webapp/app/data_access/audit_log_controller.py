import datetime as dt
import json
from dataclasses import dataclass

from app.extensions import db
from app.crypto.encryption import hybrid_encrypt
from app.data_access.db_model.audit_log import AuditLog


@dataclass
class LoggedData:
    event_name: str
    timestamp: str
    ip_address: str
    idnr: str
    transfer_ticket: str
    elster_request_id: str


@dataclass
class LoggedConfirmationData:
    event_name: str
    timestamp: str
    ip_address: str
    idnr: str
    confirmation_label: str
    confirmation_value: bool


@dataclass
class LoggedAddressData:
    event_name: str
    timestamp: str
    ip_address: str
    idnr: str
    address: str


def create_audit_log_entry(event_name: str, ip_address: str, idnr: str, transfer_ticket: str,
                           elster_request_id: str = '') -> AuditLog:
    log_data = LoggedData(event_name, dt.datetime.utcnow().isoformat(), ip_address, idnr,
                          transfer_ticket, elster_request_id)
    return _save_audit_log_object(log_data)


def create_audit_log_confirmation_entry(event_name: str, ip_address: str, idnr: str,
                                        confirmation_label: str, confirmation_value: bool) -> AuditLog:
    log_data = LoggedConfirmationData(event_name, dt.datetime.utcnow().isoformat(), ip_address, idnr,
                                      confirmation_label, confirmation_value)
    return _save_audit_log_object(log_data)


def create_audit_log_address_entry(event_name: str, ip_address: str, idnr: str, address: str) -> AuditLog:
    log_data = LoggedAddressData(event_name, dt.datetime.utcnow().isoformat(), ip_address, idnr, address)
    return _save_audit_log_object(log_data)


def _save_audit_log_object(audit_log_object) -> AuditLog:
    log_data_json = json.dumps(audit_log_object.__dict__, default=str)
    encrypted_data = hybrid_encrypt(log_data_json.encode())

    log_insert_stmt = AuditLog.__table__.insert(inline=True).values(log_data=encrypted_data)
    db.session.execute(log_insert_stmt)
    db.session.commit()

    return encrypted_data
