import unittest

from cryptography.fernet import InvalidToken

from app.config import Config
from app.crypto.encryption import encrypt, decrypt, hybrid_encrypt, hybrid_decrypt

PUBLIC_TEST_KEY = b'-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEApLDlzrgFvxqvP91dc0ML\nZZQXWY8Bap4D9qqy2NUiCPTVZ215B7WTKEMzLtIkGj+YR641YKAcTaugo6lDzzA0\naNeJ200OgZRRjyJgQOBkgR1Xoue4POlLyShn8JUA4Yds5IoAjvpVmlm/f+T0CPsi\nQiBXwLad7WfaDvBAqB8zsSIXvQmnTcV7foPpi4ETIWbqQlX5Wi6FaDM9hdNNZrYN\nbJxm02wMW8nF4IHNpTVaOSKGn7xX6YN7gwRYeXYkH27QX6IA4ezecYOGnN/2C14S\nVGiSZegkyH+TQ6IEjzwzmM2iXyW2+a2klzS+wJbv/LcDXhv7oWpA5FDwN3jIIEnF\nIJGF0avaNOaPEYDMSWKwZGpMQ5jGee22XistZgMjmKZuDyqe7r9m2UaKuxeYKHDq\nxgkaxGBxcMXGgcHYxDQVeQJjRf3jrdUq881QaHxdF/I8DmDerkbfwYs5DEombXh6\n+F8DIm0qJBSxAFo1Q2iPRJUh6/kyZgYGZwpmMTU1vtHB8EHNsogdRqnPO1wVWA/H\nxl14CjPl2HEe6ONX52QcvgAmNzP1rhaWqZrDEN6Mn1nCLzfWyW2lz1dGvDhBAdGO\nS5Rb2nH5qkUwgIM948IOHBgGxXgP2XvsJJ57AeQ/8fRDRAGv4MPrbIadFXiAPYt2\nI8kAE2EwADth6d2Hi1gA+EkCAwEAAQ==\n-----END PUBLIC KEY-----'
PRIVATE_TEST_KEY = b'-----BEGIN RSA PRIVATE KEY-----\nMIIJKQIBAAKCAgEApLDlzrgFvxqvP91dc0MLZZQXWY8Bap4D9qqy2NUiCPTVZ215\nB7WTKEMzLtIkGj+YR641YKAcTaugo6lDzzA0aNeJ200OgZRRjyJgQOBkgR1Xoue4\nPOlLyShn8JUA4Yds5IoAjvpVmlm/f+T0CPsiQiBXwLad7WfaDvBAqB8zsSIXvQmn\nTcV7foPpi4ETIWbqQlX5Wi6FaDM9hdNNZrYNbJxm02wMW8nF4IHNpTVaOSKGn7xX\n6YN7gwRYeXYkH27QX6IA4ezecYOGnN/2C14SVGiSZegkyH+TQ6IEjzwzmM2iXyW2\n+a2klzS+wJbv/LcDXhv7oWpA5FDwN3jIIEnFIJGF0avaNOaPEYDMSWKwZGpMQ5jG\nee22XistZgMjmKZuDyqe7r9m2UaKuxeYKHDqxgkaxGBxcMXGgcHYxDQVeQJjRf3j\nrdUq881QaHxdF/I8DmDerkbfwYs5DEombXh6+F8DIm0qJBSxAFo1Q2iPRJUh6/ky\nZgYGZwpmMTU1vtHB8EHNsogdRqnPO1wVWA/Hxl14CjPl2HEe6ONX52QcvgAmNzP1\nrhaWqZrDEN6Mn1nCLzfWyW2lz1dGvDhBAdGOS5Rb2nH5qkUwgIM948IOHBgGxXgP\n2XvsJJ57AeQ/8fRDRAGv4MPrbIadFXiAPYt2I8kAE2EwADth6d2Hi1gA+EkCAwEA\nAQKCAgAnO78bXmp8CsLaD4WuKjgiVEO1waQgPpGKJ0Mg9bE8efsGvyUYiZCLhGrC\niiwwlprT5LPxl2L2u96ybmXpiz3JBiPguvwsMWW2mAVfHzXCLnfMprAUzq0PuFD+\nlriVgZoW3athZFCVSzEcKjJam10fbK4LClYYEuf3LBPzGS/K0GjgT1bsZ5HSY2F1\nKuQgTnCbKfkTm0aLur06zso/IDqVd7LlRfWxviEmKTYQ1+Ns/gUdM5Sr2/dGEHh1\nQwg69r6sMZ9NMw0Q9LjSUWY/cgMi2aCap1Fv9DhkYcn9R2WxTreSPB1ZYJz3qoiQ\nv8RfK0ghmL/6xaG84m0/gcYHLxvHEt50cCyeGz/OZKG9uHIyw3VSeu72Go4sN2Hq\nnobQep5xYPSJFw/7OTy9rQZe6H7v8ehK4Lbon1Wniuj9Idne+W6WOpHmePdw7Ghu\nBNgjymTLeV0FfewTL690ApqD8g8aAZyjpo1pM4itCM7pup/kf/BhYRExeCySFpXJ\nehzcsT6Y5P3j2Kt+2dVY7aGjl6kJ6Yougpd/F9+SNZ4oHpy3sXxzZS/IJgR8ZePg\nyi7YnNXJ7mK4+RQJTSYuxfNNSVK2yFo/FZ7DQoa1jSAXL1FHZ/plSmQuMj/eLJwT\n01tlauUc+j56BmZLzHMh2XZRS/oZri4fsxAxjH/7TPJtcRCA+wKCAQEAvxsZztfH\nNkojsPjqlg5z3D2+cOKokozWEYgXAXTZN/LtGXCIC5+9i+VOZrjALdEXongNfGeX\n85JUqyXKqEbH8bHYnbNmsQqB/ubKO0V3SpOuEl5YVd46UHYVhWWn9ilKZb2WoaRo\nzMPbUJ+J2SmB09SpwDGsm6sLcK3B0op/ecQcKZg248E2OMoaYUkiJhiBH2VCGxJu\n5Le1ygzDxGOQVCirZqiYF17kUzh17QCnI1e/DjeqHPnFY1wfoUuIsBeFUhnjCFJj\nTwodooh1pNe1WZsozjvd3Ui+ed99hHOrBldTlMUJWUco7832/bXIBV5R9bcx0p1L\nm+5OgrPtbM9vvwKCAQEA3J2LU537uxOODb0t4jiAtSVjDcdJRJhjWnQCumWwuXVF\naatx4iwX7fhBi7U13AwF/zLdcLZ8l26XxoRGbTfwfhPGR0Ew2fbIAif1BfhKWzid\nmLLGjslAZd4ISbeBn69+n6BQ82hJUE6qWKT5OsMEb76XILeuxqGIfkP5OryETM/n\n9U2Qlp8WTE27IRvEB6olKx3jzboXlNY07Iouo2xvVKxj+JpeRUGFJOf738UiHuEb\nn9ee9Bwyd4+b4//fjaK/8eDnncQWwejDvP5Tni0qhW1eyL7L31cavcCf9IpwKdHe\nrYwefe13ODcYsrf7xTcm5a1hiIpqO/H3YGf2oq2Z9wKCAQEApatqziPFcU0Ib+z6\nAKf6zN1B8T6tAI7TLVObDgosHRKddMZXSixq95IMS4SyJYX0RUZp+oUb923NtKkI\nbKUfxGl27g+OYMBJPZ75hjSMW7x21Tmwvo/uYb5cnc4os3/MHTMkGHEc4RaRU+1a\nZUZUZD0iA5mMl07Klh4rvseOBxN5jp2ESCFBTi32fIwX7IqltX/ktO9f7ytLjyNN\nuzzM7Ahtvos9flUm/vYdVR6RxlPVLxAWixQEiERer0d58Z4SV8BVTuuNaAHO+w3t\nXsAZWNrnnxHLHoBnj+OtPlu/0bl2navKlPjZhjo5emxSQEUqLCdqK7lsyHro2On+\nU6vopQKCAQEAzSFr8DbgXuVi22GA7WyOOGDoBmK7vJ1ZHDzsYHa3aOoivYtdW+iV\n435HK+k1iEJhvRWFkw0LMh7x3vMVLO6rnf8zCQQTsUdmV6LhkEh6kvFEkDwCpbd5\nOn7GBA0t6NXcDf6Z5omcSaCrgbr7xmiYknKLwS8pwqVl7cm0TqoE9gsG6i7R90s7\nB33rNnDDyECrSLkFHUAgNxMpqJsfnHLx3bBhUEHwz8KJU3Sk3T9GZ6H19p0dvmsN\nfeA5GjnLmr2ubfAqTKaMZobQocV06ImklOXKESxfEm7CfZdC47Vpb2kl/QZhP8Py\na4HHZD3wS0Lp1vtsyfGxr8Vft/NS/5YdpwKCAQBVpOycWAu6//VmtbHgPRa8TELt\nuBIL8no2GXO7oR9pWRZ/zF0Sml1ET3IE9r/ihFBjPqveNHvRWP78rZwtVzEHjWsX\nQtfjXy3qF++I8T7wtiNVYe/myzcsEaqXuuBl0LwwBmY21Y43kooOZ/+H9ur7n+UO\nDhC62+f/uHqmFmqQjVJxGa2D6UxlsyWQqAgZfOzSlNkgn//zFaK0Ma1YVStuzFP4\nTIJX9RyDcOc3NamBmuvNCSJ5jGSeI+ntykqKbLl4dC6SQQFTEqmWmR+/TX2WMN9U\nxYpC8EBnT3u+cJhlF/rNUkmsPJjONpD4BEJ4mtIIsQ86/eG+as6Sl42/hRDH\n-----END RSA PRIVATE KEY-----'
PRIVATE_TEST_KEY_WRONG = b'-----BEGIN RSA PRIVATE KEY-----\n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\n-----END RSA PRIVATE KEY-----'


class TestEncryptDecrypt(unittest.TestCase):
    def setUp(self):
        self.encryption_key = Config.ENCRYPTION_KEY

    def test_if_same_key_for_encryption_and_decryption_then_return_original_plaintext(self):
        plaintext = b"It was Agatha all along"
        ciphertext = encrypt(plaintext)
        decrypted_text = decrypt(ciphertext)

        self.assertEqual(plaintext, decrypted_text)

    def test_if_ciphertext_is_changed_then_raise_error(self):
        plaintext = b"It was Agatha all along"
        ciphertext = encrypt(plaintext)
        ciphertext = ciphertext[1:2] + ciphertext[1:]

        self.assertRaises(InvalidToken, decrypt, ciphertext)

    def test_if_different_key_used_for_encryption_and_decryption_then_raise_error(self):
        plaintext = b"It was Agatha all along"
        ciphertext = encrypt(plaintext)
        Config.ENCRYPTION_KEY = Config.ENCRYPTION_KEY[1:2] + Config.ENCRYPTION_KEY[1:]

        self.assertRaises(InvalidToken, decrypt, ciphertext)

    def tearDown(self):
        Config.ENCRYPTION_KEY = self.encryption_key


class TestHybridEncryptDecrypt(unittest.TestCase):
    def setUp(self):
        self.original_public_key = Config.RSA_ENCRYPT_PUBLIC_KEY
        Config.RSA_ENCRYPT_PUBLIC_KEY = PUBLIC_TEST_KEY

    def test_version_number_set_correctly_on_encrypt(self):
        original_message = b'I am your father.'
        ciphertext = hybrid_encrypt(original_message)
        self.assertEqual(b'1', ciphertext[:1])

    def test_if_correct_asymm_key_then_return_same_data(self):
        original_message = b'I am your father.'
        encrypted_message = hybrid_encrypt(original_message)
        decrypted_message = hybrid_decrypt(encrypted_message, PRIVATE_TEST_KEY)

        self.assertEqual(original_message, decrypted_message)

    def test_if_ciphertext_is_changed_then_raise_error(self):
        original_message = b'I am your father.'
        encrypted_message = hybrid_encrypt(original_message)
        encrypted_message = b'Luke, ' + encrypted_message

        self.assertRaises(ValueError, hybrid_decrypt, encrypted_message, PRIVATE_TEST_KEY)

    def test_if_wrong_key_used_for_decryption_then_raise_error(self):
        original_message = b'I am your father.'
        encrypted_message = hybrid_encrypt(original_message)
        encrypted_message = b'Luke, ' + encrypted_message

        self.assertRaises(ValueError, hybrid_decrypt, encrypted_message, PRIVATE_TEST_KEY_WRONG)

    def tearDown(self):
        Config.RSA_ENCRYPT_PUBLIC_KEY = self.original_public_key
