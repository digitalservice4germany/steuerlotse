import unittest

import pytest
from flask import request

from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseStringField
from app.forms.steps.step import FormStep


class MockForm(SteuerlotseBaseForm):
    string_field = SteuerlotseStringField()


class TestStripWhitespaces(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_if_string_field_then_strip_whitespaces_back(self):
        step = FormStep(form=MockForm, title='step')
        data = {'string_field': "Here is whitespace "}
        expected_output = "Here is whitespace"
        with self.app.test_request_context(method='POST', data=data):
            form = step.create_form(request, prefilled_data={})
            self.assertEqual(expected_output, form.data['string_field'])

    def test_if_string_field_then_strip_whitespaces_front(self):
        step = FormStep(form=MockForm, title='step')
        data = {'string_field': " Here is whitespace"}
        expected_output = "Here is whitespace"
        with self.app.test_request_context(method='POST', data=data):
            form = step.create_form(request, prefilled_data={})
            self.assertEqual(expected_output, form.data['string_field'])
