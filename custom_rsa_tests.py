import unittest
from unittest.mock import patch

from custom_rsa import RSA, Encoder, Encrypter, Decrypter


class TestRsa(unittest.TestCase):
    
    def setUp(self):
        self.rsa = RSA(17, 31)
    
    def test_gcd(self):
        self.assertEqual(self.rsa._gcd(6, 12), 6)
        self.assertEqual(self.rsa._gcd(4, 12), 4)
        self.assertEqual(self.rsa._gcd(5, 11), 1)
    
    def test_is_prime(self):
        self.assertTrue(self.rsa._is_prime(7))
        self.assertTrue(self.rsa._is_prime(31))
        self.assertFalse(self.rsa._is_prime(39))
        self.assertFalse(self.rsa._is_prime(57))
    
    def test_cannot_initialise_with_non_primes(self):
        with self.assertRaises(ValueError):
            rsa = RSA(12, 10)
        with self.assertRaises(ValueError):
            rsa = RSA(11, 12)

    def test_calculate_viable_pairs(self):
        prime1 = 11
        prime2 = 19
        rsa = RSA(prime1, prime2)
        
        # all keys must:
        # * be between 1 and fn
        # * gcd(fn, e) == 1
        fn = (prime1-1)*(prime2-1)
        self.assertGreater(min(rsa._ds.keys()), 1)
        self.assertLess(max(rsa._ds.keys()), fn)
        
        for key in rsa._ds:
            self.assertEqual(rsa._gcd(rsa._ds[key], fn), 1)
            
    def test_get_keys(self):
        keys = list(self.rsa._ds.keys())[:3]
        ds = {key: self.rsa._ds[key] for key in keys}
        self.rsa._ds = ds
        
        self.assertEqual(self.rsa.get_keys(0), (343, 7, 527))
        self.assertEqual(self.rsa.get_keys(1), (131, 11, 527))
        self.assertEqual(self.rsa.get_keys(2), (37, 13, 527))

        self.assertEqual(self.rsa.get_keys(-3), (343, 7, 527))
        self.assertEqual(self.rsa.get_keys(-2), (131, 11, 527))
        self.assertEqual(self.rsa.get_keys(-1), (37, 13, 527))

        all_results = (
            (343, 7, 527),
            (131, 11, 527),
            (37, 13, 527),
        )
        for _ in range(10):
            self.assertIn(self.rsa.get_keys(), all_results)


class TestEncoder(unittest.TestCase):

    def setUp(self):
        self.encoder = Encoder()

    def test_encode_no_charmap(self):
        encoded = self.encoder.encode('abcABC')
        self.assertEqual(encoded, [97, 98, 99, 65, 66, 67])

    def test_encode_with_charmap(self):
        self.encoder.charmap = list('ABCDabcd')
        encoded = self.encoder.encode('abcABC')
        self.assertEqual(encoded, [4, 5, 6, 0, 1, 2])

    def test_decode_no_charmap(self):
        decoded = self.encoder.decode([97, 98, 99, 65, 66, 67])
        self.assertEqual(decoded, 'abcABC')

    def test_decode_with_charmap(self):
        self.encoder.charmap = list('ABCDabcd')
        decoded = self.encoder.decode([4, 5, 6, 0, 1, 2])
        self.assertEqual(decoded, 'abcABC')


class TestEncrypter(unittest.TestCase):
    
    @patch('custom_rsa.Encoder.encode', return_value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_encrypt(self, mock_encoder):
        # don't need to use actual RSA keys - use basic numbers to make test easier
        encrypter = Encrypter(2, 3)
        self.assertEqual(
            encrypter.encrypt('dummy'),
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
        )

    def test_decrypt(self):
        encoded_message = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        decrypter = Decrypter(2, 3, charmap='abcABC')
        self.assertEqual(
            decrypter.decrypt(encoded_message), 
            'abbabbabba'
        )
        

if __name__ == '__main__':
    unittest.main()
