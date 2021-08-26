import datetime

from app.extensions import db


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, index=True, default=datetime.datetime.utcnow)
    log_data = db.Column(db.BINARY, nullable=False)
