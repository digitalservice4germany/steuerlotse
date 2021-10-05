from werkzeug.datastructures import ImmutableMultiDict

from app.routes import extract_information_from_request


class TestExtractInformationFromRequest:

    def test_if_post_then_return_update_data_true(self, app):
        with app.test_request_context(method="POST"):
            update_data, _ = extract_information_from_request()

        assert update_data is True

    def test_if_get_then_return_update_data_false(self, app):
        with app.test_request_context(method="GET"):
            update_data, _ = extract_information_from_request()

        assert update_data is False

    def test_if_post_and_form_data_then_extract_correct_form_data(self, app):
        form_data = {'Slytherin': 'Loyalty'}
        with app.test_request_context(method="POST", data=form_data):
            update_data, extracted_form_data = extract_information_from_request()

        assert extracted_form_data == ImmutableMultiDict(form_data)
