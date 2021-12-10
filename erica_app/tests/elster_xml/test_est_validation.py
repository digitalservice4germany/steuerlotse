import unittest

from erica.config import get_settings
from erica.elster_xml.est_validation import is_valid_bufa


class TestIsInvalidBufa(unittest.TestCase):

    def test_if_invalid_bufa_then_return_false(self):
        invalid_bufa = '1234'
        result = is_valid_bufa(invalid_bufa)
        self.assertFalse(result)

    def test_if_valid_bufa_then_return_true(self):
        valid_bufas = ['1010', '1113', '2111', '2217', '2313', '2460', '2601', '2701', '2801', '3046', '3102', '3202',
                       '4070', '4151', '5101', '9101']
        for valid_bufa in valid_bufas:
            result = is_valid_bufa(valid_bufa)
            self.assertTrue(result)

    def test_if_valid_test_bufa_then_return_true(self):
        valid_test_bufas = ['1096', '1194', '2138', '2375', '2497', '2653', '2749', '2866', '3093', '3196', '3246',
                            '4088', '4196', '5192', '9172']

        for valid_test_bufa in valid_test_bufas:
            result = is_valid_bufa(valid_test_bufa)
            self.assertTrue(result)

    def test_if_valid_test_bufa_and_do_not_accept_test_bufa_then_return_false(self):
        orig_flag = get_settings().accept_test_bufa

        try:
            get_settings().accept_test_bufa = False
            valid_test_bufa = '1096'
            result = is_valid_bufa(valid_test_bufa)
            self.assertFalse(result)
        finally:
            get_settings().accept_test_bufa = orig_flag

    def test_if_valid_test_bufa_and_do_not_accept_test_bufa_but_use_testmerker_true_then_return_true(self):
        orig_flag = get_settings().accept_test_bufa

        try:
            get_settings().accept_test_bufa = False
            valid_test_bufa = '1096'
            result = is_valid_bufa(valid_test_bufa, use_testmerker=True)
            self.assertTrue(result)
        finally:
            get_settings().accept_test_bufa = orig_flag
