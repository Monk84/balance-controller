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
        # getting active regular operations
        self.regularOperations = []
        active_operations = DataManager.get_active_regular_operations()
        for operation in active_operations:
            # need to fix mapping for operation
            self.regularOperations.append(RegularOperation(operation.name, operation.reg_op_type,
                                                           operation.payment_amount, operation.period,
                                                           operation.notification_period, operation.start_date))

        # getting current balance on init
        cur_dep_balance = DataManager.get_deposit_balance()
        self.deposit_balance = DepositBalance(cur_dep_balance)

        # getting operation types

    def add_regular_operation(self, name, reg_op_type, payment_amount, period, notification_period, start_date):
        new_reg = RegularOperation(name, reg_op_type, payment_amount, period, notification_period, start_date)
        if not isinstance(new_reg, RegularOperation):
            # ignore on errors
            return
        self.regularOperations.append(new_reg)
        DataManager.add_regular_operation(new_reg)

    def change_balance(self, new_balance=0):
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
            return
        self.deposit_balance.balance.set_balance(new_balance)
        DataManager.change_balance(new_balance)

    def form_statistics_by_period(self):
        return

    def add_regular_operation_type(self):
        return

    def change_regular_operation(self):
        return

    def remove_regular_operation(self):
        return
