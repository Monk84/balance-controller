from typing import Type
import classes.const as const
# from classes.dataManager import DataManager
from classes.basicGateway import BasicGateway
from classes.depositBalance import DepositBalance
from classes.notification import Notification
from classes.paymentsBalance import PaymentsBalance
from classes.regularOperation import RegularOperation
from classes.regularOperationType import RegularOperationType
from datetime import date, timedelta, datetime
from classes.notification import Notification
import re
# DB = DataManager()
import json 

class BusinessEntity:
    # regularOperations = []
    # regularOperationTypes = [] -- why?

    def __init__(self):
        # setting flags
        self.DB = BasicGateway()
        self.is_balance_displayed = False
        self.is_reg_displayed = False
        self.is_reg_op_types_displayed = False
        self.is_period_list_displayed = False
        # getting operation types
        self.regularOperationTypes = self.DB.get_operation_types()
        # getting active regular operations
        self.regularOperations = self.DB.get_active_regular_operations()
        # getting current balances on init
        self.deposit_balance = self.DB.get_deposit_balance()
        self.payments_balance,cur_paym_balance = self.DB.get_payments_balance()
        self.payments_balance.apply_reg_operations([RegularOperation('', RegularOperationType('', True),
                                                                     cur_paym_balance,
                                                                     timedelta(days=1),
                                                                     timedelta(days=1),
                                                                     date.today())])

    def add_regular_operation(self, name, reg_op_type, payment_amount, period, notification_period, start_date):
        new_reg = RegularOperation(name, reg_op_type, payment_amount, period, notification_period, start_date)
        new_id = self.DB.add_regular_operation(new_reg)
        self.regularOperations.append({"id": new_id, "operation": new_reg})

    #TODO не работает, когда названия name и req_op_type в операции отличаются (стр 12-14 в basicGateWay)
    def change_regular_operation(self, operation_id, name, reg_op_type, payment_amount, period, notification_period):
        if not self.is_reg_displayed:
            raise KeyError("Wrong order")
        for operation in self.regularOperations:
            if operation["id"] == operation_id:
                operation["operation"].update(name, reg_op_type, payment_amount, period, notification_period)
                self.DB.change_regular_operation(operation)
                return

    def remove_regular_operation(self, operation_id):
        if not self.is_reg_displayed:
            raise KeyError("Wrong order")
        if not isinstance(operation_id, int):
            raise TypeError('Expected RegularOperationType as regular operation type')
        for i in range(len(self.regularOperations)):
            operation = self.regularOperations[i]
            if operation["id"] == operation_id:
                operation["operation"].delete()
                self.DB.remove_regular_operation(operation) #TODO было достаточно айдишника, есть смысл поменять
                self.regularOperations.pop(i)
                return True
        return False

    def change_deposit_balance(self, new_balance=0):
        if not self.is_balance_displayed:
            raise KeyError("Wrong order")
        self.is_balance_displayed = False
        if not isinstance(new_balance, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
        self.deposit_balance.set_balance(new_balance)
        self.DB.change_deposit_balance(new_balance)

    def form_statistics_by_period(self, tag, start_date, end_date):
        #TODO in the code were just a string
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
        history = self.DB.get_operations_history_by_operation_type(tag, start_date, end_date)
        total_income = 0
        total_spend = 0
        for operation in history:
            if operation["price"] < 0:
                total_spend += operation["price"]
            else:
                total_income += operation["price"]
        return {"total_income": total_income, "total_spend": total_spend, "start_date": start_date, "end_date": end_date}

    def add_regular_operation_type(self, name):
        if not self.is_reg_op_types_displayed:
            raise KeyError("Wrong order")
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.name == name:
                # found exist one
                op_type.add()
                self.DB.activate_operation_type(op_type) #TODO maybe id is ehough?
                return
        # adding a new one
        new_type = RegularOperationType(name, True)
        self.regularOperationTypes.append(new_type)
        self.DB.add_operation_type(new_type)
        return

    def remove_regular_operation_type(self, name):
        if not self.is_reg_op_types_displayed:
            raise KeyError("Wrong order")
        # search for exists op types(even deleted)
        for op_type in self.regularOperationTypes:
            if op_type.get_name() == name:
                # found exist one
                op_type.delete()
                self.DB.deactivate_operation_type(op_type)
                return True
        return False
   
    def send_notification(self, notification_format, notification_type):
        try:
            current_notify = Notification(notification_format, notification_type)
        except:
            raise TypeError("send_notification(): Invalid notification format and data")
    
        return {"message": current_notify.get_notification()}

    def get_period_of_operations(self):
        self.is_period_list_displayed = True
        return {"period": [number for number in range(1, 32)]}
  
    def set_period_of_operations(self, current_regular_operation_id, new_period):
        if not self.is_period_list_displayed:
            raise KeyError("wrong order")
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == current_regular_operation_id:
                index = i
                break
                
        if index is None or index < 0:
            raise TypeError("set_period_of_operations: Invalid operation id")
       
        if isinstance(new_period, int): 
            if new_period <= 0:
                raise TypeError("set_period_of_operations(): Set positive integer for the period value")
        else:
            raise TypeError("set_period_of_operations(): Set positive integer for the period value")

        self.regularOperations[index].update(period=timedelta(new_period))
        
        self.DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})   
        self.is_period_list_displayed = False
        return {"message": "Successfully update period"}

    def get_operation_types(self):
        self.is_reg_op_types_displayed = True
        items = self.regularOperationTypes
        res = [x.__repr__() for x in items if x.get_op_type() == const.REG_OP_STATUS_ACTIVE]
        for i in res:
            tmp = json.dumps(i, ensure_ascii=False)
            i = tmp
        return res

    def set_operation_type(self, operation_id, type):
        if not self.is_reg_op_types_displayed:
            raise KeyError("Wrong order")
        index = None 
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index is None:
            raise TypeError("set_operation_type(): Invalid operation id")
        
        self.regularOperations[index]["operation"].update(reg_op_type=type)
        
        self.DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})
        self.is_reg_op_types_displayed = False
        return {"message": "Successfully update type"}

    def get_notifications_settings(self, operation_id):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index is None:
            raise TypeError("get_notifications_settings(): Invalid operation id")
        
        operation = self.regularOperations[index]["operation"].get()
        return {"data": {
            'period': operation["period"],
            'notification_period': operation["notification_period"],
            'start_date': operation["start_date"]
            }
        }
    
    def update_notification_settings(self, operation_id, period=None, notification_period=None):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        
        if index is None:
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
        
        self.DB.change_regular_operation({"id": self.regularOperations[index]["id"], "operation": self.regularOperations[index]["operation"]})     
        return {"message": "Successfully update notification settings"}

    def execute_operation(self, operation_id):
        index = None
        for i in range(len(self.regularOperations)):
            if self.regularOperations[i]["id"] == operation_id:
                index = i
                break
        if index is None:
            raise TypeError("get_notifications_settings(): Invalid operation id")
        
        operation = self.regularOperations[index]["operation"].get()

        self.deposit_balance.set_balance(self.deposit_balance.get_balance() - operation["payment_amount"])
        self.DB.change_deposit_balance(self.deposit_balance.get_balance())
        return {"message": "Successfully updated deposit balance"}
    
    def get_balance(self):
        self.is_balance_displayed = True
        return self.deposit_balance.get_balance()

    def show_operations(self):
        self.is_reg_displayed = True
        ops_to_sort = []
        today = date.today()
        for op in [x for x in self.regularOperations if x['operation'].get()['status'] == const.REG_OP_STATUS_ACTIVE]:
            op_attrs = op['operation'].get()
            start_date = op_attrs['start_date']
            period = op_attrs['period']
            i = 0
            while today > start_date + period * i:
                i += 1
            ops_to_sort += [((today - (start_date + period * (i - 1))).days, op)]
        return sorted(ops_to_sort, key=lambda x: x[0])
    
    def set_payments_limit(self, new_limit=None, new_period=None):
        self.payments_balance.update(new_limit, new_period)
    
    def set_balance_limit(self, new_limit=None):
        self.deposit_balance.set_limit(new_limit)
    
    def daily_check(self):
        is_dep_balance_exceeded = False
        for op in self.regularOperations:
            if self.deposit_balance.apply_reg_operation(op):
                is_dep_balance_exceeded = True
        if is_dep_balance_exceeded:
            print(self.deposit_balance.get_notification().get_notification())
        self.DB.set_deposit_balance(self.deposit_balance.get_balance())
        
        if self.payments_balance.apply_reg_operations(self.regularOperations):
            print(self.payments_balance.get_notification().get_notification())
        #  self.DB.set_payments_balance(self.payments_balance.get_balance())

    def secret_menu_recovery(self, operations_to_recover):
        for op in operations_to_recover:
            self.DB.activate_regular_operation(op)
            op['operation'].add()

