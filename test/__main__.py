from unittest import runner
import unittest
from . import suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
