from erica.config import get_settings
from erica.elster_xml.bufa_numbers import VALID_BUFA_NUMBERS, VALID_TEST_BUFA_NUMBERS


def is_valid_bufa(bufa, use_testmerker=False):
    """
    Checks whether a number is a valid bufa. For this it has to be checked against all
    the different tax offices in different states

    :param bufa: The first four digits of the electronic tax number; representing the Bundesfinanzamt number
    :param use_testmerker: Allows test_bufas even if the settings do not accept test bufas. Use this for special idnrs.
    """
    if get_settings().accept_test_bufa or use_testmerker:
        return bufa in VALID_BUFA_NUMBERS or bufa in VALID_TEST_BUFA_NUMBERS

    return bufa in VALID_BUFA_NUMBERS
