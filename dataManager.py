import const
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType


class DataManager:
    def __init__(self):
        #  add connection to DB or anything else
        return

    def add_regular_operation(self, new_reg):
        # Insert
        return

    def change_regular_operation(self, reg):
        # Update
        return

    def remove_regular_operation(self, reg):
        # set it disabled
        return

    def change_balance(self):
        # Update balance
        return

    def get_operations_history_by_operation_type(self, tag, start_date, end_date):
        # SELECT price ... WHERE tag.. and date between start_date and end_date
        result = [{"price": 123}, {"price": -234}]
        return result

    def add_regular_operation_type(self):
        return

    def get_deposit_balance(self):
        # SElect
        return 0

    def get_active_regular_operations(self):
        """
        Getting active regular operations info
        :returns name: str
        :returns reg_op_type
        :returns payment_amount
        :returns period
        :returns notification_period
        :returns start_date
        """
        active_operations = []
        return active_operations

    def activate_operation_type(self, operation_type):
        # Update ...
        return

    def add_operation_type(self, operation_type):
        # INSERT ...
        return

    def get_operation_types(self):
        # getting all types(active and disabled
        """
        Getting all regular operation types
        :returns name: str
        :returns reg_op_type
        :returns payment_amount
        :returns period
        :returns notification_period
        :returns start_date
        """
        result = [{}]
        return