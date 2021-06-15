import unittest

from .test_dle_rae_bot import TestGetDefinitions, TestGetUnwrappedContent


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetDefinitions)
    suite.addTest(TestGetUnwrappedContent)
