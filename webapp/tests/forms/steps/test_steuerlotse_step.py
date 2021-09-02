import json
import unittest
from unittest.mock import patch, MagicMock, call

import pytest
from flask import url_for
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.routing import BuildError
from werkzeug.utils import redirect

from app.forms.flows.multistep_flow import RenderInfo
from app.forms.steps.steuerlotse_step import SteuerlotseStep, \
    RedirectSteuerlotseStep, FormSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormStep, \
    MockRenderStep, MockYesNoStep
from tests.utils import create_session_form_data


class TestSteuerlotseStepInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current link_overview is set from request
        self.req.request.args = {'link_overview': "True"}

        step = SteuerlotseStep(endpoint="WhereItAllStarts", header_title=None, stored_data=None, overview_step=None,
                                default_data=None, prev_step=None, next_step=None)

        self.assertTrue(step.has_link_overview)

        self.req.request.args = {'link_overview': "False"}

        step = SteuerlotseStep(endpoint="WhereItAllStarts", header_title=None, stored_data=None, overview_step=None,
                                default_data=None, prev_step=None, next_step=None)

        self.assertFalse(step.has_link_overview)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        # Only link_overview and session are set from request
        step = SteuerlotseStep(endpoint="WhereItAllStarts", header_title=None, stored_data=None, overview_step=None,
                                default_data=None, prev_step=None, next_step=None)

        self.assertFalse(step.has_link_overview)


class TestSteuerlotseStepUrlForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    @staticmethod
    def helper_build_test_url(endpoint, step):
        return "/" + endpoint + "/step/" + step.name

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]

        self.endpoint_correct = "lotse"
        self.endpoint_incorrect = "IT_IS_A_TRAP"
        self.correct_session = "C3PO"
        self.incorrect_session = "r2D2"
        self.set_link_overview = True
        self.expected_url_params_if_attribute_set = "?link_overview=" + str(self.set_link_overview)
        self.empty_url_params = ""

        self.steuerlotse_step_with_overlink_view = SteuerlotseStep(endpoint=self.endpoint_correct,
                                                                    header_title=None, stored_data=None,
                                                                    overview_step=None,
                                                                    default_data=None, prev_step=None,
                                                                    next_step=None)
        self.steuerlotse_step_with_overlink_view.has_link_overview = True

    def test_if_step_given_and_attributes_correct_then_return_correct_url(self):
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
        steuerlotse_step = SteuerlotseStep(endpoint=self.endpoint_correct, header_title=None, stored_data=None,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        created_url = steuerlotse_step.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=False"
        self.assertEqual(expected_url, created_url)

    def test_if_attributes_correct_then_correct_url(self):
        created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                    MockStartStep) + self.expected_url_params_if_attribute_set
        self.assertEqual(expected_url, created_url)

    def test_if_link_overview_param_set_then_used_in_url(self):
        self.req.request.args = {'link_overview': "True"}
        steuerlotse_step = SteuerlotseStep(endpoint=self.endpoint_correct, header_title=None, stored_data=None,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        created_url = steuerlotse_step.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=True"
        self.assertEqual(expected_url, created_url)

        self.req.request.args = {'link_overview': "False"}
        steuerlotse_step = SteuerlotseStep(endpoint=self.endpoint_correct, header_title=None, stored_data=None,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        created_url = steuerlotse_step.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=False"
        self.assertEqual(expected_url, created_url)

    def test_if_incorrect_endpoint_then_throw_error(self):
        steuerlotse_incorrect_endpoint = SteuerlotseStep(endpoint="IncorrectEndpoint", header_title=None,
                                                            stored_data=None,
                                                            overview_step=None, default_data=None, prev_step=None,
                                                            next_step=None)
        self.assertRaises(BuildError, steuerlotse_incorrect_endpoint.url_for_step, MockStartStep.name)

    def test_if_additional_attr_provided_then_append_to_url(self):
        created_url = self.steuerlotse_step_with_overlink_view.url_for_step(MockStartStep.name,
                                                                            additional_attr1="did_not_expect",
                                                                            additional_attr2="to_see_you_here")
        expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                    MockStartStep) + self.expected_url_params_if_attribute_set + \
                        "&additional_attr1=did_not_expect" \
                        "&additional_attr2=to_see_you_here"
        self.assertEqual(expected_url, created_url)


class TestSteuerlotseStepHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_calls_methods_in_correct_order(self):
        steuerlotse_step = SteuerlotseStep(endpoint="WhereItAllStarts", header_title=None, stored_data=None,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        with (
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._pre_handle") as mock_pre_handle,
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._main_handle") as mock_main_handle,
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._post_handle") as mock_post_handle
        ):
            call_order = MagicMock()
            call_order.attach_mock(mock_pre_handle, "mock_pre_handle")
            call_order.attach_mock(mock_main_handle, "mock_main_handle")
            call_order.attach_mock(mock_post_handle, "mock_post_handle")

            steuerlotse_step.handle()
            call_order.assert_has_calls(
                [call.mock_pre_handle(), call.mock_main_handle(), call.mock_post_handle()])

    def test_handle_returns_result_from_post_handle(self):
        post_handle_stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        steuerlotse_step = SteuerlotseStep(endpoint="WhereItAllStarts", header_title=None, stored_data=None,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        with (
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._pre_handle"),
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._main_handle"),
            patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._post_handle", MagicMock(return_value=post_handle_stored_data))
        ):
            handle_result = steuerlotse_step.handle()
            self.assertEqual(post_handle_stored_data, handle_result)


class TestSteuerlotseStepPreHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_no_prev_next_step_set_then_render_info_is_set_correctly(self):
        correct_endpoint = "lotse"

        steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, header_title=None, stored_data=None, overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        steuerlotse_step.name = "This is the one"
        steuerlotse_step._pre_handle()

        expected_render_info = RenderInfo(step_title=steuerlotse_step.title, step_intro=steuerlotse_step.intro,
                                            form=None, prev_url=None,
                                            next_url=None, submit_url=url_for(endpoint=correct_endpoint,
                                                                            step=steuerlotse_step.name,
                                                                            link_overview=steuerlotse_step.has_link_overview),
                                            overview_url=None)

        self.assertEqual(expected_render_info, steuerlotse_step.render_info)

    def test_if_prev_and_next_step_set_then_render_info_is_set_correctly(self):
        correct_endpoint = "lotse"
        prev_step = MockStartStep
        next_step = MockFormStep

        steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, stored_data=None,
                                            prev_step=prev_step,
                                            next_step=next_step, header_title=None, overview_step=None,
                                            default_data=None)
        steuerlotse_step.name = "This is the one"
        steuerlotse_step._pre_handle()

        expected_render_info = RenderInfo(step_title=steuerlotse_step.title, step_intro=steuerlotse_step.intro,
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

    def test_render_info_is_set_correctly(self):
        correct_endpoint = "lotse"
        overview_step = MockFinalStep

        self.req.request.args = {'link_overview': "True"}
        overview_url = url_for(endpoint=correct_endpoint, step=overview_step.name, link_overview="True")
        steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, overview_step=overview_step,
                                            header_title=None, stored_data=None,
                                            default_data=None, prev_step=None, next_step=None)
        steuerlotse_step.name = "This is the one"
        expected_render_info = RenderInfo(step_title=steuerlotse_step.title, step_intro=steuerlotse_step.intro,
                                            form=None, prev_url=None,
                                            next_url=None, submit_url=url_for(endpoint=correct_endpoint,
                                                                            step=steuerlotse_step.name,
                                                                            link_overview=steuerlotse_step.has_link_overview),
                                            overview_url=overview_url)

        steuerlotse_step._pre_handle()

        self.assertEqual(expected_render_info, steuerlotse_step.render_info)

    def test_pre_handle_leaves_stored_data_untouched(self):
        data = {'father': 'Mufasa'}

        steuerlotse_step = SteuerlotseStep(endpoint="lotse", header_title=None, stored_data=data,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        steuerlotse_step.name = "This is the one"

        steuerlotse_step._pre_handle()

        self.assertEqual(data, steuerlotse_step.stored_data)

    def test_if_title_multiple_set_and_number_of_users_is_2_then_set_render_info_title_to_multiple(self):
        correct_endpoint = "lotse"
        overview_step = MockFinalStep
        correct_multiple_title = "We are more than one"

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=2)):
            self.req.request.args = {'link_overview': "True"}
            overview_url = url_for(endpoint=correct_endpoint, step=overview_step.name, link_overview="True")
            steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, overview_step=overview_step,
                                               header_title=None, stored_data=None,
                                               default_data=None, prev_step=None, next_step=None)
            steuerlotse_step.title_multiple = correct_multiple_title
            steuerlotse_step.name = "This is the one"

            steuerlotse_step._pre_handle()

            self.assertEqual(correct_multiple_title, steuerlotse_step.render_info.step_title)

    def test_if_title_multiple_set_and_number_of_users_is_1_then_set_render_info_title_to_single(self):
        correct_endpoint = "lotse"
        overview_step = MockFinalStep
        correct_single_title = "We are only one"
        correct_multiple_title = "We are more than one"

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=1)):
            self.req.request.args = {'link_overview': "True"}
            overview_url = url_for(endpoint=correct_endpoint, step=overview_step.name, link_overview="True")
            steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, overview_step=overview_step,
                                               header_title=None, stored_data=None,
                                               default_data=None, prev_step=None, next_step=None)
            steuerlotse_step.title = correct_single_title
            steuerlotse_step.title_multiple = correct_multiple_title
            steuerlotse_step.name = "This is the one"

            steuerlotse_step._pre_handle()

            self.assertEqual(correct_single_title, steuerlotse_step.render_info.step_title)

    def test_if_intro_multiple_set_and_number_of_users_is_2_then_set_render_info_intro_to_multiple(self):
        correct_endpoint = "lotse"
        overview_step = MockFinalStep
        correct_multiple_intro = "We are more than one"

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=2)):
            self.req.request.args = {'link_overview': "True"}
            overview_url = url_for(endpoint=correct_endpoint, step=overview_step.name, link_overview="True")
            steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, overview_step=overview_step,
                                               header_title=None, stored_data=None,
                                               default_data=None, prev_step=None, next_step=None)
            steuerlotse_step.intro_multiple = correct_multiple_intro
            steuerlotse_step.name = "This is the one"

            steuerlotse_step._pre_handle()

            self.assertEqual(correct_multiple_intro, steuerlotse_step.render_info.step_intro)

    def test_if_intro_multiple_set_and_number_of_users_is_1_then_set_render_info_intro_to_single(self):
        correct_endpoint = "lotse"
        overview_step = MockFinalStep
        correct_single_intro = "We are only one"
        correct_multiple_intro = "We are more than one"

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=1)):
            self.req.request.args = {'link_overview': "True"}
            overview_url = url_for(endpoint=correct_endpoint, step=overview_step.name, link_overview="True")
            steuerlotse_step = SteuerlotseStep(endpoint=correct_endpoint, overview_step=overview_step,
                                               header_title=None, stored_data=None,
                                               default_data=None, prev_step=None, next_step=None)
            steuerlotse_step.intro = correct_single_intro
            steuerlotse_step.intro_multiple = correct_multiple_intro
            steuerlotse_step.name = "This is the one"

            steuerlotse_step._pre_handle()

            self.assertEqual(correct_single_intro, steuerlotse_step.render_info.step_intro)


class TestSteuerlotseStepPostHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_post_handle_called_then_return_render_result(self):
        stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        steuerlotse_step = SteuerlotseStep(endpoint="lotse", header_title=None, stored_data=None, overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        steuerlotse_step.name = "This is the one"
        steuerlotse_step._pre_handle()

        with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep.render", MagicMock()) as step_render:
            post_result = steuerlotse_step._post_handle()

            self.assertEqual(step_render.return_value, post_result)
            step_render.assert_called()

    def test_if_redirection_url_set_then_return_redirect(self):
        stored_data = {'location': "Spiro's tower", 'attacker': 'Mulch Diggums', 'target': 'C Cube'}
        steuerlotse_step = SteuerlotseStep(endpoint="lotse", header_title=None, stored_data=stored_data,
                                            overview_step=None,
                                            default_data=None, prev_step=None, next_step=None)
        steuerlotse_step.name = "This is the one"
        steuerlotse_step._pre_handle()

        redirect_url = url_for(endpoint="lotse", step="RedirectToThis",
                                link_overview=steuerlotse_step.has_link_overview)
        steuerlotse_step.render_info.redirect_url = redirect_url

        with patch("app.forms.steps.steuerlotse_step.SteuerlotseStep.render", MagicMock()):
            # We need to patch this because the render function in the SteuerlotseStep is not implemented but
            # called by _post_handle
            post_result = steuerlotse_step._post_handle()

        self.assertEqual(302, post_result.status_code)
        self.assertEqual(
            redirect(redirect_url).location,
            post_result.location)


class TestRedirectSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_redirect_url_provided_then_return_redirect_on_specified_page(self):
        redirection_step = RedirectSteuerlotseStep(redirection_step_name="RedirectToThis", endpoint="lotse")

        returned_redirect = redirection_step.handle()

        self.assertEqual(302, returned_redirect.status_code)
        self.assertEqual(
            redirect(url_for(endpoint="lotse", step="RedirectToThis",
                                link_overview=redirection_step.has_link_overview)).location,
            returned_redirect.location)


class TestSteuerlotseFormStepHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self) -> None:
        self.endpoint_correct = 'lotse'
        self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_post_then_return_redirect_to_next_step(self):
        next_step = MockFinalStep
        with self.app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                method='POST') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            form_step = MockFormStep(endpoint=self.endpoint_correct, stored_data={}, next_step=next_step)
            response = form_step.handle()

            self.assertEqual(
                redirect(
                    "/" + self.endpoint_correct + "/step/" + next_step.name
                    + "?link_overview=" + str(form_step.has_link_overview)).location,
                response.location
            )

    def test_if_not_post_then_return_render(self):
        next_step = MockFinalStep
        with self.app.test_request_context(
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
        with self.app.test_request_context():
            with patch('app.forms.steps.steuerlotse_step.override_session_data') as update_fun, \
                    self.app.test_request_context(
                        path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                        method='GET') as req:
                form_step = MockFormStep(endpoint=self.endpoint_correct, stored_data=expected_data, next_step=next_step)
                form_step.handle()

                update_fun.assert_called_once_with(expected_data, form_step.session_data_identifier)

    def test_yes_no_field_content_overriden_if_empty(self):
        with self.app.test_request_context(method='POST') as req:
            req.request.form = ImmutableMultiDict({'yes_no_field': 'yes'})
            mock_yesno_step = MockYesNoStep(endpoint="lotse", stored_data={}, next_step=MockRenderStep)
            mock_yesno_step.handle()
            data_after_first_handle = mock_yesno_step.stored_data

        with self.app.test_request_context(method='POST') as req:
            req.request.form = ImmutableMultiDict({})
            mock_yesno_step = MockYesNoStep(endpoint="lotse", stored_data=data_after_first_handle,
                                            next_step=MockRenderStep)
            mock_yesno_step.handle()
            data_after_second_handle = mock_yesno_step.stored_data

        self.assertEqual({'yes_no_field': None}, data_after_second_handle)


class TestFormSteuerlotseStepCreateForm(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_multiple_form_and_is_multiple_user_then_return_multiple_form(self):
        self.req.form = MagicMock()
        form_step = FormSteuerlotseStep(endpoint='lotse', header_title=None, stored_data={}, form=MagicMock())
        form_multiple = MagicMock()
        form_multiple_constructor = MagicMock(return_value=form_multiple)
        form_step.form_multiple = form_multiple_constructor

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=2)):
            created_form = form_step.create_form(self.req, {})

        form_multiple_constructor.assert_called_once()
        self.assertEqual(form_multiple, created_form)

    def test_if_multiple_form_is_none_and_is_multiple_user_then_return_single_form(self):
        self.req.form = MagicMock()
        form_step = FormSteuerlotseStep(endpoint='lotse', header_title=None, stored_data={}, form=MagicMock())
        form_single = MagicMock()
        form_single_constructor = MagicMock(return_value=form_single)
        form_step.form = form_single_constructor
        form_step.form_multiple = None

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=2)):
            created_form = form_step.create_form(self.req, {})

        form_single_constructor.assert_called_once()
        self.assertEqual(form_single, created_form)

    def test_if_multiple_form_and_not_multiple_user_then_return_single_form(self):
        self.req.form = MagicMock()
        form_step = FormSteuerlotseStep(endpoint='lotse', header_title=None, stored_data={}, form=MagicMock())
        form_single = MagicMock()
        form_single_constructor = MagicMock(return_value=form_single)
        form_step.form = form_single_constructor

        with patch('app.forms.steps.steuerlotse_step.SteuerlotseStep.number_of_users', MagicMock(return_value=1)):
            created_form = form_step.create_form(self.req, {})

        form_single_constructor.assert_called_once()
        self.assertEqual(form_single, created_form)


class TestFormSteuerlotseStepDeleteDependentData(unittest.TestCase):

    def setUp(self):
        self.example_data = {
            'animal': 'butterfly',
            'animagus': 'stag',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }

    def test_single_matching_prefix_deleted(self):
        expected_data = {
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['ani'])
        self.assertEqual(expected_data, returned_data)

    def test_single_matching_postfix_deleted(self):
        expected_data = {
            'animal': 'butterfly',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=['us'])
        self.assertEqual(expected_data, returned_data)

    def test_single_matching_pre_and_postfix_deleted(self):
        expected_data = {
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['ani'], post_fixes=['us'])
        self.assertEqual(expected_data, returned_data)

    def test_if_single_complete_matching_prefix_then_item_deleted(self):
        expected_data = {
            'animal': 'butterfly',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['animagus'])
        self.assertEqual(expected_data, returned_data)

    def test_if_single_complete_matching_postfix_then_item_deleted(self):
        expected_data = {
            'animal': 'butterfly',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=['animagus'])
        self.assertEqual(expected_data, returned_data)

    def test_if_single_complete_matching_pre_and_postfix_then_item_deleted(self):
        expected_data = {
            'animal': 'butterfly',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['animagus'], post_fixes=['animagus'])
        self.assertEqual(expected_data, returned_data)

    def test_multiple_matching_prefix_deleted(self):
        expected_data = {
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['ani', 'another'])
        self.assertEqual(expected_data, returned_data)

    def test_multiple_matching_postfix_deleted(self):
        expected_data = {
            'animal': 'butterfly',
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=['us', 'another_animal'])
        self.assertEqual(expected_data, returned_data)

    def test_multiple_matching_pre_and_postfix_deleted(self):
        expected_data = {
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['ani', 'another'], post_fixes=['us', 'another_animal'])
        self.assertEqual(expected_data, returned_data)

    def test_if_multiple_complete_matching_prefix_then_items_deleted(self):
        expected_data = {
            'animagus': 'stag',
            'yet_another_animal': 'penguin'
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['animal', 'another_animal'])
        self.assertEqual(expected_data, returned_data)

    def test_if_multiple_complete_matching_postfix_then_items_deleted(self):
        expected_data = {
            'animal': 'butterfly',
            'another_animal': 'pangolin',
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=['animagus', 'yet_another_animal'])
        self.assertEqual(expected_data, returned_data)

    def test_if_multiple_complete_matching_pre_and_postfix_then_items_deleted(self):
        expected_data = {
        }
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['animal', 'another_animal'], post_fixes=['animagus', 'yet_another_animal'])
        self.assertEqual(expected_data, returned_data)

    def test_if_prefixes_empty_list_then_nothing_is_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=[])
        self.assertEqual(self.example_data, returned_data)

    def test_if_postfixes_empty_list_then_nothing_is_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=[])
        self.assertEqual(self.example_data, returned_data)

    def test_if_prefixes_and_postfixes_empty_list_then_nothing_is_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=[], post_fixes=[])
        self.assertEqual(self.example_data, returned_data)

    def test_non_matching_prefixes_not_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['plant'])
        self.assertEqual(self.example_data, returned_data)

    def test_non_matching_postfixes_not_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), post_fixes=['plant'])
        self.assertEqual(self.example_data, returned_data)

    def test_non_matching_prefixes_and_postfixes_not_deleted(self):
        returned_data = FormSteuerlotseStep._delete_dependent_data(self.example_data.copy(), pre_fixes=['plant'], post_fixes=['plant'])
        self.assertEqual(self.example_data, returned_data)
