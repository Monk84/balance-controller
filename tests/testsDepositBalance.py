from classes.depositBalance import DepositBalance
from classes.regularOperationType import RegularOperationType as rot
from classes.regularOperation import RegularOperation as ro
from datetime import timedelta as td, date as d
import unittest as ut


class TestDepositBalance(ut.TestCase):
    def test_exception_on_init(self):
        with self.assertRaises(TypeError):
            p = DepositBalance('123')

    def test_normal_on_init(self):
        p = DepositBalance(123)
        self.assertEqual(p.get_balance(), 123)

    def test_get_balance(self):
        p = DepositBalance(0)
        self.assertEqual(p.get_balance(), 0)

    def test_exception_on_set_limit(self):
        p = DepositBalance(0)
        with self.assertRaises(TypeError):
            p.set_limit('123')

    def test_normal_set_limit(self):
        p = DepositBalance(0)
        p.set_limit(new_limit=123)
        self.assertEqual(p.get_limit(), 123)

    def test_get_limit(self):
        p = DepositBalance(0)
        self.assertEqual(p.get_limit(), 0)

    def test_get_notification(self):
        p = DepositBalance(0)
        self.assertGreater(len(p.get_notification()), 0)

    def test_apply_reg_op_exception(self):
        p = DepositBalance(0)
        with self.assertRaises(TypeError):
            res = p.apply_reg_operation(1)

    def test_apply_reg_op_not_today(self):
        p = DepositBalance(0)
        res = p.apply_reg_operation(ro(name='1', reg_op_type=rot(name='1', op_type=True), payment_amount=2,
                                       period=td(days=5),
                                       notification_period=td(days=1),
                                       start_date=d.today() - td(days=3)))
        self.assertFalse(res)

    def test_apply_reg_op_today_not_excess_balance(self):
        p = DepositBalance(0)
        p.set_limit(100)
        res = p.apply_reg_operation(ro(name='1', reg_op_type=rot(name='1', op_type=True), payment_amount=2,
                                       period=td(days=1),
                                       notification_period=td(days=1),
                                       start_date=d.today() - td(days=3)))
        self.assertFalse(res)

    def test_apply_reg_op_today_excess_balance(self):
        p = DepositBalance(0)
        p.set_limit(100)
        res = p.apply_reg_operation(ro(name='1', reg_op_type=rot(name='1', op_type=True), payment_amount=200,
                                       period=td(days=1),
                                       notification_period=td(days=1),
                                       start_date=d.today() - td(days=3)))
        self.assertTrue(res)


def suite():
    _suite = ut.TestSuite()
    _suite.addTest(TestDepositBalance('test_exception_on_init'))
    _suite.addTest(TestDepositBalance('test_normal_on_init'))
    _suite.addTest(TestDepositBalance('test_get_balance'))
    _suite.addTest(TestDepositBalance('test_exception_on_set_limit'))
    _suite.addTest(TestDepositBalance('test_normal_set_limit'))
    _suite.addTest(TestDepositBalance('test_get_limit'))
    _suite.addTest(TestDepositBalance('test_get_notification'))
    _suite.addTest(TestDepositBalance('test_apply_reg_op_exception'))
    _suite.addTest(TestDepositBalance('test_apply_reg_op_not_today'))
    _suite.addTest(TestDepositBalance('test_apply_reg_op_today_not_excess_balance'))
    _suite.addTest(TestDepositBalance('test_apply_reg_op_today_excess_balance'))
    return _suite

