from app.elster_client.elster_errors import ElsterInvalidTaxNumberError
from flask_babel import lazy_gettext as _l


class TestElsterInvalidTaxNumberError:

    def test_set_validation_problems_correctly(self):
        expected_validation_problems = [_l('form.lotse.input_invalid.InvalidTaxNumber')]
        error = ElsterInvalidTaxNumberError()
        assert error.validation_problems == expected_validation_problems
