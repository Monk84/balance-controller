import const
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType
from dataManager import DataManager


class BusinessEntity:
    regularOperations = []
    regularOperationTypes = []

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
            return
        self.regularOperations.append(new_reg)
        DataManager.add_regular_operation(new_reg)

    def change_regular_operation(self, operation_id, name, reg_op_type, payment_amount, period, notification_period):
        for operation in self.regularOperations:
            if operation.operation_id == operation_id:
                operation.update(name, reg_op_type, payment_amount, period, notification_period)
                DataManager.change_regular_operation(operation)
                return

    def remove_regular_operation(self, operation_id):
        for i in range(len(self.regularOperations)):
            operation = self.regularOperations[i]
            if operation.operation_id == operation_id:
                operation.delete()
                DataManager.remove_regular_operation(operation)
                self.regularOperations.pop(i)
                return

    def change_balance(self, new_balance=0):
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
            return
        self.deposit_balance.balance.set_balance(new_balance)
        DataManager.change_balance(new_balance)

    def form_statistics_by_period(self, tag, start_date, end_date):
        if not isinstance(tag, str):
            raise TypeError("form_statistics_by_period(): expected str for tag")
            return
        if not isinstance(start_date, str):
            raise TypeError("form_statistics_by_period(): expected str for start_date")
            return
        if not isinstance(end_date, str):
            raise TypeError("form_statistics_by_period(): expected str for end_date")
            return
        history = DataManager.get_operations_history_by_operation_type(tag, start_date, end_date)
        total_income = 0
        total_spend = 0
        for operation in history:
            if operation.price < 0:
                total_spend += operation.price
            else:
                total_income += operation.price
        return {"total_income": total_income, "total_spend": total_spend, "start_date": start_date, "end_date": end_date}

    def add_regular_operation_type(self, name):
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.name == name:
                # found exist one
                op_type.add()
                DataManager.activate_operation_type(op_type)
                return
        # adding a new one
        new_type = RegularOperationType(name, const.REG_OP_STATUS_ACTIVE)
        if not isinstance(new_type, RegularOperationType):
            return
        self.regularOperationTypes.append(new_type)
        DataManager.add_operation_type(new_type)
        return


