import unittest
import sqroots

class TestSome(unittest.TestCase):
    
    def test_0(self):
        """Zero roots"""
        self.assertEqual(sqroots.sqroots('10 0 10'), '')
    
    def test_1(self):
        """One root"""
        self.assertEqual(sqroots.sqroots('10 0 0'), '0.0')
    
    def test_2(self):
        """Two roots"""
        self.assertEqual(sqroots.sqroots('1 10 9'), '-1.0 -9.0')
    
    def test_exception(self):
        """Exception"""
        with self.assertRaises(ValueError):
            sqroots.sqroots('1 1 1 1')
