import datetime as dt
import logging
import os
import click

from flask.cli import AppGroup
from sqlalchemy.exc import IntegrityError

from app.elster_client.elster_errors import ElsterProcessNotSuccessful, \
    ElsterRequestAlreadyRevoked, ElsterRequestIdUnkownError


logger = logging.getLogger(__name__)


@click.command()
def populate_database():
    try:
        from app.extensions import db
        from app.data_access.db_model.user import User

        if os.environ.get('FLASK_ENV') == 'production':
            logger.warn('Refusing to run populate database cron job on production '
                            '(would create unwanted users).')
            return

        logger.info('Executing populate_database')

        pre_stored_idnrs = [('04452397687', 'DBNH-B8JS-9JE7'),
                            ('02259674819', 'BMVL-U2YM-AWJ4')]
        for idnr, unlock_code in pre_stored_idnrs:
            new_user = User(idnr, '1985-01-01', '123')
            new_user.activate(unlock_code)
            try:
                db.session.add(new_user)
                db.session.commit()
                logger.info('Added user with IdNr: ' + idnr)
            except IntegrityError:
                db.session.rollback()
                logger.warn('User with IdNr ' + idnr + ' already exists in database.')
    except Exception:
        logger.exception('An unexpected error occurred.')


cronjob_cli = AppGroup('cronjob')

@cronjob_cli.command('delete_outdated_users')
def delete_outdated_users():
    try:
        if os.environ.get('FLASK_ENV') == 'staging':
            logger.warn('Refusing to run lifecycle cron job on staging (would delete users needed for testing)')
            return

        _delete_outdated_users()
    except Exception:
        logger.exception('An unexpected error occurred.')


def _delete_outdated_users():
    from app.extensions import db

    logger.info('Executing delete_outdated_users')

    _delete_outdated_not_activated_users()
    _delete_outdated_users_with_completed_process()
    _delete_inactive_users()
    db.session.commit()


def _delete_outdated_not_activated_users():
    from app.extensions import db
    from app.data_access.db_model.user import User

    num_deleted_rows = db.session.query(User) \
        .filter(User.unlock_code_hashed.is_(None),
                User.last_modified < dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)) \
        .delete(synchronize_session=False)
    logger.info('Removed outdated non-activated users: ' + str(num_deleted_rows))


def _delete_outdated_users_with_completed_process():
    from app.extensions import db
    from app.data_access.db_model.user import User

    users_to_delete_query = db.session.query(User) \
        .filter(User.pdf.isnot(None),
                User.last_modified < dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10))
    users_to_delete = users_to_delete_query.all()

    _revoke_permission_and_delete_users(users_to_delete, 'Removed user with completed process.')


def _delete_inactive_users():
    from app.extensions import db
    from app.data_access.db_model.user import User

    users_to_delete_query = db.session.query(User) \
        .filter(User.last_modified < dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=60))
    users_to_delete = users_to_delete_query.all()

    _revoke_permission_and_delete_users(users_to_delete, 'Removed user inactive for long time.')


def _revoke_permission_and_delete_users(users_to_delete, success_message):
    from app.extensions import db
    from app.elster_client import elster_client
    from app.crypto.pw_hashing import global_salt_hash

    for user_to_delete in users_to_delete:
        PRODUCTION_TEST_IDNR = '04452397687'
        if user_to_delete.idnr_hashed == global_salt_hash().hash(PRODUCTION_TEST_IDNR):
            # Ensure that testmerker is used to actually revoke the permission
            form_data = {
                'idnr': PRODUCTION_TEST_IDNR,
                'elster_request_id': user_to_delete.elster_request_id}
        else:
            form_data = {
                'idnr': user_to_delete.idnr_hashed,
                'elster_request_id': user_to_delete.elster_request_id}
        try:
            elster_client.send_unlock_code_revocation_with_elster(form_data, 'CRONJOB-IP')
            db.session.delete(user_to_delete)
            logger.info(success_message)
        except (ElsterRequestAlreadyRevoked, ElsterRequestIdUnkownError) as e:
            logger.warn(str(e))
            db.session.delete(user_to_delete)
            logger.info(success_message)
        except ElsterProcessNotSuccessful as e:
            logger.error(str(e))
