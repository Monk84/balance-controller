import const
from dataManager import DataManager
from depositBalance import DepositBalance
from notification import Notification
from paymentsBalance import PaymentsBalance
from regularOperation import RegularOperation
from regularOperationType import RegularOperationType
from datetime import date, timedelta

DB = DataManager()


class BusinessEntity:
    regularOperations = []
    regularOperationTypes = []

    def __init__(self):
        # getting operation types
        self.regularOperationTypes = []
        all_types = DB.get_operation_types()
        for op_type in all_types:
            # we do not use op_type in RegularOperationType __init__
            new_op_type = RegularOperationType(op_type["name"], const.REG_OP_STATUS_ACTIVE)
            if not op_type["active"]:
                new_op_type.delete()
            self.regularOperationTypes.append(new_op_type)

        # getting active regular operations
        self.regularOperations = []
        active_operations = DB.get_active_regular_operations()
        for operation in active_operations:
            # searching for RegularOperationType
            for op_type in self.regularOperationTypes:
                if op_type.name == operation["reg_op_type"]:
                    # building dates and RegularOperation
                    period = timedelta(days=float(operation["period"]))   # IMPORTANT FORMAT OF TIMEDELTA
                    notification_period = timedelta(days=operation["notification_period"]) # IMPORTANT FORMAT OF TIMEDELTA
                    start_date = date(
                        year=int(operation["start_date"][:4]),
                        month=int(operation["start_date"][5:7]),
                        day=int(operation["start_date"][8:]))
                    new_reg_op = RegularOperation(operation["name"], op_type, operation["payment_amount"], period, notification_period, start_date)
                    self.regularOperations.append({"id": operation["id"], "operation": new_reg_op})

        # getting current balance on init
        cur_dep_balance = DB.get_deposit_balance()
        self.deposit_balance = DepositBalance(cur_dep_balance)
        # **add here limits



    def add_regular_operation(self, name, reg_op_type, payment_amount, period, notification_period, start_date):
        new_reg = RegularOperation(name, reg_op_type, payment_amount, period, notification_period, start_date)
        if not isinstance(new_reg, RegularOperation):
            return
        new_id = DB.add_regular_operation(new_reg)
        self.regularOperations.append({"id": new_id, "operation": new_reg})

    def change_regular_operation(self, operation_id, name, reg_op_type, payment_amount, period, notification_period):
        for operation in self.regularOperations:
            if operation["id"] == operation_id:
                operation["operation"].update(name, reg_op_type, payment_amount, period, notification_period)
                DB.change_regular_operation(operation)
                return

    def remove_regular_operation(self, operation_id):
        for i in range(len(self.regularOperations)):
            operation = self.regularOperations[i]
            if operation["id"] == operation_id:
                operation["operation"].delete()
                DB.remove_regular_operation(operation)
                self.regularOperations.pop(i)
                return

    def change_deposit_balance(self, new_balance=0):
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
            return
        self.deposit_balance.balance.set_balance(new_balance)
        DB.change_deposit_balance(new_balance)

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
        history = DB.get_operations_history_by_operation_type(tag, start_date, end_date)
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
                DB.activate_operation_type(op_type)
                return
        # adding a new one
        new_type = RegularOperationType(name, True)
        if not isinstance(new_type, RegularOperationType):
            return
        self.regularOperationTypes.append(new_type)
        DB.add_operation_type(new_type)
        return


