#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from prime_generator import miller_test

class TestPrime(unittest.TestCase):
    
    def test_prime(self):
        self.assertEqual(miller_test(53, 4), True, "Should be Prime")
        self.assertEqual(miller_test(7, 11), True, "Should be Prime")
        self.assertEqual(miller_test(11, 2), True, "Should be Prime")
        self.assertEqual(miller_test(23, 10), True, "Should be Prime")
        self.assertEqual(miller_test(971, 20), True, "Should be Prime")
        self.assertEqual(miller_test(77, 4), False, "Should be Composite")
        self.assertEqual(miller_test(969, 4), False, "Should be Composite")


if __name__ == "__main__":
    unittest.main()
        