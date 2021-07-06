import json
import unittest
from unittest.mock import patch, MagicMock, call

from flask import url_for
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.routing import BuildError
from werkzeug.utils import redirect

from app import app
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.steps.steuerlotse_step import SteuerlotseStep, serialize_session_data, deserialize_session_data, \
    RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormStep, \
    MockFormWithInputStep, MockRenderStep, MockYesNoStep
from tests.utils import create_session_form_data


class TestSteuerlotseStepInit(unittest.TestCase):

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current session and link_overview are set from request
        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': "True"}

            step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="WhereItAllStarts")

            self.assertTrue(step.has_link_overview)
            self.assertIsNone(step.render_info)

        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': "False"}

            step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="WhereItAllStarts")

            self.assertFalse(step.has_link_overview)
            self.assertIsNone(step.render_info)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        # Only link_overview and session are set from request
        with app.app_context() and app.test_request_context():
            step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="WhereItAllStarts")

            self.assertFalse(step.has_link_overview)
            self.assertIsNone(step.render_info)


class TestSteuerlotseStepUrlForStep(unittest.TestCase):

    @staticmethod
    def helper_build_test_url(endpoint, step):
        return "/" + endpoint + "/step/" + step.name

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]

            self.endpoint_correct = "lotse"
            self.endpoint_incorrect = "IT_IS_A_TRAP"
            self.correct_session = "C3PO"
            self.incorrect_session = "r2D2"
            self.set_link_overview = True
            self.expected_url_params_if_attribute_set = "?link_overview=" + str(self.set_link_overview)
            self.empty_url_params = ""

            self.steuerlotse_step_with_overlink_view = SteuerlotseStep(title="The Steuerlotse I",
                                                                       intro="Not so long ago....",
                                                                       endpoint=self.endpoint_correct)
            self.steuerlotse_step_with_overlink_view.has_link_overview = True

    def test_if_step_given_and_attributes_correct_then_return_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockStartStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

            created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockMiddleStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockMiddleStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

            created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockFinalStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockFinalStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

    def test_if_attributes_empty_then_correct_url(self):
        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I",
                                               intro="Not so long ago....",
                                               endpoint=self.endpoint_correct)
            created_url = steuerlotse_step.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=False"
            self.assertEqual(expected_url, created_url)

    def test_if_attributes_correct_then_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                      MockStartStep) + self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

    def test_if_link_overview_param_set_then_used_in_url(self):
        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': "True"}
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I",
                                               intro="Not so long ago....",
                                               endpoint=self.endpoint_correct)
            created_url = steuerlotse_step.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=True"
            self.assertEqual(expected_url, created_url)

        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': "False"}
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I",
                                               intro="Not so long ago....",
                                               endpoint=self.endpoint_correct)
            created_url = steuerlotse_step.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=False"
            self.assertEqual(expected_url, created_url)

    def test_if_incorrect_endpoint_then_throw_error(self):
        with app.app_context() and app.test_request_context():
            steuerlotse_incorrect_endpoint = SteuerlotseStep(title="The Steuerlotse I",
                                                             intro="Not so long ago....",
                                                             endpoint="IncorrectEndpoint")
            self.assertRaises(BuildError, steuerlotse_incorrect_endpoint.url_for_step, MockStartStep.name)

    def test_if_additional_attr_provided_then_append_to_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockStartStep.name,
                                                                                additional_attr1="did_not_expect",
                                                                                additional_attr2="to_see_you_here")
            expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                      MockStartStep) + self.expected_url_params_if_attribute_set + \
                           "&additional_attr1=did_not_expect" \
                           "&additional_attr2=to_see_you_here"
            self.assertEqual(expected_url, created_url)


class TestSteuerlotseStepGetSessionData(unittest.TestCase):
    def setUp(self):
        with app.app_context() and app.test_request_context():
            self.endpoint_correct = "lotse"
            self.steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I",
                                                    intro="Not so long ago....",
                                                    endpoint=self.endpoint_correct)

            # Set sessions up
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_session_data_then_return_session_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            session_data = self.steuerlotse_step._get_session_data()

            self.assertEqual(self.session_data, session_data)

    def test_if_session_data_and_default_data_different_then_update_session_data(self):
        default_data = {"brother": "Luigi"}
        expected_data = {**self.session_data, **default_data}

        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            steuerlotse_step_with_default_data = SteuerlotseStep(title="The Steuerlotse I",
                                                                 intro="Not so long ago....",
                                                                 endpoint=self.endpoint_correct,
                                                                 default_data=default_data
                                                                 )

            session_data = steuerlotse_step_with_default_data._get_session_data()

            self.assertEqual(expected_data, session_data)

    def test_if_no_form_data_in_session_then_return_default_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({})
            session_data = self.steuerlotse_step._get_session_data()

            self.assertEqual({}, session_data)  # multistep flow has no default data

    def test_if_no_session_data_and_debug_data_provided_then_return_copy(self):
        original_default_data = {}
        with app.app_context() and app.test_request_context():
            session_data = self.steuerlotse_step._get_session_data()

            self.assertIsNot(original_default_data, session_data)

    def test_if_no_session_data_and_no_debug_data_then_return_empty_dict(self):
        with app.app_context() and app.test_request_context():
            session_data = self.steuerlotse_step._get_session_data()

            self.assertEqual({}, session_data)

    def test_if_session_data_then_keep_data_in_session(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': serialize_session_data(self.session_data)})
            self.steuerlotse_step._get_session_data()

            self.assertIn('form_data', req.session)
            self.assertEqual(self.session_data, deserialize_session_data(req.session['form_data'],
                                                                         app.config['PERMANENT_SESSION_LIFETIME']))


class TestSteuerlotseStepHandle(unittest.TestCase):

    def test_handle_calls_methods_in_correct_order_and_with_returned_stored_data_from_call_before(self):
        get_session_stored_data = {'location': 'Fowl Manor'}
        pre_handle_stored_data = {'location': 'Fowl Manor', 'attacker': 'Mulch Diggums'}
        main_handle_stored_data = {'location': 'Fowl Manor', 'attacker': 'Mulch Diggums', 'organisation': 'ZUP'}
        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....",
                                               endpoint="WhereItAllStarts")
            with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data",
                       MagicMock(return_value=get_session_stored_data)) as mock_get_session_data, \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._pre_handle",
                          MagicMock(return_value=pre_handle_stored_data)) as mock_pre_handle, \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._main_handle",
                          MagicMock(return_value=main_handle_stored_data)) as mock_main_handle, \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._post_handle") as mock_post_handle:
                call_order = MagicMock()
                call_order.attach_mock(mock_get_session_data, "mock_get_session_data")
                call_order.attach_mock(mock_pre_handle, "mock_pre_handle")
                call_order.attach_mock(mock_main_handle, "mock_main_handle")
                call_order.attach_mock(mock_post_handle, "mock_post_handle")

                steuerlotse_step.handle()
                call_order.assert_has_calls(
                    [call.mock_get_session_data(), call.mock_pre_handle(get_session_stored_data),
                     call.mock_main_handle(pre_handle_stored_data), call.mock_post_handle(main_handle_stored_data)])

    def test_handle_returns_result_from_post_handle(self):
        post_handle_stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....",
                                               endpoint="WhereItAllStarts")
            with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data"), \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._pre_handle"), \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._main_handle"), \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._post_handle",
                          MagicMock(return_value=post_handle_stored_data)):
                handle_result = steuerlotse_step.handle()
                self.assertEqual(post_handle_stored_data, handle_result)


class TestSteuerlotseStepPreHandle(unittest.TestCase):

    def test_if_no_prev_next_step_set_then_render_info_is_set_correctly(self):
        title = "The Steuerlotse I"
        intro = "Not so long ago...."
        correct_endpoint = "lotse"

        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title=title, intro=intro, endpoint=correct_endpoint)
            steuerlotse_step.name = "This is the one"
            steuerlotse_step._pre_handle(None)

            expected_render_info = RenderInfo(flow_title=title, step_title=title, step_intro=intro,
                                              form=None,
                                              prev_url=None,
                                              next_url=None,
                                              submit_url=url_for(endpoint=correct_endpoint,
                                                                 step=steuerlotse_step.name,
                                                                 link_overview=steuerlotse_step.has_link_overview),
                                              overview_url=None)

            self.assertEqual(expected_render_info, steuerlotse_step.render_info)

    def test_if_prev_and_next_step_set_then_render_info_is_set_correctly(self):
        title = "The Steuerlotse I"
        intro = "Not so long ago...."
        correct_endpoint = "lotse"
        prev_step = MockStartStep
        next_step = MockFormStep

        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title=title, intro=intro, endpoint=correct_endpoint,
                                               prev_step=prev_step,
                                               next_step=next_step)
            steuerlotse_step.name = "This is the one"
            steuerlotse_step._pre_handle(None)

            expected_render_info = RenderInfo(flow_title=title, step_title=title, step_intro=intro,
                                              form=None,
                                              prev_url=url_for(endpoint=correct_endpoint,
                                                               step=prev_step.name,
                                                               link_overview=steuerlotse_step.has_link_overview),
                                              next_url=url_for(endpoint=correct_endpoint,
                                                               step=next_step.name,
                                                               link_overview=steuerlotse_step.has_link_overview),
                                              submit_url=url_for(endpoint=correct_endpoint,
                                                                 step=steuerlotse_step.name,
                                                                 link_overview=steuerlotse_step.has_link_overview),
                                              overview_url=None)

            self.assertEqual(expected_render_info, steuerlotse_step.render_info)

    def test_if_overview_url_set_then_render_info_is_set_correctly(self):
        title = "The Steuerlotse I"
        intro = "Not so long ago...."
        correct_endpoint = "lotse"
        overview_url = "Everything the light touches..."

        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title=title, intro=intro, endpoint=correct_endpoint)
            steuerlotse_step.name = "This is the one"
            steuerlotse_step._pre_handle(None)

            steuerlotse_step.render_info.overview_url = overview_url

            expected_render_info = RenderInfo(flow_title=title, step_title=title, step_intro=intro,
                                              form=None,
                                              prev_url=None,
                                              next_url=None,
                                              submit_url=url_for(endpoint=correct_endpoint,
                                                                 step=steuerlotse_step.name,
                                                                 link_overview=steuerlotse_step.has_link_overview),
                                              overview_url=overview_url)

            self.assertEqual(expected_render_info, steuerlotse_step.render_info)

    def test_pre_handle_returns_stored_data_untouched(self):
        data = {'father': 'Mufasa'}

        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="lotse")
            steuerlotse_step.name = "This is the one"

            return_stored_data = steuerlotse_step._pre_handle(data)

            self.assertEqual(data, return_stored_data)


class TestSteuerlotseStepPostHandle(unittest.TestCase):

    def test_if_post_handle_called_then_return_render_result(self):
        stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="lotse")
            steuerlotse_step.name = "This is the one"
            steuerlotse_step._pre_handle(stored_data)

            with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep.render", MagicMock()) as step_render:
                post_result = steuerlotse_step._post_handle(stored_data)

                self.assertEqual(step_render.return_value, post_result)
                step_render.assert_called()

    def test_if_redirection_url_set_then_return_redirect(self):
        stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        with app.app_context() and app.test_request_context():
            steuerlotse_step = SteuerlotseStep(title="The Steuerlotse I", intro="Not so long ago....", endpoint="lotse")
            steuerlotse_step.name = "This is the one"
            steuerlotse_step._pre_handle(stored_data)

            redirect_url = url_for(endpoint="lotse", step="RedirectToThis",
                                   link_overview=steuerlotse_step.has_link_overview)
            steuerlotse_step.render_info.redirect_url = redirect_url

            with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep.render", MagicMock()) as step_render:
                post_result = steuerlotse_step._post_handle(stored_data)

            self.assertEqual(302, post_result.status_code)
            self.assertEqual(
                redirect(redirect_url).location,
                post_result.location)


class TestRedirectSteuerlotseStep(unittest.TestCase):

    def test_if_redirect_url_provided_then_return_redirect_on_specified_page(self):
        with app.app_context() and app.test_request_context():
            redirection_step = RedirectSteuerlotseStep(redirection_step_name="RedirectToThis", endpoint="lotse")

            returned_redirect = redirection_step.handle()

            self.assertEqual(302, returned_redirect.status_code)
            self.assertEqual(
                redirect(url_for(endpoint="lotse", step="RedirectToThis",
                                 link_overview=redirection_step.has_link_overview)).location,
                returned_redirect.location)


class TestSteuerlotseFormStepHandle(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint_correct = 'lotse'
        self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_post_then_return_redirect_to_next_step(self):
        next_step = MockFinalStep
        with app.app_context() and app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                method='POST') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            form_step = MockFormStep(endpoint=self.endpoint_correct, next_step=next_step)
            response = form_step.handle()

            self.assertEqual(
                redirect(
                    "/" + self.endpoint_correct + "/step/" + next_step.name
                    + "?link_overview=" + str(form_step.has_link_overview)).location,
                response.location
            )

    def test_if_not_post_then_return_render(self):
        next_step = MockFinalStep
        with app.app_context() and app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                method='GET') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            form_step = MockFormStep(endpoint=self.endpoint_correct, next_step=next_step)
            response = form_step.handle()

            self.assertEqual(200, response.status_code)
            # Check response data because that's where our Mock returns. Decode because response stores as bytestring
            self.assertEqual(form_step.title, json.loads(str(response.get_data(), 'utf-8'))[0])

    def test_update_session_data_is_called(self):
        next_step = MockFinalStep
        expected_data = {'brother': 'Luigi'}
        with app.app_context() and app.test_request_context():
            with patch('app.forms.steps.steuerlotse_step.override_session_data') as update_fun, \
                    app.app_context() and app.test_request_context(
                        path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                        method='GET') as req:
                req.session = SecureCookieSession({'form_data': create_session_form_data(expected_data)})
                form_step = MockFormStep(endpoint=self.endpoint_correct, next_step=next_step)
                form_step.handle()

                update_fun.assert_called_once_with(expected_data)

    def test_yes_no_field_content_overriden_if_empty(self):
        steps = [MockYesNoStep, MockFinalStep]
        with app.test_request_context():
            mock_yesno_step = MockYesNoStep(endpoint="lotse", next_step=MockRenderStep)
        resulting_session = run_handle(mock_yesno_step, 'POST', {'yes_no_field': 'yes'})
        resulting_session = run_handle(mock_yesno_step, 'POST', {}, resulting_session)
        self.assertEqual({'yes_no_field': None}, deserialize_session_data(resulting_session['form_data'],
                                                                        app.config['PERMANENT_SESSION_LIFETIME']))


class TestSteuerlotseStep(unittest.TestCase):

    def test_if_form_step_after_render_step_then_keep_data_from_older_form_step(self):
        endpoint_correct = "lotse"
        original_data = {'pet': 'Yoshi', 'date': '09.07.1981', 'decimal': '60.000'}

        with app.app_context() and app.test_request_context():
            first_step = MockFormWithInputStep(endpoint=endpoint_correct, next_step=MockRenderStep)
            second_step = MockRenderStep(endpoint=endpoint_correct, next_step=MockFormStep)
            third_step = MockFormStep(endpoint=endpoint_correct, next_step=MockFinalStep)

        session = run_handle(first_step, method='POST', form_data=original_data)
        session = run_handle(second_step, method='GET', session=session)
        session = run_handle(third_step, method='GET', session=session)
        self.assertTrue(set(original_data).issubset(
            set(deserialize_session_data(session['form_data'], app.config['PERMANENT_SESSION_LIFETIME']))))


def run_handle(step, method='GET', form_data=None, session=None):
    with app.app_context() and app.test_request_context(method=method) as req:
        if not form_data:
            form_data = {}
        req.request.form = ImmutableMultiDict(form_data)
        if session is not None:
            req.session = session

        step.handle()

        return req.session
