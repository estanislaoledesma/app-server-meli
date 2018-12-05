import unittest

import sys
import os

from mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.modules['gridfs'] = MagicMock()

from test.testHelloWorld import TestHelloWorld
from test.testSignUp import TestSignUp
from test.testLogIn import TestLogIn
from test.testUser import TestUser
from test.testProducts import TestProducts
from test.testProduct import TestProduct
from test.testPurchases import TestPurchases
from test.testPayments import TestPayments
from test.testPaymentStatus import TestPaymentStatus
from test.testDeliveries import TestDeliveries
from test.testEstimates import TestEstimates
from test.testDeliveryStatus import TestDeliveryStatus

if __name__ == '__main__':
    unittest.main()
