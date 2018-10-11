import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test.test_authentication import Test_Authetication

if __name__ == '__main__':
    unittest.main()
