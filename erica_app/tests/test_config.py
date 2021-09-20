import os
import unittest
from unittest.mock import patch

import pytest

from erica.config import Settings, DevelopmentSettings, StagingSettings, TestingSettings, get_settings, UnknownEricaEnvironment
from tests.utils import missing_cert, missing_pyeric_lib


class TestGetCertPath(unittest.TestCase):

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.darwin_stick_cert_path = "libaetpkss.dylib"
        self.linux_stick_cert_path = "libaetpkss.so"
        self.file_cert_path = "erica/instances/blueprint/cert.pfx"

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_using_stick_and_platform_darwin_then_return_correct_cert_path(self):
        with patch('erica.config.platform', 'darwin'):
            settings = Settings()
            settings.using_stick = True
            actual_cert_path = settings.get_cert_path()
            self.assertEqual(self.darwin_stick_cert_path, actual_cert_path)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_using_stick_and_platform_not_darwin_then_return_correct_cert_path(self):
        with patch('erica.config.platform', 'not_darwin'):
            settings = Settings()
            settings.using_stick = True
            actual_cert_path = settings.get_cert_path()
            self.assertEqual(self.linux_stick_cert_path, actual_cert_path)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_not_using_stick_and_platform_darwin_then_return_correct_cert_path(self):
        with patch('erica.config.platform', 'darwin'):
            settings = Settings()
            settings.using_stick = False
            actual_cert_path = settings.get_cert_path()
            self.assertEqual(self.file_cert_path, actual_cert_path)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_not_using_stick_and_platform_not_darwin_then_return_correct_cert_path(self):
        with patch('erica.config.platform', 'not_darwin'):
            settings = Settings()
            settings.using_stick = False
            actual_cert_path = settings.get_cert_path()
            self.assertEqual(self.file_cert_path, actual_cert_path)


class TestGetEricDll(unittest.TestCase):

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.darwin_dll_path = "erica/lib/libericapi.dylib"
        self.linux_dll_path = "erica/lib/libericapi.so"

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_platform_darwin_then_return_correct_library(self):
        with patch('erica.config.platform', 'darwin'):
            actual_dll_path = Settings.get_eric_dll_path()
            self.assertEqual(self.darwin_dll_path, actual_dll_path)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_platform_not_darwin_then_return_linux_library(self):
        with patch('erica.config.platform', 'not_darwin'):
            actual_dll_path = Settings.get_eric_dll_path()
            self.assertEqual(self.linux_dll_path, actual_dll_path)


class TestGetSettings(unittest.TestCase):

    def setUp(self) -> None:
        if 'ERICA_ENV' in os.environ:
            self.old_env = os.environ['ERICA_ENV']
        else:
            self.old_env = None
        get_settings.cache_clear()  # Because the result is stored in a lru cache, we have to remove the stored value

    def test_if_env_development_then_return_development_settings(self):
        os.environ['ERICA_ENV'] = 'development'
        setting = get_settings()
        self.assertIsInstance(setting, DevelopmentSettings)

    def test_if_env_testing_then_return_testing_settings(self):
        os.environ['ERICA_ENV'] = 'testing'
        setting = get_settings()
        self.assertIsInstance(setting, TestingSettings)

    def test_if_env_staging_then_return_staging_settings(self):
        os.environ['ERICA_ENV'] = 'staging'
        setting = get_settings()
        self.assertIsInstance(setting, StagingSettings)

    def test_if_other_env_then_raise_error(self):
        os.environ['ERICA_ENV'] = 'other_env'
        self.assertRaises(UnknownEricaEnvironment, get_settings)

    def tearDown(self) -> None:
        get_settings.cache_clear()  # Because the result is stored in a lru cache, we have to remove the stored value
        if self.old_env:
            os.environ['ERICA_ENV'] = self.old_env
        else:
            os.environ.pop('ERICA_ENV', None)
