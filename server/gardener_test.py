import unittest

from gardener import Gardener


class UtilsTest(unittest.TestCase):

    @staticmethod
    def test_that_it_sends_sms():
        Gardener.send_sms("testing sms")


if __name__ == '__main__':
    unittest.main()
