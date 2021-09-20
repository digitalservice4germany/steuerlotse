import datetime
from decimal import Decimal
import unittest

import pytest

from erica.routes import validate_est
from tests.utils import create_est, create_est_single, missing_cert, missing_pyeric_lib


class TestSampleDataValidation(unittest.TestCase):

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_01_not_married(self):
        response = validate_est(est=create_est_single(True))
        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_02_married_rel_ev(self):
        married_data = create_est(True)

        married_data.est_data.__dict__.update({
            'person_a_religion': 'ev',
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_est(married_data)
        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_03_divorced_rel_rk(self):
        single_data = create_est_single(True)
        single_data.est_data.__dict__.update({
            'person_a_religion': 'rk',
            'familienstand': 'divorced',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_est(single_data)
        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_04_widowed(self):
        single_data = create_est_single(True)
        single_data.est_data.__dict__.update({
            'familienstand': 'widowed',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_est(single_data)
        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_06_with_person_b_same_address(self):
        married_data = create_est(True)
        married_data.est_data.__dict__.update({
            'person_b_same_address': True,
        })

        response = validate_est(married_data)
        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_07_steuerminderungen(self):
        single_data = create_est_single(True)
        single_data.est_data.__dict__.update({
            'steuerminderung': 'yes',

            'haushaltsnahe_entries': ["Gartenarbeiten"],
            'haushaltsnahe_summe': Decimal('500.00'),

            'handwerker_entries': ["Renovierung Badezimmer"],
            'handwerker_summe': Decimal('200.00'),
            'handwerker_lohn_etc_summe': Decimal('100.00'),
        })

        response = validate_est(single_data)
        self.assertIsNotNone(response)
