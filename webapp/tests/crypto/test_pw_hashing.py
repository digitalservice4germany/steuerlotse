import unittest

from app.config import Config, ProductionConfig
from app.crypto.pw_hashing import global_salt_hash, indiv_salt_hash


class TestGlobalSaltHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_hash_algorithm = Config.HASH_ALGORITHM
        Config.HASH_ALGORITHM = ProductionConfig.HASH_ALGORITHM  # To test the real and not the mock hashing_algorithms

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        Config.HASH_ALGORITHM = cls.original_hash_algorithm
        super().tearDownClass()

    def test_hashing_twice_has_same_result(self):
        value = "The Ring has awoken"
        first_hash_value = global_salt_hash().hash(value)
        second_hash_value = global_salt_hash().hash(value)

        self.assertEqual(first_hash_value, second_hash_value)

    def test_verify_for_same_value_returns_true(self):
        value = "The Ring has awoken"
        hash_value = global_salt_hash().hash(value)

        self.assertTrue(global_salt_hash().verify(value, hash_value))

    def test_verify_for_different_values_returns_false(self):
        value = "The Ring has awoken"
        different_value = "The wise speak only of what they know"
        hash_value = global_salt_hash().hash(value)

        self.assertFalse(global_salt_hash().verify(different_value, hash_value))


class TestIndivSaltHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_hash_algorithm = Config.HASH_ALGORITHM
        Config.HASH_ALGORITHM = ProductionConfig.HASH_ALGORITHM  # To test the real and not the mock hashing_algorithms

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        Config.HASH_ALGORITHM = cls.original_hash_algorithm
        super().tearDownClass()

    def test_hashing_twice_has_different_result(self):
        value = "The Ring has awoken"
        first_hash_value = indiv_salt_hash().hash(value)
        second_hash_value = indiv_salt_hash().hash(value)

        self.assertNotEqual(first_hash_value, second_hash_value)

    def test_verify_for_same_value_returns_true(self):
        value = "The Ring has awoken"
        hash_value = indiv_salt_hash().hash(value)

        self.assertTrue(indiv_salt_hash().verify(value, hash_value))

    def test_verify_for_different_values_returns_false(self):
        value = "The Ring has awoken"
        different_value = "The wise speak only of what they know"
        hash_value = indiv_salt_hash().hash(value)

        self.assertFalse(indiv_salt_hash().verify(different_value, hash_value))
