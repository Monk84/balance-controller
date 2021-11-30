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
        return

    def change_balance(self):
        # Update balance
        return

    def form_statistics_by_period(self):
        return

    def add_regular_operation_type(self):
        return

    def change_regular_operation(self):
        return

    def remove_regular_operation(self):
        return

    def get_deposit_balance(self):
        # SElect
        return 0

    def get_active_regular_operations(self):
        """
        regular operation type initialization
        :returns name: str
        :returns reg_op_type
        :returns payment_amount
        :returns period
        :returns notification_period
        :returns start_date
        """
        active_operations = []
        return active_operations