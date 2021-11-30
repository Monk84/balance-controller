import const
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType


class DataManager:
    regularOperations = []
    def __init__(self):
        self.regularOperations = []

    def add_regular_operation(self, new_reg):
        return True

    def change_balance(self):
        return

    def form_statistics_by_period(self):
        return

    def add_regular_operation_type(self):
        return

    def change_regular_operation(self):
        return

    def remove_regular_operation(self):
        return