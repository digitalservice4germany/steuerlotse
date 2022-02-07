from cookie_storage import CookieStorage
from app.data_access.storage.session_storage import SessionStorage


def sync_session_to_redis():
    # get all session data
    form_data = CookieStorage().get_data('form_data')
    if form_data.__len__() <= 1:
        return

    # remove unlock code from redis session and save other session_data
    form_data_session = form_data.copy()
    del form_data_session['unlock_code']
    SessionStorage().override_data(form_data_session, 'form_data')

    # create session cookie with unlock_code
    form_data_cookie = {
        'unlock_code': form_data['unlock_code']
    }
    CookieStorage().override_data(form_data_cookie)
