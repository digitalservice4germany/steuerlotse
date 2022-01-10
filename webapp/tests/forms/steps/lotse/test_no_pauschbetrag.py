from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from app.forms.steps.lotse.merkzeichen import HasMerkzeichenPersonBPrecondition
from app.forms.steps.lotse.no_pauschbetrag import HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition, \
    HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition
    

class TestHasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                    MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_zero_and_fahrkostenpauschbetrag_return_number_other_than_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                    MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_number_other_than_zero_and_fahrkostenpauschbetrag_return_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                    MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschale_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})


class TestHasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
        patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_zero_and_fahrkostenpauschbetrag_return_number_other_than_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                    MagicMock(return_value=1)):
                with pytest.raises(ValidationError):
                    HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_number_other_than_zero_and_fahrkostenpauschbetrag_return_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                    MagicMock(return_value=0)):
                with pytest.raises(ValidationError):
                    HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschale_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrkostenpauschale',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})