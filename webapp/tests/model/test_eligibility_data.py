import unittest
from unittest.mock import patch, MagicMock

from pydantic import ValidationError

from app.model.eligibility_data import LongSeparateLivingEligibilityData, \
    ShortSeparateLivingEligibilityData, AlimonySeparatedEligibilityData, UserAElsterAccountEligibilityData, \
    UserBElsterAccountEligibilityData, DivorcedJointTaxesEligibilityData, AlimonyEligibilityData, \
    SingleUserElsterAccountEligibilityData, PensionEligibilityData, InvestmentIncomeEligibilityData, \
    CheaperCheckEligibilityData, \
    NoTaxedInvestmentIncome, NoInvestmentIncomeEligibilityData, \
    NoEmploymentIncomeEligibilityData, EmploymentIncomeEligibilityData, MarginalEmploymentEligibilityData, \
    OtherIncomeEligibilityData, ForeignCountryEligibility, SeparatedJointTaxesEligibilityData, MarriedEligibilityData, \
    SingleEligibilityData, WidowedEligibilityData, DivorcedEligibilityData, MoreThanMinimalInvestmentIncome, \
    MinimalInvestmentIncome


class TestMarriedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['widowed', 'single', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status': invalid_marital_status}
            self.assertRaises(ValidationError, MarriedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_married_then_raise_no_validation_error(self):
        valid_data = {'marital_status': 'married'}
        try:
            MarriedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("FamilienStandEligibilityData.parse_obj should not raise validation error")


class TestWidowedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_widowed_raise_validation_error(self):
        invalid_marital_statuses = ['single', 'married', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status': invalid_marital_status}
            self.assertRaises(ValidationError, WidowedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_widowed_then_raise_no_validation_error(self):
        valid_data = {'marital_status': 'widowed'}
        try:
            WidowedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("FamilienStandEligibilityData.parse_obj should not raise validation error")


class TestSingleEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['married', 'widowed', 'divorced', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status': invalid_marital_status}
            self.assertRaises(ValidationError, SingleEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_single_then_raise_no_validation_error(self):
        valid_data = {'marital_status': 'single'}
        try:
            SingleEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("FamilienStandEligibilityData.parse_obj should not raise validation error")


class TestDivorcedEligibilityData(unittest.TestCase):

    def test_if_marital_status_not_married_raise_validation_error(self):
        invalid_marital_statuses = ['married', 'widowed', 'single', 'INVALID']
        for invalid_marital_status in invalid_marital_statuses:
            non_valid_data = {'marital_status': invalid_marital_status}
            self.assertRaises(ValidationError, DivorcedEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_divorced_then_raise_no_validation_error(self):
        valid_data = {'marital_status': 'divorced'}
        try:
            DivorcedEligibilityData.parse_obj(valid_data)
        except ValidationError:
            self.fail("FamilienStandEligibilityData.parse_obj should not raise validation error")


class TestLongSeparateLivingEligibilityData(unittest.TestCase):

    def test_if_marital_status_valid_and_separated_since_last_year_no_then_raise_validation_error(self):
        non_valid_data = {'separated_since_last_year': 'no'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, LongSeparateLivingEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_invalid_and_separated_since_last_year_yes_then_raise_validation_error(self):
        valid_data = {'separated_since_last_year': 'yes'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, LongSeparateLivingEligibilityData.parse_obj, valid_data)

    def test_if_marital_status_valid_and_separated_since_last_year_yes_then_raise_no_validation_error(self):
        valid_data = {'separated_since_last_year': 'yes'}
        try:
            with patch('app.model.eligibility_data.MarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                LongSeparateLivingEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("LongSeparateLivingEligibilityData.parse_obj should not raise validation error")


class TestShortSeparateLivingEligibilityData(unittest.TestCase):

    def test_if_marital_status_valid_and_separated_since_last_year_yes_then_raise_validation_error(self):
        non_valid_data = {'separated_since_last_year': 'yes'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, ShortSeparateLivingEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_invalid_and_separated_since_last_year_no_then_raise_validation_error(self):
        valid_data = {'separated_since_last_year': 'no'}
        with patch('app.model.eligibility_data.MarriedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], MarriedEligibilityData))):
            self.assertRaises(ValidationError, ShortSeparateLivingEligibilityData.parse_obj, valid_data)

    def test_if_marital_status_valid_and_separated_since_last_year_no_then_raise_no_validation_error(self):
        valid_data = {'separated_since_last_year': 'no'}
        try:
            with patch('app.model.eligibility_data.MarriedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                ShortSeparateLivingEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestSeparatedJointTaxesEligibilityData(unittest.TestCase):

    def test_if_marital_status_valid_and_joint_taxes_no_then_raise_validation_error(self):
        non_valid_data = {'joint_taxes': 'no'}
        with patch('app.model.eligibility_data.ShortSeparateLivingEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SeparatedJointTaxesEligibilityData.parse_obj, non_valid_data)

    def test_if_marital_status_invalid_and_joint_taxes_yes_then_raise_validation_error(self):
        valid_data = {'joint_taxes': 'yes'}
        with patch('app.model.eligibility_data.ShortSeparateLivingEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], ShortSeparateLivingEligibilityData))):
            self.assertRaises(ValidationError, SeparatedJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_marital_status_valid_and_joint_taxes_yes_then_raise_no_validation_error(self):
        valid_data = {'joint_taxes': 'yes'}
        try:
            with patch('app.model.eligibility_data.ShortSeparateLivingEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SeparatedJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SeparatedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestAlimonySeparatedEligibilityData(unittest.TestCase):

    def test_if_short_separate_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony': 'yes'}
        with patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.LongSeparateLivingEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], LongSeparateLivingEligibilityData))):
            self.assertRaises(ValidationError, AlimonySeparatedEligibilityData.parse_obj, non_valid_data)

    def test_if_long_separate_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony': 'yes'}
        with patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SeparatedJointTaxesEligibilityData))), \
                patch('app.model.eligibility_data.LongSeparateLivingEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, AlimonySeparatedEligibilityData.parse_obj, non_valid_data)

    def test_if_short_and_long_separate_invalid_and_alimony_no_then_raise_validation_error(self):
        valid_data = {'alimony': 'no'}
        with patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SeparatedJointTaxesEligibilityData))), \
                patch('app.model.eligibility_data.LongSeparateLivingEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], LongSeparateLivingEligibilityData))):
            self.assertRaises(ValidationError, AlimonySeparatedEligibilityData.parse_obj, valid_data)

    def test_if_short_separate_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony': 'no'}
        try:
            with patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.LongSeparateLivingEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], LongSeparateLivingEligibilityData))):
                AlimonySeparatedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonySeparatedEligibilityData.parse_obj should not raise validation error")

    def test_if_long_separate_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony': 'no'}
        try:
            with patch('app.model.eligibility_data.SeparatedJointTaxesEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], SeparatedJointTaxesEligibilityData))), \
                    patch('app.model.eligibility_data.LongSeparateLivingEligibilityData.__init__',
                          MagicMock(return_value=None)):
                AlimonySeparatedEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("AlimonySeparatedEligibilityData.parse_obj should not raise validation error")


class TestUserAElsterAccountEligibilityData(unittest.TestCase):

    def test_if_alimony_separated_valid_and_user_a_has_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account': 'yes'}
        with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserAElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_separated_invalid_and_user_a_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'no'}
        with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonySeparatedEligibilityData))):
            self.assertRaises(ValidationError, UserAElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_separated_valid_and_user_a_has_elster_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'no'}
        try:
            with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                UserAElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("UserAElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestUserBElsterAccountEligibilityData(unittest.TestCase):

    def test_if_alimony_separated_valid_and_user_b_has_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account': 'yes', 'user_b_has_elster_account': 'yes'}
        with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserBElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_separated_valid_and_user_a_and_user_b_have_elster_account_yes_then_raise_validation_error(self):
        non_valid_data = {'user_a_has_elster_account': 'no', 'user_b_has_elster_account': 'no'}
        with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, UserBElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_user_a_elster_invalid_and_user_b_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'yes', 'user_b_has_elster_account': 'no'}
        with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonySeparatedEligibilityData))):
            self.assertRaises(ValidationError, UserBElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_separated_valid_and_user_b_has_elster_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'yes', 'user_b_has_elster_account': 'no'}
        try:
            with patch('app.model.eligibility_data.AlimonySeparatedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                UserBElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("UserBElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestDivorcedJointTaxesEligibilityData(unittest.TestCase):

    def test_if_alimony_separated_valid_and_joint_taxes_yes_then_raise_validation_error(self):
        non_valid_data = {'joint_taxes': 'yes'}
        with patch('app.model.eligibility_data.DivorcedEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, DivorcedJointTaxesEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_separated_invalid_and_joint_taxes_no_then_raise_validation_error(self):
        valid_data = {'joint_taxes': 'no'}
        with patch('app.model.eligibility_data.DivorcedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], DivorcedEligibilityData))):
            self.assertRaises(ValidationError, DivorcedJointTaxesEligibilityData.parse_obj, valid_data)

    def test_if_alimony_separated_valid_and_joint_taxes_no_then_raise_no_validation_error(self):
        valid_data = {'joint_taxes': 'no'}
        try:
            with patch('app.model.eligibility_data.DivorcedEligibilityData.__init__',
                       MagicMock(return_value=None)):
                DivorcedJointTaxesEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("DivorcedJointTaxesEligibilityData.parse_obj should not raise validation error")


class TestAlimonyEligibilityData(unittest.TestCase):

    def test_if_widowed_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_single_status_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_divorced_joint_taxes_valid_and_alimony_yes_then_raise_validation_error(self):
        non_valid_data = {'alimony': 'yes'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, non_valid_data)

    def test_if_widowed_and_single_status_and_divorced_joint_taxes_invalid_and_alimony_no_then_raise_validation_error(self):
        valid_data = {'alimony': 'no'}
        with patch('app.model.eligibility_data.WidowedEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], WidowedEligibilityData))), \
                patch('app.model.eligibility_data.SingleEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], SingleEligibilityData))), \
                patch('app.model.eligibility_data.DivorcedJointTaxesEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], DivorcedJointTaxesEligibilityData))):
            self.assertRaises(ValidationError, AlimonyEligibilityData.parse_obj, valid_data)

    def test_if_widowed_valid_and_alimony_no_then_raise_no_validation_error(self):
        valid_data = {'alimony': 'no'}
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
        valid_data = {'alimony': 'no'}
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
        valid_data = {'alimony': 'no'}
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
        non_valid_data = {'user_a_has_elster_account': 'yes'}
        with patch('app.model.eligibility_data.AlimonyEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, SingleUserElsterAccountEligibilityData.parse_obj, non_valid_data)

    def test_if_alimony_invalid_and_user_a_has_elster_account_no_then_raise_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'no'}
        with patch('app.model.eligibility_data.AlimonyEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], AlimonyEligibilityData))):
            self.assertRaises(ValidationError, SingleUserElsterAccountEligibilityData.parse_obj, valid_data)

    def test_if_alimony_valid_and_user_a_has_elster_account_account_no_then_raise_no_validation_error(self):
        valid_data = {'user_a_has_elster_account': 'no'}
        try:
            with patch('app.model.eligibility_data.AlimonyEligibilityData.__init__',
                       MagicMock(return_value=None)):
                SingleUserElsterAccountEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("SingleUserElsterAccountEligibilityData.parse_obj should not raise validation error")


class TestPensionEligibilityData(unittest.TestCase):

    def test_if_single_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_user_a_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_user_b_elster_valid_and_pension_no_then_raise_validation_error(self):
        non_valid_data = {'pension': 'no'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, non_valid_data)

    def test_if_single_elster_and_user_a_elster_and_user_b_elster_invalid_and_pension_yes_then_raise_validation_error(self):
        valid_data = {'pension': 'yes'}
        with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBElsterAccountEligibilityData))):
            self.assertRaises(ValidationError, PensionEligibilityData.parse_obj, valid_data)

    def test_if_single_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBElsterAccountEligibilityData))):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")

    def test_if_user_a_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.__init__',
                       MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], UserBElsterAccountEligibilityData))):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")

    def test_if_user_b_elster_valid_and_pension_yes_then_raise_no_validation_error(self):
        valid_data = {'pension': 'yes'}
        try:
            with patch('app.model.eligibility_data.SingleUserElsterAccountEligibilityData.parse_obj',
                       MagicMock(side_effect=ValidationError([], SingleUserElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserAElsterAccountEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], UserAElsterAccountEligibilityData))), \
                    patch('app.model.eligibility_data.UserBElsterAccountEligibilityData.__init__',
                          MagicMock(return_value=None)):
                PensionEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("PensionEligibilityData.parse_obj should not raise validation error")


class TestInvestmentIncome(unittest.TestCase):

    def test_if_pension_valid_and_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'investment_income': 'no'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, InvestmentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_pension_invalid_and_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'investment_income': 'yes'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], PensionEligibilityData))):
            self.assertRaises(ValidationError, InvestmentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_pension_valid_and_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'investment_income': 'yes'}
        try:
            with patch('app.model.eligibility_data.PensionEligibilityData.__init__',
                       MagicMock(return_value=None)):
                InvestmentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("InvestmentIncomeEligibilityData.parse_obj should not raise validation error")


class TestMinimalInvestmentIncome(unittest.TestCase):

    def test_if_inv_income_valid_and_taxed_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'minimal_investment_income': 'no'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MinimalInvestmentIncome.parse_obj, non_valid_data)

    def test_if_inv_income_invalid_and_minimal_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'minimal_investment_income': 'yes'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], InvestmentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MinimalInvestmentIncome.parse_obj, valid_data)

    def test_if_inv_income_valid_and_minimal_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'minimal_investment_income': 'yes'}
        try:
            with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MinimalInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MinimalInvestmentIncome.parse_obj should not raise validation error")


class TestMoreThanMinimalInvestmentIncome(unittest.TestCase):

    def test_if_inv_income_valid_and_minimal_investment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'minimal_investment_income': 'yes'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MoreThanMinimalInvestmentIncome.parse_obj, non_valid_data)

    def test_if_inv_income_invalid_and_minimal_investment_income_no_then_raise_validation_error(self):
        valid_data = {'minimal_investment_income': 'no'}
        with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], InvestmentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MoreThanMinimalInvestmentIncome.parse_obj, valid_data)

    def test_if_inv_income_valid_and_minimal_investment_income_no_then_raise_no_validation_error(self):
        valid_data = {'minimal_investment_income': 'no'}
        try:
            with patch('app.model.eligibility_data.InvestmentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MoreThanMinimalInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MoreThanMinimalInvestmentIncome.parse_obj should not raise validation error")


class TestNoTaxedInvestmentIncome(unittest.TestCase):

    def test_if_above_minimal_inv_income_valid_and_taxed_investment_income_no_then_raise_validation_error(self):
        non_valid_data = {'taxed_investment_income': 'no'}
        with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, NoTaxedInvestmentIncome.parse_obj, non_valid_data)

    def test_if_above_minimal_inv_income_invalid_and_taxed_investment_income_yes_then_raise_validation_error(self):
        valid_data = {'taxed_investment_income': 'yes'}
        with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.parse_obj',
                   MagicMock(side_effect=ValidationError([], MoreThanMinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoTaxedInvestmentIncome.parse_obj, valid_data)

    def test_if_above_minimal_inv_income_valid_and_taxed_investment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'taxed_investment_income': 'yes'}
        try:
            with patch('app.model.eligibility_data.MoreThanMinimalInvestmentIncome.__init__',
                       MagicMock(return_value=None)):
                NoTaxedInvestmentIncome.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoTaxedInvestmentIncome.parse_obj should not raise validation error")


class TestCheaperCheckEligibilityData(unittest.TestCase):

    def test_if_taxed_inv_valid_and_cheaper_check_yes_then_raise_validation_error(self):
        non_valid_data = {'cheaper_check': 'yes'}
        with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, CheaperCheckEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_invalid_and_cheaper_check_no_then_raise_validation_error(self):
        valid_data = {'cheaper_check': 'no'}
        with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoTaxedInvestmentIncome))):
            self.assertRaises(ValidationError, CheaperCheckEligibilityData.parse_obj, valid_data)

    def test_if_taxed_inv_valid_and_cheaper_check_no_then_raise_no_validation_error(self):
        valid_data = {'cheaper_check': 'no'}
        try:
            with patch('app.model.eligibility_data.NoTaxedInvestmentIncome.__init__',
                       MagicMock(return_value=None)):
                CheaperCheckEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("CheaperCheckEligibilityData.parse_obj should not raise validation error")


class TestNoInvestmentIncomeEligibilityData(unittest.TestCase):

    def test_if_taxed_inv_valid_and_investment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'investment_income': 'yes'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, NoInvestmentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_invalid_and_investment_income_no_then_raise_validation_error(self):
        valid_data = {'investment_income': 'no'}
        with patch('app.model.eligibility_data.PensionEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], PensionEligibilityData))):
            self.assertRaises(ValidationError, NoInvestmentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_taxed_inv_valid_and_investment_income_no_then_raise_no_validation_error(self):
        valid_data = {'investment_income': 'no'}
        try:
            with patch('app.model.eligibility_data.PensionEligibilityData.__init__',
                       MagicMock(return_value=None)):
                NoInvestmentIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("NoInvestmentIncomeEligibilityData.parse_obj should not raise validation error")


class TestNoEmploymentIncomeEligibilityData(unittest.TestCase):

    def test_if_cheaper_check_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_inv_income_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_income_valid_and_employment_income_yes_then_raise_validation_error(self):
        non_valid_data = {'employment_income': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_cheaper_check_and_no_inv_income_and_taxed_inv_income_invalid_and_employment_income_no_then_raise_validation_error(self):
        valid_data = {'employment_income': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, NoEmploymentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_cheaper_check_valid_and_employment_income_no_then_raise_no_validation_error(self):
        valid_data = {'employment_income': 'no'}
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
        valid_data = {'employment_income': 'no'}
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
        valid_data = {'employment_income': 'no'}
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
        non_valid_data = {'employment_income': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_inv_income_valid_and_employment_income_no_then_raise_validation_error(self):
        non_valid_data = {'employment_income': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_taxed_inv_income_valid_and_employment_income_no_then_raise_validation_error(self):
        non_valid_data = {'employment_income': 'no'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj'):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_cheaper_check_and_no_inv_income_and_taxed_inv_income_invalid_and_employment_income_yes_then_raise_validation_error(self):
        valid_data = {'employment_income': 'yes'}
        with patch('app.model.eligibility_data.CheaperCheckEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], CheaperCheckEligibilityData))), \
                patch('app.model.eligibility_data.NoInvestmentIncomeEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], NoInvestmentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MinimalInvestmentIncome.parse_obj',
                      MagicMock(side_effect=ValidationError([], MinimalInvestmentIncome))):
            self.assertRaises(ValidationError, EmploymentIncomeEligibilityData.parse_obj, valid_data)

    def test_if_cheaper_check_valid_and_employment_income_yes_then_raise_no_validation_error(self):
        valid_data = {'employment_income': 'yes'}
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
        valid_data = {'employment_income': 'yes'}
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
        valid_data = {'employment_income': 'yes'}
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
        non_valid_data = {'marginal_employment': 'no'}
        with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, MarginalEmploymentEligibilityData.parse_obj, non_valid_data)

    def test_if_employment_income_invalid_and_marginal_employment_yes_then_raise_validation_error(self):
        valid_data = {'marginal_employment': 'yes'}
        with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], EmploymentIncomeEligibilityData))):
            self.assertRaises(ValidationError, MarginalEmploymentEligibilityData.parse_obj, valid_data)

    def test_if_employment_income_valid_and_marginal_employment_yes_then_raise_no_validation_error(self):
        valid_data = {'marginal_employment': 'yes'}
        try:
            with patch('app.model.eligibility_data.EmploymentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)):
                MarginalEmploymentEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("MarginalEmploymentEligibilityData.parse_obj should not raise validation error")


class TestOtherIncomeEligibilityData(unittest.TestCase):

    def test_if_no_employment_valid_and_other_income_yes_then_raise_validation_error(self):
        non_valid_data = {'other_income': 'yes'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj'), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_marginal_employ_valid_and_other_income_yes_then_raise_validation_error(self):
        non_valid_data = {'other_income': 'yes'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoEmploymentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, non_valid_data)

    def test_if_no_and_marginal_employ_invalid_and_other_income_no_then_raise_validation_error(self):
        valid_data = {'other_income': 'no'}
        with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], NoEmploymentIncomeEligibilityData))), \
                patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                      MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
            self.assertRaises(ValidationError, OtherIncomeEligibilityData.parse_obj, valid_data)

    def test_if_no_employment_valid_and_other_income_no_then_raise_no_validation_error(self):
        valid_data = {'other_income': 'no'}
        try:
            with patch('app.model.eligibility_data.NoEmploymentIncomeEligibilityData.__init__',
                       MagicMock(return_value=None)), \
                    patch('app.model.eligibility_data.MarginalEmploymentEligibilityData.parse_obj',
                          MagicMock(side_effect=ValidationError([], MarginalEmploymentEligibilityData))):
                OtherIncomeEligibilityData.parse_obj(valid_data)
        except ValidationError as e:
            self.fail("OtherIncomeEligibilityData.parse_obj should not raise validation error")

    def test_if_marginal_employ_valid_and_other_income_no_then_raise_no_validation_error(self):
        valid_data = {'other_income': 'no'}
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
        non_valid_data = {'foreign_country': 'yes'}
        with patch('app.model.eligibility_data.OtherIncomeEligibilityData.parse_obj'):
            self.assertRaises(ValidationError, ForeignCountryEligibility.parse_obj, non_valid_data)

    def test_if_other_income_invalid_and_foreign_country_no_then_raise_validation_error(self):
        valid_data = {'foreign_country': 'no'}
        with patch('app.model.eligibility_data.OtherIncomeEligibilityData.parse_obj',
                   MagicMock(side_effect=ValidationError([], OtherIncomeEligibilityData))):
            self.assertRaises(ValidationError, ForeignCountryEligibility.parse_obj, valid_data)

    def test_if_other_income_valid_and_foreign_country_no_then_raise_no_validation_error(self):
        valid_data = {'foreign_country': 'no'}
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
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_separated_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'yes',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'yes',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_separated_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'yes',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_joint_taxes_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'yes',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_both_have_elster_account_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'yes',
            'user_b_has_elster_account': 'yes',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_only_a_has_elster_account_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'yes',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_widowed_and_everything_is_set_to_no_and_pension_then_parse_valid_foreign_country_data(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_everything_is_set_to_no_and_pension_then_parse_valid_foreign_country_data(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_divorced_and_joint_taxes_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'divorced',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_divorced_and_no_joint_taxes_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'divorced',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_widowed_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'widowed',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'yes',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_widowed_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'widowed',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'yes',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_divorced_and_no_joint_taxes_and_alimony_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'divorced',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'yes',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_divorced_and_no_joint_taxes_and_no_alimony_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'divorced',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_single_and_has_elster_account_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'yes',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'no',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_has_no_pension_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'no',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_single_and_has_pension_then_raise_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_married_and_joint_taxes_and_has_no_pension_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'no',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_married_and_joint_taxes_and_has_pension_then_raise_validation_error(self):
        valid_data = {
            'marital_status': 'married',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'yes',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_pension_has_only_minimal_investment_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_pension_has_investment_not_taxed_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_pension_has_taxed_investment_and_wants_cheaper_check_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'no',
            'cheaper_check': 'yes',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_pension_has_taxed_investment_and_wants_no_cheaper_check_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'yes',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_no_investment_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'no',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_no_investment_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_has_minimal_investment_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'no',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_has_minimal_investment_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_wants_no_cheaper_check_income_and_has_employment_income_and_has_more_than_marginal_income_then_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'yes',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'no',
            'other_income': 'no',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_wants_no_cheaper_check_income_and_has_employment_income_and_has_only_marginal_income_then_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'yes',
            'minimal_investment_income': 'no',
            'taxed_investment_income': 'yes',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_only_marginal_income_and_other_income_than_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'yes',
            'other_income': 'yes',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_only_marginal_income_and_no_other_income_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'yes',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_no_employment_income_and_other_income_than_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'no',
            'other_income': 'yes',
            'foreign_country': 'no'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_no_employment_income_and_no_other_income_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_other_income_and_foreign_country_than_raise_validation_error(self):
        invalid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'no',
            'other_income': 'no',
            'foreign_country': 'yes'}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)

    def test_if_other_income_and_no_foreign_country_than_raise_no_validation_error(self):
        valid_data = {
            'marital_status': 'single',
            'separated_since_last_year': 'no',
            'user_a_has_elster_account': 'no',
            'user_b_has_elster_account': 'no',
            'joint_taxes': 'no',
            'alimony': 'no',
            'pension': 'yes',
            'investment_income': 'no',
            'minimal_investment_income': 'yes',
            'taxed_investment_income': 'no',
            'cheaper_check': 'no',
            'employment_income': 'no',
            'marginal_employment': 'yes',
            'other_income': 'no',
            'foreign_country': 'no'}

        try:
            self.last_step_data_type.parse_obj(valid_data)
        except ValidationError:
            self.fail("Parsing the data should not have raised a validation error")

    def test_if_empty_data_then_raise_validation_error(self):
        invalid_data = {}

        self.assertRaises(ValidationError, self.last_step_data_type.parse_obj, invalid_data)
