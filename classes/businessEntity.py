from typing import Type
import classes.const as const
from classes.dataManager import DataManager
from classes.depositBalance import DepositBalance
from classes.notification import Notification
from classes.paymentsBalance import PaymentsBalance
from classes.regularOperation import RegularOperation
from classes.regularOperationType import RegularOperationType
from datetime import date, timedelta, datetime
from classes.notification import Notification
import re
DB = DataManager()


class BusinessEntity:
    # regularOperations = []
    # regularOperationTypes = [] -- why?

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
                    period = timedelta(days=int(operation["period"]))   # IMPORTANT FORMAT OF TIMEDELTA
                    notification_period = timedelta(days=operation["notification_period"])
                    start_date = date(
                        year=int(operation["start_date"][:4]),
                        month=int(operation["start_date"][5:7]),
                        day=int(operation["start_date"][8:]))
                    new_reg_op = RegularOperation(operation["name"], op_type, operation["payment_amount"], period, notification_period, start_date)
                    self.regularOperations.append({"id": operation["id"], "operation": new_reg_op})

        # getting current balances on init
        cur_dep_balance = DB.get_deposit_balance()
        self.deposit_balance = DepositBalance(cur_dep_balance)
        cur_paym_balance = DB.get_paymenst_balance()
        self.payments_balance = PaymentsBalance(cur_paym_balance) # constructor must be another

    def add_regular_operation(self, name, reg_op_type, payment_amount, period, notification_period, start_date):
        new_reg = RegularOperation(name, reg_op_type, payment_amount, period, notification_period, start_date)
        new_id = DB.add_regular_operation(new_reg)
        self.regularOperations.append({"id": new_id, "operation": new_reg})

    def change_regular_operation(self, operation_id, name, reg_op_type, payment_amount, period, notification_period):
        for operation in self.regularOperations:
            if operation["id"] == operation_id:
                operation["operation"].update(name, reg_op_type, payment_amount, period, notification_period)
                DB.change_regular_operation(operation)
                return


    def remove_regular_operation(self, operation_id):
        if not isinstance(operation_id, int):
            raise TypeError('Expected RegularOperationType as regular operation type')
        for i in range(len(self.regularOperations)):
            operation = self.regularOperations[i]
            if operation["id"] == operation_id:
                operation["operation"].delete()
                DB.remove_regular_operation(op)
                self.regularOperations.pop(i)
                return True
        return False

    def change_deposit_balance(self, new_balance=0):
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
        self.deposit_balance.set_balance(new_balance)
        DB.change_deposit_balance(new_balance)

    def form_statistics_by_period(self, tag, start_date, end_date):
        if not isinstance(tag, str):
            raise TypeError("form_statistics_by_period(): expected str for tag")
        if not isinstance(start_date, str):
            raise TypeError("form_statistics_by_period(): expected str for start_date")
        if not isinstance(end_date, str):
            raise TypeError("form_statistics_by_period(): expected str for end_date")
        if not re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', start_date):
            raise KeyError("Wrong format of start_date")
        if not re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', end_date):
            raise KeyError("Wrong format of end_date")
        history = DB.get_operations_history_by_operation_type(tag, start_date, end_date)
        total_income = 0
        total_spend = 0
        for operation in history:
            if operation["price"] < 0:
                total_spend += operation["price"]
            else:
                total_income += operation["price"]
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
        self.regularOperationTypes.append(new_type)
        DB.add_operation_type(new_type)
        return
        
    
    def remove_regular_operation_type(self, name):
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.name == name:
                # found exist one
                op_type.delete()
                DB.deactivate_operation_type(op_type)
                return
        # adding a new one
        new_type = RegularOperationType(name, True)
        if not isinstance(new_type, RegularOperationType):
            return
        self.regularOperationTypes.append(new_type)
        DB.add_operation_type(new_type)
        return
   
    def send_notification(self, notification_format, notification_type):
        try:
            current_notify = Notification(notification_format, notification_type)
        except:
            raise TypeError("send_notification(): Invalid notification format and data")
    
        return { "message" : current_notify.get_notification()}

    def get_period_of_operations(self):
        return { "period" : [number for number in range(1, 32)]}
  
    def set_period_of_operations(self, current_regular_operation_id, new_period):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == current_regular_operation_id:
                index = i
                break
                
        if index == None or index < 0:
            raise TypeError("set_period_of_operations: Invalid operation id")
       
        if isinstance(new_period, int): 
                if new_period <= 0:
                    raise TypeError("set_period_of_operations(): Set positive integer for the period value")
        else:
            raise TypeError("set_period_of_operations(): Set positive integer for the period value")

        
        self.regularOperations[index].update(period=timedelta(new_period))
        
        DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})   
        return {"message": "Successfully update period"}

    def get_operation_types(self):
        items = self.regularOperationTypes
        return [x.__repr__() for x in items]

    def set_operation_type(self, operation_id, type):
        index = None 
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index == None:
            raise TypeError("set_operation_type(): Invalid operation id")
        
        try:
            self.regularOperations[index]["operation"].update(reg_op_type=type)
        except Exception:
            raise TypeError("set_operation_type(): Set correct RegularOperationType for update")
        
        DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})
        return {"message": "Successfully update type"}

    def get_notifications_settings(self, operation_id):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index == None:
            raise TypeError("get_notifications_settings(): Invalid operation id")
        
        operation = self.regularOperations[index]["operation"].get()
        return { "data": {
            'period': operation["period"],
            'notification_period': operation["notification_period"],
            'start_date': operation["start_date"]
            }
        }
    
    def update_notification_settings(self, operation_id, period = None, notification_period = None):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index == None:
            raise TypeError("update_notification_settings(): Invalid operation id")
        
        if not period and not notification_period:
            raise TypeError("update_notification_settings(): Set positive value for period parameters")

        if period:
            if isinstance(period, int): 
                if period <= 0:
                    raise TypeError("update_notification_settings(): Set positive integer for the period value")
                self.regularOperations[index]["operation"].update(period=timedelta(period)) 
            else:
                raise TypeError("update_notification_settings(): Set positive integer for the period value")     

        if notification_period: 
            if isinstance(notification_period, int): 
                if notification_period <= 0:
                    raise TypeError("update_notification_settings(): Set positive integer for the notification_period value")     
                self.regularOperations[index]["operation"].update(notification_period=timedelta(notification_period))
            else:
                raise TypeError("update_notification_settings(): Set positive integer for the notification_period value")
        
        DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})     
        return {"message": "Successfully update notification settings"}

    def execute_operation(self, operation_id):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        if index == None:
            raise TypeError("get_notifications_settings(): Invalid operation id")
        
        operation = self.regularOperations[index]["operation"].get()

        self.deposit_balance.set_balance(self.deposit_balance.get_balance() - operation["payment_amount"])
        DB.change_deposit_balance(self.deposit_balance.get_balance())
        return {"message": "Successfully updated deposit balance"}
    
    def get_balance(self):
        return self.deposit_balance.get_balance()

    def show_operations(self):
        ops_to_sort = []
        today = datetime.date.today()
        for op in self.regularOperations:
            op_attrs = op['operation'].get()
            start_date = op_attrs['start_date']
            period = op_attrs['period']
            i = 0
            while today > start_date + period * i:
                i += 1
            ops_to_sort += [(today - (start_date + period * (i - 1)).days, op)]
        return sorted(ops_to_sort, key=lambda x : x[1])
    
    def set_payments_limit(self, new_limit=None, new_period=None):
        self.payments_balance.update(new_limit, new_period)
    
    def set_balance_limit(self, new_limit=None, new_period=None):
        self.deposit_balance.update(new_limit, new_period)
    
    def daily_check(self):
        if self.deposit_balance.apply_reg_ops(self.regularOperations):
            print(self.deposit_balance.get_notification().get_notification())
        DB.set_deposit_balance(self.deposit_balance.get_balance())
        
        if self.payments_balance.apply_reg_ops(self.regularOperations):
            print(self.payments_balance.get_notification().get_notification())
        DB.set_payments_balance(self.payments_balance.get_balance())

    def secret_menu_recovery(self, operations_to_recover):
        for op in operations_to_recover:
            DB.activate_regular_operation(op)
            op.add()