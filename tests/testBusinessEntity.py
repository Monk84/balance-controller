import unittest
from datetime import date, timedelta, datetime

from classes.businessEntity import BusinessEntity


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

    def test_right_remove_regular_operation(self):
        application = BusinessEntity()
        application.remove_regular_operation(1)
        for i in range(len(application.regularOperations)):
            self.assertNotEqual("Кредит за машину", application.regularOperations[i]["operation"].name)
            self.assertNotEqual(1, application.regularOperations[i]["id"])

    def test_wrong_remove_regular_operation(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            application.remove_regular_operation('id')
            self.assertEqual(1, application.regularOperations[0]["id"])

    def test_missing_remove_regular_operation(self):
        application = BusinessEntity()
        application.remove_regular_operation(1234124)
        self.assertEqual(2, len(application.regularOperations))

    def test_right_change_deposit_balance(self):
        application = BusinessEntity()
        application.change_deposit_balance(123456)
        self.assertEqual(123456, application.deposit_balance.balance)

    def test_wrong_change_deposit_balance(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            application.change_deposit_balance("new value")
            self.assertNotEqual("new value", application.deposit_balance.balance)

    def test_right_form_statistics_by_period(self):
        application = BusinessEntity()
        result = application.form_statistics_by_period("any_tag", "2020-01-01", "2021-01-01")
        self.assertEqual(123, result["total_income"])
        self.assertEqual(-234, result["total_spend"])

    def test_wrong_dates_format_form_statistics_by_period(self):
        application = BusinessEntity()
        with self.assertRaises(KeyError):
            result = application.form_statistics_by_period("any_tag", "20aa-01123-01", "2021-01-01")
            self.assertNotEqual(123, result["total_income"])
            self.assertNotEqual(-234, result["total_spend"])
        with self.assertRaises(KeyError):
            result = application.form_statistics_by_period("any_tag", "2020-01-01", "2021/01/01")
            self.assertNotEqual(123, result["total_income"])
            self.assertNotEqual(-234, result["total_spend"])

    def test_wrong_tag_type_statistics_by_period(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            result = application.form_statistics_by_period(123, "20aa-01123-01", "2021/01/01")

    def test_wrong_date_types_form_statistics_by_period(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            result = application.form_statistics_by_period("any_tag", 123, "2021-01-01")
            self.assertNotEqual(123, result["total_income"])
            self.assertNotEqual(-234, result["total_spend"])
        with self.assertRaises(TypeError):
            result = application.form_statistics_by_period("any_tag", "2021-01-01", 123)
            self.assertNotEqual(123, result["total_income"])
            self.assertNotEqual(-234, result["total_spend"])

    def test_right_add_regular_operation_type(self):
        application = BusinessEntity()
        application.add_regular_operation_type("Special name")
        self.assertEqual("Special name", application.regularOperationTypes[-1].name)

    def test_add_disabled_regular_operation_type(self):
        application = BusinessEntity()
        application.add_regular_operation_type("Тестовый")
        self.assertEqual(3, len(application.regularOperationTypes))

    def test_wrong_add_regular_operation_type(self):
        application = BusinessEntity()
        with self.assertRaises(TypeError):
            application.add_regular_operation_type(123)
            for i in range(len(application.regularOperations)):
                self.assertNotEqual(123, application.regularOperationTypes[-1].name)

    def test_send_wrong_notification(self):
        application = BusinessEntity()
        res = application.send_notification(None, None)
        self.assertEqual(res,  {'message': 'Invalid notification format and data'})
        res = application.send_notification(None, "HELLO")
        self.assertEqual(res,  {'message': 'Invalid notification format and data'})
        res = application.send_notification("HELLO", None)
        self.assertEqual(res,  {'message': 'Invalid notification format and data'})

    def test_send_right_notification(self):
        application = BusinessEntity()
        res = application.send_notification("This is test  notif", "GREAT")
        self.assertEqual(res, {'message': 'GREAT: This is test  notif'})

    def test_get_period_of_operations(self):
        application = BusinessEntity()
        res = application.get_period_of_operations()
        self.assertEqual(res, { "period" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]})

    

