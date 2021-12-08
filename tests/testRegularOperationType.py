import unittest

from classes import const
from classes import regularOperationType


# ----------------- REGULAR OPERATION TYPE TESTING ----------------
class TestsRegularOperationType(unittest.TestCase):

    def setUp(self):
        self.r_minus = regularOperationType.RegularOperationType('string', False)
        self.r_plus = regularOperationType.RegularOperationType('string123', True)

    def test_reg_op_type_init(self):
        self.assertEqual(self.r_minus.get_op_type(), const.OP_TYPE_EXPENSE)
        self.assertEqual(self.r_minus.get_name(), 'string')
        self.assertEqual(self.r_minus.get_status(), const.REG_OP_STATUS_ACTIVE)

        self.assertEqual(self.r_plus.get_op_type(), const.OP_TYPE_INCOME)
        self.assertEqual(self.r_plus.get_name(), 'string123')
        self.assertEqual(self.r_plus.get_status(), const.REG_OP_STATUS_ACTIVE)

        with self.assertRaises(TypeError):
            regularOperationType.RegularOperationType(['string'], False)
        with self.assertRaises(TypeError):
            regularOperationType.RegularOperationType('asd', 123)

    def test_reg_op_type_get_status(self):
        self.assertEqual(self.r_minus.get_status(), const.REG_OP_STATUS_ACTIVE)
        self.r_minus.delete()
        self.assertEqual(self.r_minus.get_status(), const.REG_OP_STATUS_INACTIVE)
        self.r_minus.add()
        self.assertEqual(self.r_minus.get_status(), const.REG_OP_STATUS_ACTIVE)

        self.assertEqual(self.r_plus.get_status(), const.REG_OP_STATUS_ACTIVE)
        self.r_plus.delete()
        self.assertEqual(self.r_plus.get_status(), const.REG_OP_STATUS_INACTIVE)
        self.r_plus.add()
        self.assertEqual(self.r_plus.get_status(), const.REG_OP_STATUS_ACTIVE)


def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(TestsRegularOperationType('test_reg_op_type_init'))
    _suite.addTest(TestsRegularOperationType('test_reg_op_type_get_status'))
    return _suite

