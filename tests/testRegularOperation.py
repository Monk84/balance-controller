import datetime
import unittest
from time import sleep

from classes import const
from classes import  regularOperationType
from classes import  regularOperation


# ----------------- REGULAR OPERATION TESTING ----------------
class TestsRegularOperation(unittest.TestCase):

    def setUp(self):
        self.nw = datetime.datetime.now()
        sleep(0.3)
        self.period = datetime.datetime.now() - self.nw
        self.tod = datetime.date.today()
        self.r = regularOperation.RegularOperation(
                'name', regularOperationType.RegularOperationType('string', False),
                100, self.period, self.period, self.tod
            )

    def test_reg_op_init(self):
        meta_data = self.r.get()
        self.assertEqual(meta_data['name'], 'name')
        self.assertEqual(meta_data['reg_op_type'].__repr__(),
                         regularOperationType.RegularOperationType('string', False).__repr__())
        self.assertEqual(meta_data['payment_amount'], -100)
        self.assertEqual(meta_data['period'], self.period)
        self.assertEqual(meta_data['notification_period'], self.period)
        self.assertEqual(meta_data['start_date'], self.tod)
        self.assertEqual(meta_data['status'], const.REG_OP_STATUS_ACTIVE)

        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                ['name'], regularOperationType.RegularOperationType('string', False),
                100, self.period, self.period, self.tod
            )
        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                'name', 1, 100, self.period,
                self.period, self.tod
            )
        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                'name', regularOperationType.RegularOperationType('string', False),
                '100', self.period, self.period,
                datetime.date.today()
            )
        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                'name', regularOperationType.RegularOperationType('string', False),
                100, [], self.period, self.tod
            )
        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                'name', regularOperationType.RegularOperationType('string', False),
                100, self.period, 'asd', self.tod
            )
        with self.assertRaises(TypeError):
            regularOperation.RegularOperation(
                'name', regularOperationType.RegularOperationType('string', False),
                100, self.period, self.period,
                'datetime.date.today()'
            )

    def test_reg_op_get_notification(self):
        self.assertEqual(self.r.get_notification(),
                         'Payment: in the amount -100, date - %s' % datetime.date.today().strftime('%d:%m:%y'))

    def test_reg_op_delete(self):
        self.assertEqual(self.r.status, const.REG_OP_STATUS_ACTIVE)
        self.r.delete()
        self.assertEqual(self.r.status, const.REG_OP_STATUS_INACTIVE)
        self.r.add()
        self.assertEqual(self.r.status, const.REG_OP_STATUS_ACTIVE)

    def test_reg_op_update(self):
        self.r.update(name='nam1')
        self.assertEqual(self.r.get()['name'], 'nam1')
        self.r.update(reg_op_type=regularOperationType.RegularOperationType('not accept', False))
        self.assertEqual(self.r.get()['reg_op_type'].get_name(), 'not accept')
        self.r.update(reg_op_type=regularOperationType.RegularOperationType('not accept', True))
        self.assertEqual(self.r.get()['payment_amount'], 100)
        self.r.update(payment_amount=1000)
        self.assertEqual(self.r.get()['payment_amount'], 1000)
        sleep(0.1)
        period2 = datetime.datetime.now() - self.nw
        self.r.update(period=period2)
        self.assertEqual(self.r.get()['period'], period2)
        self.assertNotEqual(self.r.get()['period'], self.period)
        self.r.update(notification_period=period2)
        self.assertEqual(self.r.get()['notification_period'], period2)
        self.assertNotEqual(self.r.get()['notification_period'], self.period)

        with self.assertRaises(TypeError):
            self.r.update(name=['nam1'])

        with self.assertRaises(TypeError):
            self.r.update(reg_op_type="regularOperationType.RegularOperationType('not accept', False)")

        with self.assertRaises(TypeError):
            self.r.update(payment_amount=[1000])

        with self.assertRaises(TypeError):
            self.r.update(period=[123])
        with self.assertRaises(TypeError):
            self.r.update(notification_period=[123])


def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(TestsRegularOperation('test_reg_op_init'))
    _suite.addTest(TestsRegularOperation('test_reg_op_get_notification'))
    _suite.addTest(TestsRegularOperation('test_reg_op_delete'))
    _suite.addTest(TestsRegularOperation('test_reg_op_update'))
    return _suite


