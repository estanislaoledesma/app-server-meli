import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test.testHelloWorld import TestHelloWorld
from test.testSignUp import TestSignUp
from test.testLogIn import TestLogIn
from test.testUser import TestUser
from test.testProducts import TestProducts
from test.testProduct import TestProduct
from test.testPurchases import TestPurchases

if __name__ == '__main__':
    unittest.main()
