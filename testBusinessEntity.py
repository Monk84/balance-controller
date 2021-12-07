import unittest

from businessEntity import BusinessEntity


# ----------------- NOTIFICATION TESTING ----------------
class TestBusinessEntity(unittest.TestCase):

    def setUp(self):
        return

    def test_init(self):
        return

    def test_add_regular_operation(self):
        return

    def test_change_regular_operation(self):
        return

    def test_remove_regular_operation(self):
        return

    def test_change_deposit_balance(self):
        return

    def test_form_statistics_by_period(self):
        return

    def add_regular_operation_type(self):
        return

def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(TestBusinessEntity('test_init'))
    _suite.addTest(TestBusinessEntity('test_add_regular_operation'))
    _suite.addTest(TestBusinessEntity('test_change_regular_operation'))
    _suite.addTest(TestBusinessEntity('test_remove_regular_operation'))
    _suite.addTest(TestBusinessEntity('test_change_deposit_balance'))
    _suite.addTest(TestBusinessEntity('test_form_statistics_by_period'))
    _suite.addTest(TestBusinessEntity('add_regular_operation_type'))
    return _suite




