import unittest

from .test_drae import TestGetDefinitions


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetDefinitions)
