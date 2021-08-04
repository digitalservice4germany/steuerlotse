import unittest
from unittest.mock import patch, MagicMock

from pydantic import ValidationError

from app.model.eligibility_data import SeparatedEligibilityData, \
    NotSeparatedEligibilityData, AlimonyMarriedEligibilityData, UserANoElsterAccountEligibilityData, \
    UserBNoElsterAccountEligibilityData, DivorcedJointTaxesEligibilityData, AlimonyEligibilityData, \
    SingleUserElsterAccountEligibilityData, PensionEligibilityData, InvestmentIncomeEligibilityData, \
    CheaperCheckEligibilityData, \
    NoTaxedInvestmentIncome, NoInvestmentIncomeEligibilityData, \
    NoEmploymentIncomeEligibilityData, EmploymentIncomeEligibilityData, MarginalEmploymentEligibilityData, \
    OtherIncomeEligibilityData, ForeignCountryEligibility, MarriedJointTaxesEligibilityData, MarriedEligibilityData, \
    SingleEligibilityData, WidowedEligibilityData, DivorcedEligibilityData, MoreThanMinimalInvestmentIncome, \
    MinimalInvestmentIncome, UserAElsterAccountEligibilityData, SeparatedLivedTogetherEligibilityData, \
    SeparatedNotLivedTogetherEligibilityData, SeparatedJointTaxesEligibilityData, SeparatedNoJointTaxesEligibilityData


class TestMarriedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['widowed', 'single', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status_eligibility': invalid_marital_status}
            self.assertRaises(ValidationError, MarriedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_married_then_raise_no_validation_error(self):
        valid_data = {'marital_status_eligibility': 'married'}
        try:
            MarriedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("MarriedEligibilityData.parse_obj should not raise validation error")


class TestWidowedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_widowed_raise_validation_error(self):
        invalid_marital_statuses = ['single', 'married', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status_eligibility': invalid_marital_status}
            self.assertRaises(ValidationError, WidowedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_widowed_then_raise_no_validation_error(self):
        valid_data = {'marital_status_eligibility': 'widowed'}
        try:
            WidowedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("WidowedEligibilityData.parse_obj should not raise validation error")


class TestSingleEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['married', 'widowed', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status_eligibility': invalid_marital_status}
            self.assertRaises(ValidationError, SingleEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_single_then_raise_no_validation_error(self):
        valid_data = {'marital_status_eligibility': 'single'}
        try:
            SingleEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("SingleEligibilityData.parse_obj should not raise validation error")


class TestDivorcedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['married', 'widowed', 'single', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status_eligibility': invalid_marital_status}
            self.assertRaises(ValidationError, DivorcedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_divorced_then_raise_no_validation_error(self):
        valid_data = {'marital_status_eligibility': 'divorced'}
        try:
            DivorcedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("DivorcedEligibilityData.parse_obj should not raise validation error")


class TestSeparatedEligibilityDataEligibilityData(unittest.TestCase):

    def test_if_married_data_valid_and_separated_since_last_year_no_then_raise_validation_error(self):
        non_valid_data = {'separated_since_last_year_eligibility': 'no'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedEligibilityData.parse_obj, non_valid_data)

    def test_if_married_data_invalid_and_separated_since_last_year_yes_then_raise_validation_error(self):
        valid_data = {'separated_since_last_year_eligibility': 'yes'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, SeparatedEligibilityData.parse_obj, valid_data)

    def test_if_married_data_valid_and_separated_since_last_year_yes_then_raise_no_validation_error(self):
        valid_data = {'separated_since_last_year_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.MarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedEligibilityData.parse_obj should not raise validation error")


class TestNotSeparatedEligibilityDataEligibilityData(unittest.TestCase):

    def test_if_married_data_valid_and_separated_since_last_year_yes_then_raise_validation_error(self):
        non_valid_data = {'separated_since_last_year_eligibility': 'yes'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, NotSeparatedEligibilityData.parse_obj, non_valid_data)

    def test_if_married_data_invalid_and_separated_since_last_year_no_then_raise_validation_error(self):
        valid_data = {'separated_since_last_year_eligibility': 'no'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, NotSeparatedEligibilityData.parse_obj, valid_data)

    def test_if_married_data_valid_and_separated_since_last_year_no_then_raise_no_validation_error(self):
        valid_data = {'separated_since_last_year_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.MarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                NotSeparatedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MarriedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestSeparatedLivedTogetherEligibilityData(unittest.TestCase):

    def test_if_separated_data_valid_and_separated_lived_together_no_then_raise_validation_error(self):
        invalid_data = {'separated_lived_together_eligibility': 'no'}
        with patch('app.model.eligibility_data.SeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedLivedTogetherEligibilityData.parse_obj, invalid_data)

    def test_if_separated_data_invalid_and_separated_lived_together_yes_then_raise_validation_error(self):
        valid_data = {'separated_lived_together_eligibility': 'yes'}
        with patch('app.model.eligibility_data.SeparatedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, SeparatedLivedTogetherEligibilityData.parse_obj, valid_data)

    def test_if_separated_data_valid_and_separated_lived_together_yes_then_raise_no_validation_error(self):
        valid_data = {'separated_lived_together_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.SeparatedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedLivedTogetherEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedLivedTogetherEligibilityData.parse_obj should not raise validation error")


class TestSeparatedNotLivedTogetherEligibilityData(unittest.TestCase):

    def test_if_separated_data_valid_and_separated_lived_together_yes_then_raise_validation_error(self):
        invalid_data = {'separated_lived_together_eligibility': 'yes'}
        with patch('app.model.eligibility_data.SeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedNotLivedTogetherEligibilityData.parse_obj, invalid_data)

    def test_if_separated_data_invalid_and_separated_lived_together_no_then_raise_validation_error(self):
        valid_data = {'separated_lived_together_eligibility': 'no'}
        with patch('app.model.eligibility_data.SeparatedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, SeparatedNotLivedTogetherEligibilityData.parse_obj, valid_data)

    def test_if_separated_data_valid_and_separated_lived_together_no_then_raise_no_validation_error(self):
        valid_data = {'separated_lived_together_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.SeparatedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedNotLivedTogetherEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedNotLivedTogetherEligibilityData.parse_obj should not raise validation error")


class TestSeparatedJointTaxesEligibilityData(unittest.TestCase):

    def test_if_separated_data_valid_and_separated_joint_taxes_no_then_raise_validation_error(self):
        invalid_data = {'separated_joint_taxes_eligibility': 'no'}
        with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedJointTaxesEligibilityData.parse_obj, invalid_data)

    def test_if_separated_data_invalid_and_separated_joint_taxes_yes_then_raise_validation_error(self):
        valid_data = {'separated_joint_taxes_eligibility': 'yes'}
        with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, SeparatedJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_separated_data_valid_and_separated_joint_taxes_yes_then_raise_no_validation_error(self):
        valid_data = {'separated_joint_taxes_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestSeparatedNoJointTaxesEligibilityData(unittest.TestCase):

    def test_if_separated_data_valid_and_separated_joint_taxes_yes_then_raise_validation_error(self):
        invalid_data = {'separated_joint_taxes_eligibility': 'yes'}
        with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedNoJointTaxesEligibilityData.parse_obj, invalid_data)

    def test_if_separated_data_invalid_and_separated_joint_taxes_no_then_raise_validation_error(self):
        valid_data = {'separated_joint_taxes_eligibility': 'no'}
        with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, SeparatedNoJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_separated_data_valid_and_separated_joint_taxes_no_then_raise_no_validation_error(self):
        valid_data = {'separated_joint_taxes_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.SeparatedLivedTogetherEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedNoJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedNoJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestMarriedJointTaxesEligibilityData(unittest.TestCase):

    def test_if_not_separated_valid_and_joint_taxes_no_then_raise_validation_error(self):
        non_valid_data = {'joint_taxes_eligibility': 'no'}
        with patch('app.model.eligibility_data.NotSeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MarriedJointTaxesEligibilityData.parse_obj, non_valid_data)

    def test_if_not_separated_invalid_and_joint_taxes_yes_then_raise_validation_error(self):
        valid_data = {'joint_taxes_eligibility': 'yes'}
        with patch('app.model.eligibility_data.NotSeparatedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], NotSeparatedEligibilityData))):
            self.assertRaises(ValidationError, MarriedJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_not_separated_valid_and_joint_taxes_yes_then_raise_no_validation_error(self):
        valid_data = {'joint_taxes_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.NotSeparatedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MarriedJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MarriedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestAlimonyMarriedEligibilityData(unittest.TestCase):

    def test_if_not_separated_data_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony_eligibility': 'yes'}
        with patch('app.model.eligibility_data.MarriedJointTaxesEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SeparatedEligibilityData))):
            self.assertRaises(ValidationError, AlimonyMarriedEligibilityData.parse_obj, non_valid_data)

    def test_if_separated_data_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony_eligibility': 'yes'}
        with patch('app.model.eligibility_data.MarriedJointTaxesEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedJointTaxesEligibilityData))), \
                patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, AlimonyMarriedEligibilityData.parse_obj, non_valid_data)

    def test_if_not_and_separated_data_invalid_and_alimony_no_then_raise_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        with patch('app.model.eligibility_data.MarriedJointTaxesEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedJointTaxesEligibilityData))), \
                patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SeparatedEligibilityData))):
            self.assertRaises(ValidationError, AlimonyMarriedEligibilityData.parse_obj, valid_data)

    def test_if_not_separated_data_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.MarriedJointTaxesEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], SeparatedEligibilityData))):
                AlimonyMarriedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonyMarriedEligibilityData.parse_obj should not raise validation error")

    def test_if_separated_data_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.MarriedJointTaxesEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], MarriedJointTaxesEligibilityData))), \
                    patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.__init__',
                          MagicMock(return_value=None)):
                AlimonyMarriedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonyMarriedEligibilityData.parse_obj should not raise validation error")


class TestUserANoElsterAccountEligibilityData(unittest.TestCase):

    def test_if_alimony_married_valid_and_user_a_has_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account_eligibility': 'yes'}
        with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserANoElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_married_invalid_and_user_a_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'no'}
        with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonyMarriedEligibilityData))):
            self.assertRaises(ValidationError, UserANoElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_married_valid_and_user_a_has_elster_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                UserANoElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("UserANoElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestUserAElsterAccountEligibilityData(unittest.TestCase):

    def test_if_alimony_married_valid_and_user_a_has_elster_account_no_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account_eligibility': 'no'}
        with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserAElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_married_invalid_and_user_a_has_elster_account_yes_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'yes'}
        with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonyMarriedEligibilityData))):
            self.assertRaises(ValidationError, UserAElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_married_valid_and_user_a_has_elster_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.AlimonyMarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                UserAElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("UserANoElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestUserBNoElsterAccountEligibilityData(unittest.TestCase):

    def test_if_user_a_elster_account_valid_and_user_b_has_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_b_has_elster_account_eligibility': 'yes'}
        with patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserBNoElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_user_a_elster_account_invalid_and_user_b_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_b_has_elster_account_eligibility': 'no'}
        with patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, UserBNoElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_user_a_elster_account_valid_and_user_b_has_elster_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_b_has_elster_account_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.__init__',
                       MagicMock(return_value=None)):
                UserBNoElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("UserBNoElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestDivorcedJointTaxesEligibilityData(unittest.TestCase):

    def test_if_divorced_data_valid_and_joint_taxes_yes_then_raise_validation_error(self):
        non_valid_data = {'joint_taxes_eligibility': 'yes'}
        with patch('app.model.eligibility_data.DivorcedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, DivorcedJointTaxesEligibilityData.parse_obj, non_valid_data)

    def test_if_divorced_data_invalid_and_joint_taxes_no_then_raise_validation_error(self):
        valid_data = {'joint_taxes_eligibility': 'no'}
        with patch('app.model.eligibility_data.DivorcedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], DivorcedEligibilityData))):
            self.assertRaises(ValidationError, DivorcedJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_divorced_data_valid_and_joint_taxes_no_then_raise_no_validation_error(self):
        valid_data = {'joint_taxes_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.DivorcedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                DivorcedJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("DivorcedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestAlimonyEligibilityData(unittest.TestCase):

    def test_if_widowed_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony_eligibility': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_single_status_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony_eligibility': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_divorced_joint_taxes_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony_eligibility': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_widowed_and_single_status_and_divorced_joint_taxes_invalid_and_alimony_no_then_raise_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, valid_data)

    def test_if_widowed_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.WidowedEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
                AlimonyEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonyEligibilityData.parse_obj should not raise validation error")

    def test_if_single_status_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.WidowedEligibilityData.__init__',
                       MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                    patch('app.model.eligibility_data.SingleEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
                AlimonyEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonyEligibilityData.parse_obj should not raise validation error")

    def test_if_divorced_joint_taxes_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                    patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                    patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.__init__',
                          MagicMock(return_value=None)):
                AlimonyEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonyEligibilityData.parse_obj should not raise validation error")


class TestSingleUserElsterAccountEligibilityData(unittest.TestCase):

    def test_if_alimony_valid_and_user_a_has_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account_eligibility': 'yes'}
        with patch('app.model.eligibility_data.AlimonyEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SingleUserElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_invalid_and_user_a_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'no'}
        with patch('app.model.eligibility_data.AlimonyEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonyEligibilityData))):
            self.assertRaises(ValidationError, SingleUserElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_valid_and_user_a_has_elster_account_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.AlimonyEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SingleUserElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SingleUserElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestPensionEligibilityData(unittest.TestCase):

    def test_if_single_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension_eligibility': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserANoElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBNoElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_user_a_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension_eligibility': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBNoElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_user_b_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension_eligibility': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserANoElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_single_elster_and_user_a_elster_and_user_b_elster_invalid_and_pension_yes_then_raise_validation_error(self):
        valid_data = {'pension_eligibility': 'yes'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserANoElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBNoElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, valid_data)

    def test_if_single_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], UserANoElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBNoElsterAccountEligibilityData))):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")

    def test_if_user_a_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.__init__',
                       MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBNoElsterAccountEligibilityData))):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")

    def test_if_user_b_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserANoElsterAccountEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], UserANoElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserBNoElsterAccountEligibilityData.__init__',
                          MagicMock(return_value=None)):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")


class TestInvestmentIncome(unittest.TestCase):

    def test_if_pension_valid_and_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'investment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, InvestmentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_pension_invalid_and_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'investment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], PensionEligibilityData))):
            self.assertRaises(ValidationError, InvestmentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_pension_valid_and_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'investment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.PensionEligibilityData.__init__',
                       MagicMock(return_value=None)):
                InvestmentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("InvestmentIncomeEligibilityData.parse_obj should not raise validation error")


class TestMinimalInvestmentIncome(unittest.TestCase):

    def test_if_inv_income_valid_and_taxed_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'minimal_investment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MinimalInvestmentIncome.parse_obj, non_valid_data)

    def test_if_inv_income_invalid_and_minimal_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'minimal_investment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], InvestmentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MinimalInvestmentIncome.parse_obj, valid_data)

    def test_if_inv_income_valid_and_minimal_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'minimal_investment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MinimalInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MinimalInvestmentIncome.parse_obj should not raise validation error")


class TestMoreThanMinimalInvestmentIncome(unittest.TestCase):

    def test_if_inv_income_valid_and_minimal_investment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'minimal_investment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MoreThanMinimalInvestmentIncome.parse_obj, non_valid_data)

    def test_if_inv_income_invalid_and_minimal_investment_income_no_then_raise_validation_error(self):
        valid_data = {'minimal_investment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], InvestmentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MoreThanMinimalInvestmentIncome.parse_obj, valid_data)

    def test_if_inv_income_valid_and_minimal_investment_income_no_then_raise_no_validation_error(self):
        valid_data = {'minimal_investment_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MoreThanMinimalInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MoreThanMinimalInvestmentIncome.parse_obj should not raise validation error")


class TestNoTaxedInvestmentIncome(unittest.TestCase):

    def test_if_above_minimal_inv_income_valid_and_taxed_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'taxed_investment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, NoTaxedInvestmentIncome.parse_obj, non_valid_data)

    def test_if_above_minimal_inv_income_invalid_and_taxed_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'taxed_investment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.parse_obj',
                   MagicMock(side_effect=ValidationError([], MoreThanMinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoTaxedInvestmentIncome.parse_obj, valid_data)

    def test_if_above_minimal_inv_income_valid_and_taxed_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'taxed_investment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.__init__',
                       MagicMock(return_value=None)):
                NoTaxedInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoTaxedInvestmentIncome.parse_obj should not raise validation error")


class TestCheaperCheckEligibilityData(unittest.TestCase):

    def test_if_taxed_inv_valid_and_cheaper_check_yes_then_raise_validation_error(self):
        non_valid_data = {'cheaper_check_eligibility': 'yes'}
        with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, CheaperCheckEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_invalid_and_cheaper_check_no_then_raise_validation_error(self):
        valid_data = {'cheaper_check_eligibility': 'no'}
        with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoTaxedInvestmentIncome))):
            self.assertRaises(ValidationError, CheaperCheckEligibilityData.parse_obj, valid_data)

    def test_if_taxed_inv_valid_and_cheaper_check_no_then_raise_no_validation_error(self):
        valid_data = {'cheaper_check_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.__init__',
                       MagicMock(return_value=None)):
                CheaperCheckEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("CheaperCheckEligibilityData.parse_obj should not raise validation error")


class TestNoInvestmentIncomeEligibilityData(unittest.TestCase):

    def test_if_taxed_inv_valid_and_investment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'investment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, NoInvestmentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_invalid_and_investment_income_no_then_raise_validation_error(self):
        valid_data = {'investment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], PensionEligibilityData))):
            self.assertRaises(ValidationError, NoInvestmentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_taxed_inv_valid_and_investment_income_no_then_raise_no_validation_error(self):
        valid_data = {'investment_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.PensionEligibilityData.__init__',
                       MagicMock(return_value=None)):
                NoInvestmentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoInvestmentIncomeEligibilityData.parse_obj should not raise validation error")


class TestNoEmploymentIncomeEligibilityData(unittest.TestCase):

    def test_if_cheaper_check_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_inv_income_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_income_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_cheaper_check_and_no_inv_income_and_taxed_inv_income_invalid_and_employment_income_no_then_raise_validation_error(self):
        valid_data = {'employment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_cheaper_check_valid_and_employment_income_no_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
                NoEmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoEmploymentIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_no_inv_income_valid_and_employment_income_no_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.__init__',
                       MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
                NoEmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoEmploymentIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_taxed_inv_income_valid_and_employment_income_no_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                    patch('app.model.eligibility_data.MinimalInvestmentIncome.__init__',
                          MagicMock(return_value=None)):
                NoEmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoEmploymentIncomeEligibilityData.parse_obj should not raise validation error")


class TestEmploymentIncomeEligibilityData(unittest.TestCase):

    def test_if_cheaper_check_valid_and_employment_income_no_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_inv_income_valid_and_employment_income_no_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_income_valid_and_employment_income_no_then_raise_validation_error(self):
        non_valid_data = {'employment_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_cheaper_check_and_no_inv_income_and_taxed_inv_income_invalid_and_employment_income_yes_then_raise_validation_error(self):
        valid_data = {'employment_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_cheaper_check_valid_and_employment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
                EmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("EmploymentIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_no_inv_income_valid_and_employment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.__init__',
                       MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
                EmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("EmploymentIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_taxed_inv_income_valid_and_employment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'employment_income_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                    patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                    patch('app.model.eligibility_data.MinimalInvestmentIncome.__init__',
                          MagicMock(return_value=None)):
                EmploymentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("EmploymentIncomeEligibilityData.parse_obj should not raise validation error")


class TestMarginalEmploymentEligibilityData(unittest.TestCase):

    def test_if_employment_income_valid_and_marginal_employment_no_then_raise_validation_error(self):
        non_valid_data = {'marginal_employment_eligibility': 'no'}
        with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MarginalEmploymentEligibilityData.parse_obj, non_valid_data)

    def test_if_employment_income_invalid_and_marginal_employment_yes_then_raise_validation_error(self):
        valid_data = {'marginal_employment_eligibility': 'yes'}
        with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], EmploymentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MarginalEmploymentEligibilityData.parse_obj, valid_data)

    def test_if_employment_income_valid_and_marginal_employment_yes_then_raise_no_validation_error(self):
        valid_data = {'marginal_employment_eligibility': 'yes'}
        try:
            with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MarginalEmploymentEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MarginalEmploymentEligibilityData.parse_obj should not raise validation error")


class TestOtherIncomeEligibilityData(unittest.TestCase):

    def test_if_no_employment_valid_and_other_income_yes_then_raise_validation_error(self):
        non_valid_data = {'other_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_marginal_employ_valid_and_other_income_yes_then_raise_validation_error(self):
        non_valid_data = {'other_income_eligibility': 'yes'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoEmploymentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_and_marginal_employ_invalid_and_other_income_no_then_raise_validation_error(self):
        valid_data = {'other_income_eligibility': 'no'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoEmploymentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, valid_data)

    def test_if_no_employment_valid_and_other_income_no_then_raise_no_validation_error(self):
        valid_data = {'other_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
                OtherIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("OtherIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_marginal_employ_valid_and_other_income_no_then_raise_no_validation_error(self):
        valid_data = {'other_income_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], NoEmploymentIncomeEligibilityData))), \
                    patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.__init__',
                          MagicMock(return_value=None)):
                OtherIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("OtherIncomeEligibilityData.parse_obj should not raise validation error")


class TestForeignCountryEligibility(unittest.TestCase):

    def test_if_other_income_valid_and_foreign_country_yes_then_raise_validation_error(self):
        non_valid_data = {'foreign_country_eligibility': 'yes'}
        with patch('app.model.eligibility_data.OtherIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, ForeignCountryEligibility.parse_obj, non_valid_data)

    def test_if_other_income_invalid_and_foreign_country_no_then_raise_validation_error(self):
        valid_data = {'foreign_country_eligibility': 'no'}
        with patch('app.model.eligibility_data.OtherIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], OtherIncomeEligibilityData))):
            self.assertRaises(ValidationError, ForeignCountryEligibility.parse_obj, valid_data)

    def test_if_other_income_valid_and_foreign_country_no_then_raise_no_validation_error(self):
        valid_data = {'foreign_country_eligibility': 'no'}
        try:
            with patch('app.model.eligibility_data.OtherIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                ForeignCountryEligibility.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("ForeignCountryEligibility.parse_obj should not raise validation error")


class TestEligibilityDataInGeneral(unittest.TestCase):
    last_step_data_type = ForeignCountryEligibility

    def test_if_married_and_no_joint_taxes_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_separated_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'yes',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'yes',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_separated_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'yes',
            'separated_lived_together_eligibility': 'yes',
            'separated_joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_joint_taxes_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'yes',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_both_have_elster_account_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes',
            'user_b_has_elster_account_eligibility': 'yes',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_only_a_has_elster_account_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_widowed_and_everything_is_set_to_no_and_pension_then_parse_valid_foreign_country_data(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_everything_is_set_to_no_and_pension_then_parse_valid_foreign_country_data(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_divorced_and_joint_taxes_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'divorced',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_divorced_and_no_joint_taxes_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'divorced',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_widowed_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'widowed',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'yes',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_widowed_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'widowed',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'yes',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_divorced_and_no_joint_taxes_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'divorced',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'yes',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_divorced_and_no_joint_taxes_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'divorced',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_has_elster_account_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'no',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_has_no_pension_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'no',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_has_pension_then_raise_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_joint_taxes_and_has_no_pension_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'no',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_and_has_pension_then_raise_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'married',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'yes',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_pension_has_only_minimal_investment_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_pension_has_investment_not_taxed_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_pension_has_taxed_investment_and_wants_cheaper_check_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'yes',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_pension_has_taxed_investment_and_wants_no_cheaper_check_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_no_investment_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'no',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_no_investment_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_minimal_investment_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'no',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_minimal_investment_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_wants_no_cheaper_check_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'no',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_wants_no_cheaper_check_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes',
            'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_only_marginal_income_and_other_income_than_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'yes',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_only_marginal_income_and_no_other_income_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_no_employment_income_and_other_income_than_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'no',
            'other_income_eligibility': 'yes',
            'foreign_country_eligibility': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_no_employment_income_and_no_other_income_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_other_income_and_foreign_country_than_raise_validation_error(self):
        invalid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'no',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'yes'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_other_income_and_no_foreign_country_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status_eligibility': 'single',
            'separated_since_last_year_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no',
            'user_b_has_elster_account_eligibility': 'no',
            'joint_taxes_eligibility': 'no',
            'alimony_eligibility': 'no',
            'pension_eligibility': 'yes',
            'investment_income_eligibility': 'no',
            'minimal_investment_income_eligibility': 'yes',
            'taxed_investment_income_eligibility': 'no',
            'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'no',
            'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no',
            'foreign_country_eligibility': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_empty_data_then_raise_validation_error(self):
        invalid_data = {}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)
