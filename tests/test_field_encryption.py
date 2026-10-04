import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.security import encrypt_field, decrypt_field

class TestFieldEncryption(unittest.TestCase):
    def test_encryption_roundtrip(self):
        key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        secret_name = "Major Johnathan Synthetic Pilot"

        ciphertext = encrypt_field(secret_name, key_hex)
        self.assertTrue(ciphertext.startswith("enc:"))
        self.assertNotEqual(secret_name, ciphertext)

        decrypted = decrypt_field(ciphertext, key_hex)
        self.assertEqual(secret_name, decrypted)

    def test_decryption_with_wrong_key_fails_safely(self):
        key1 = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        key2 = "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        secret = "Classified Personnel 42"

        ciphertext = encrypt_field(secret, key1)
        decrypted = decrypt_field(ciphertext, key2)
        # Should not reveal the plaintext
        self.assertNotEqual(secret, decrypted)

if __name__ == '__main__':
    unittest.main()
