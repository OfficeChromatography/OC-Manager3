# Helps to test functions
from django.test import TestCase

from app.calc import add

class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that 2 numbers are add it together"""
        self.assertEqual(add(3,8),11)
