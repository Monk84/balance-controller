from classes.paymentsBalance import PaymentsBalance
from classes.regularOperationType import RegularOperationType as rot
from classes.regularOperation import RegularOperation as ro
from datetime import timedelta as td, date as d
import unittest as ut


class TestPaymentsBalance(ut.TestCase):
    def test_exception_on_init_on_new_limit(self):
        with self.assertRaises(TypeError):
            p = PaymentsBalance('123', td(days=1))

    def test_exception_on_init_on_new_period(self):
        with self.assertRaises(TypeError):
            p = PaymentsBalance(123, 'td(days=1)')

    def test_normal_on_init(self):
        p = PaymentsBalance(123, td(days=1))
        self.assertEqual(p.get_limit(), 123)

    def test_exceptions_on_update(self):  # 2
        p = PaymentsBalance(0, td(days=1))
        cases = [(123, 12), ('123', td(days=1))]
        for c in cases:
            with self.subTest(c=c):
                with self.assertRaises(TypeError):
                    p.update(c[0], c[1])

    def test_nones_on_update(self):  # 3
        p = PaymentsBalance(123, td(days=1))
        cases = [(None, None), (123, None), (None, td(days=1)), (123, td(days=1))]
        for c in cases:
            with self.subTest(c=c):
                p.update(c[0], c[1])
                self.assertEqual(p.get_limit(), 123)

    def test_get_limit(self):
        p = PaymentsBalance(0, td(days=1))
        self.assertEqual(p.get_limit(), 0)

    def test_exception_apply_reg_ops(self):
        p = PaymentsBalance(0, td(days=2))
        with self.assertRaises(TypeError):
            p.apply_reg_operations(123)

    def test_normal_apply_reg_ops(self):
        p = PaymentsBalance(10, td(days=2))
        cases = [
            ([ro('1', rot('1', True), 7, td(days=4), td(days=1), d.today() - td(days=4)),
              ro('2', rot('1', True), 6, td(days=4), td(days=1), d.today() - td(days=4))], True),  # exceed limit
            ([ro('1', rot('1', True), 2, td(days=1), td(days=1), d.today() - td(days=3)),
              ro('2', rot('1', True), 1, td(days=2), td(days=1), d.today() - td(days=4))], False),  # not exceed limit
            ([ro('1', rot('1', True), 2, td(days=8), td(days=1), d.today() - td(days=4)),
              ro('2', rot('1', True), 1, td(days=8), td(days=1), d.today() - td(days=4))], False),  # not get in check period
            ([ro('1', rot('1', True), 2, td(days=4), td(days=1), d.today() - td(days=4)),
              ro('2', rot('1', True), 1, td(days=4), td(days=1), d.today() - td(days=4))], False),  # not get in minus day
            ([ro('1', rot('1', True), 2, td(days=4), td(days=1), d.today() - td(days=5)),
              ro('2', rot('1', True), 1, td(days=4), td(days=1), d.today() - td(days=5))], False),  # not get in plus day
        ]
        for i in range(4):
            with self.subTest(i=i):
                res = p.apply_reg_operations(cases[i][0])
                self.assertEqual(res, cases[i][1])

    def test_get_notification(self):
        p = PaymentsBalance(0, td(days=2))
        self.assertGreater(len(p.get_notification()), 0)


def suite():
    _suite = ut.TestSuite()
    _suite.addTest(TestPaymentsBalance('test_exception_on_init_on_new_limit'))
    _suite.addTest(TestPaymentsBalance('test_exception_on_init_on_new_period'))
    _suite.addTest(TestPaymentsBalance('test_normal_on_init'))
    _suite.addTest(TestPaymentsBalance('test_exceptions_on_update'))
    _suite.addTest(TestPaymentsBalance('test_nones_on_update'))
    _suite.addTest(TestPaymentsBalance('test_get_limit'))
    _suite.addTest(TestPaymentsBalance('test_exception_apply_reg_ops'))
    _suite.addTest(TestPaymentsBalance('test_normal_apply_reg_ops'))
    _suite.addTest(TestPaymentsBalance('test_get_notification'))
    return _suite

