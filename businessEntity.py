import const
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType
from dataManager import DataManager


class BusinessEntity:
    regularOperations = []
    def __init__(self):
        self.regularOperations = []

    def add_regular_operation(self):
        new_reg = RegularOperation()
        self.regularOperations.append(new_reg)
        return

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