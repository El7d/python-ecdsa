try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    buffer
except NameError:
    buffer = memoryview

import array
import six
import sys
import pytest

from .keys import VerifyingKey
from .der import unpem


class TestVerifyingKeyFromString(unittest.TestCase):
    """
    Verify that ecdsa.keys.VerifyingKey.from_string() can be used with
    bytes-like objects
    """

    @classmethod
    def setUpClass(cls):
        cls.key_bytes = (b'\x04L\xa2\x95\xdb\xc7Z\xd7\x1f\x93\nz\xcf\x97\xcf'
                       b'\xd7\xc2\xd9o\xfe8}X!\xae\xd4\xfah\xfa^\rpI\xba\xd1'
                       b'Y\xfb\x92xa\xebo+\x9cG\xfav\xca')
        cls.vk = VerifyingKey.from_string(cls.key_bytes)

    def test_bytes(self):
        self.assertIsNotNone(self.vk)
        self.assertIsInstance(self.vk, VerifyingKey)
        self.assertEqual(
            self.vk.pubkey.point.x(),
            105419898848891948935835657980914000059957975659675736097)
        self.assertEqual(
            self.vk.pubkey.point.y(),
            4286866841217412202667522375431381222214611213481632495306)

    def test_bytes_memoryview(self):
        vk = VerifyingKey.from_string(buffer(self.key_bytes))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytearray(self):
        vk = VerifyingKey.from_string(bytearray(self.key_bytes))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytesarray_memoryview(self):
        vk = VerifyingKey.from_string(buffer(bytearray(self.key_bytes)))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_bytes(self):
        arr = array.array('B', self.key_bytes)
        vk = VerifyingKey.from_string(arr)

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_bytes_memoryview(self):
        arr = array.array('B', self.key_bytes)
        vk = VerifyingKey.from_string(buffer(arr))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_ints(self):
        arr = array.array('I', self.key_bytes)
        vk = VerifyingKey.from_string(arr)

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_ints_memoryview(self):
        arr = array.array('I', self.key_bytes)
        vk = VerifyingKey.from_string(buffer(arr))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytes_uncompressed(self):
        vk = VerifyingKey.from_string(b'\x04' + self.key_bytes)

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytearray_uncompressed(self):
        vk = VerifyingKey.from_string(bytearray(b'\x04' + self.key_bytes))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytes_compressed(self):
        vk = VerifyingKey.from_string(b'\x02' + self.key_bytes[:24])

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytearray_uncompressed(self):
        vk = VerifyingKey.from_string(bytearray(b'\x02' + self.key_bytes[:24]))

        self.assertEqual(self.vk.to_string(), vk.to_string())


class TestVerifyingKeyFromDer(unittest.TestCase):
    """
    Verify that ecdsa.keys.VerifyingKey.from_der() can be used with
    bytes-like objects.
    """
    @classmethod
    def setUpClass(cls):
        prv_key_str = (
            "-----BEGIN EC PRIVATE KEY-----\n"
            "MF8CAQEEGF7IQgvW75JSqULpiQQ8op9WH6Uldw6xxaAKBggqhkjOPQMBAaE0AzIA\n"
            "BLiBd9CE7xf15FY5QIAoNg+fWbSk1yZOYtoGUdzkejWkxbRc9RWTQjqLVXucIJnz\n"
            "bA==\n"
            "-----END EC PRIVATE KEY-----\n")
        key_str = (
            "-----BEGIN PUBLIC KEY-----\n"
            "MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEuIF30ITvF/XkVjlAgCg2D59ZtKTX\n"
            "Jk5i2gZR3OR6NaTFtFz1FZNCOotVe5wgmfNs\n"
            "-----END PUBLIC KEY-----\n")
        cls.key_bytes = unpem(key_str)
        assert isinstance(cls.key_bytes, bytes)
        cls.vk = VerifyingKey.from_pem(key_str)

    def test_bytes(self):
        vk = VerifyingKey.from_der(self.key_bytes)

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytes_memoryview(self):
        vk = VerifyingKey.from_der(buffer(self.key_bytes))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytearray(self):
        vk = VerifyingKey.from_der(bytearray(self.key_bytes))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_bytesarray_memoryview(self):
        vk = VerifyingKey.from_der(buffer(bytearray(self.key_bytes)))

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_bytes(self):
        arr = array.array('B', self.key_bytes)
        vk = VerifyingKey.from_der(arr)

        self.assertEqual(self.vk.to_string(), vk.to_string())

    def test_array_array_of_bytes_memoryview(self):
        arr = array.array('B', self.key_bytes)
        vk = VerifyingKey.from_der(buffer(arr))

        self.assertEqual(self.vk.to_string(), vk.to_string())
