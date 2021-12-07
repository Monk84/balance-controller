import unittest
from datetime import date, timedelta, datetime

from businessEntity import BusinessEntity


# ----------------- BUSINESS ENTITY TESTING ----------------
class TestBusinessEntity(unittest.TestCase):

    def setUp(self):
        return

    def test_init(self):
        return

    def test_right_add_regular_operation(self):
        application = BusinessEntity()
        application.add_regular_operation("Special name", application.regularOperationTypes[0], 12,
                                          timedelta(30), timedelta(2), date(2020, 2, 1))
        self.assertEqual("Special name", application.regularOperations[-1]["operation"].name)

    def test_wrong_add_regular_operation(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            application.add_regular_operation("Special name", application.regularOperationTypes[0],
                                              12, 30, timedelta(2), "2020-02-01")
            self.assertNotEqual("Special name", application.regularOperations[-1]["operation"].name)

    def test_right_change_regular_operation(self):
        application = BusinessEntity()
        application.change_regular_operation(1, "Special name", application.regularOperationTypes[0],
                                             12, timedelta(30), timedelta(2))
        self.assertEqual("Special name", application.regularOperations[0]["operation"].name)

    def test_wrong_change_regular_operation(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            application.change_regular_operation(1, 11, application.regularOperationTypes[0],
                                                 12, timedelta(30), timedelta(2))
            self.assertEqual("Special name", application.regularOperations[0]["operation"].name)

    def test_missing_change_regular_operation(self):
        application = BusinessEntity()
        application.change_regular_operation(12314124, "Special name", application.regularOperationTypes[0],
                                             12, timedelta(30), timedelta(2))
        for i in range(len(application.regularOperations)):
            self.assertNotEqual("Special name", application.regularOperations[i]["operation"].name)

    def test_remove_regular_operation(self):
        application = BusinessEntity()
        application.change_regular_operation(1)
        for i in range(len(application.regularOperations)):
            self.assertNotEqual("Кредит за машину", application.regularOperations[i]["operation"].name)
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




