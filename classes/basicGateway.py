from json.decoder import JSONDecodeError
from os import stat_result
import classes.const as const
from classes.depositBalance import DepositBalance
from classes.notification import Notification
from classes.paymentsBalance import PaymentsBalance
from classes.regularOperation import RegularOperation
from classes.regularOperationType import RegularOperationType
from classes.dbGatewayInterface import GatewayInterface
from datetime import date, timedelta, datetime
import  json 

class BasicGateway(GatewayInterface):
    def __init__(self):
        self.first_regular_operation = {"id": 1, "name": "Кредит", "reg_op_type": "Кредит", "payment_amount": -123, "period": 1, "notification_period": 7, "start_date": "2020-01-01", "active": True}
        self.second_regular_operation = {"id": 2, "name": "Аренда", "reg_op_type": "Аренда", "payment_amount": 2000, "period": 7, "notification_period": 1, "start_date": "2021-01-01", "active": True}
        self.third_reqular_operation = {"id": 3, "name": "Тестовый", "reg_op_type": "Тестовый", "payment_amount": 55, "period": 7, "notification_period": 0, "start_date": "2020-01-01", "active": False}
        self.regular_operations = [ self.first_regular_operation, self.second_regular_operation, self.third_reqular_operation]
        self.regular_operations_types = [{"id": 1, "type" :{"name": "Аренда", "op_type": 1, "status": True }}, {"id": 2, "type" :{"name": "Кредит", "op_type": 1, "status": True }},{"id": 3, "type" :{"name": "Тестовый", "op_type": 1, "status": True }}]
        self.deposit_balance = 0
        self.payments_balance = {"days": 30, "payment_amount": 15, "current_payment_limit": 150}

    def get_operation_types(self) -> list:
        """
        Getting all regular operation types with disabled.
        Returns an array of RegularOperationType objects with params:
        :param {list} name
        :param {bool} active
        """
        result = []
        for op_type in self.regular_operations:
            new_op_type = RegularOperationType(op_type["reg_op_type"], const.REG_OP_STATUS_ACTIVE)
            if not op_type["active"]:
                new_op_type.delete()
            result.append(new_op_type)
        return result
    
    def get_active_regular_operations(self) -> list:
        """
        Getting an array with active regular operations.
        Array contains RegularOperation objects with fields:
        :param {int} id
        :param {str} name
        :param {str} reg_op_type
        :param {int} payment_amount
        :param {int} period
        :param {int} notification_period
        :param {str} start_date
        """
        result = []
        active = [op for op in self.regular_operations if op["active"] == True]
        regularOperationTypes = self.get_operation_types()       
     
        for operation in active:
            for op_type in regularOperationTypes:
                if op_type.name == operation["reg_op_type"]:
                    period = timedelta(days=int(operation["period"]))
                    notification_period = timedelta(days=operation["notification_period"])
                    start_date = date(
                        year=int(operation["start_date"][:4]),
                        month=int(operation["start_date"][5:7]),
                        day=int(operation["start_date"][8:]))
                    new_reg_op = RegularOperation(operation["name"], op_type, operation["payment_amount"], period,
                                                  notification_period, start_date)
                    result.append({"id": operation["id"], "operation": new_reg_op})
        return result

    def get_deposit_balance(self) -> DepositBalance:
        """
        Gets deposit balance.
        :returns result: DepositBalance
        """
        return DepositBalance(self.deposit_balance)

    def get_payments_balance(self) -> DepositBalance:
        """
        Getting the payments balance object for the period
        :return DepositBalance
        """
        return PaymentsBalance(self.payments_balance['current_payment_limit'], timedelta(days=self.payments_balance['days'])), self.payments_balance["payment_amount"]
    
    def add_regular_operation(self, new_reg: RegularOperation) -> int:
        """
        Inserts new regular operation.
        :argument new_reg: RegularOperation
        Returns new id from DB.
        :returns id: int
        """
        tmp = new_reg.get()
        operation = tmp
        exist = False
        for op in self.regular_operations_types:
            if op["type"]["name"] == tmp["reg_op_type"].name:
                exist = True
        if exist:
            operation["id"] = len(self.regular_operations) + 1
            operation["active"] = True
            operation["reg_op_type"] = tmp["reg_op_type"].name
            self.regular_operations.append(operation)
            return operation["id"]
        return None
    
    def change_regular_operation(self, reg: dict) -> None:
        """
        Updates regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        for op in self.regular_operations:
            if op["id"] == reg["id"]:
                id = op["id"]
                tmp = reg["operation"].get()
                tmp["id"] = id
                op = tmp
                break
    
    def remove_regular_operation(self, reg: dict) -> None:
        """
        Disables regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        for operation in self.regular_operations:
            if operation["id"] == reg["id"]:
                operation["active"] = False
                break     
    
    def change_deposit_balance(self, new_balance: int) -> None:
        """
        Updates current deposit balance.
        :argument new_balance: int
        """
        self.deposit_balance = new_balance
    
    def get_operations_history_by_operation_type(self, tag: RegularOperationType, start_date: date, end_date: date) -> list:
        """
        Gets history of operations between start_date and end_date by tag.
        :argument tag: RegularOperationType
        :argument start_date: date
        :argument end_date: date
        Returns prices.
        :returns result: array with format [{"price": int}, {"price": int}, ...]
        """
        result = []
        for op in self.regular_operations:
            if tag == op["reg_op_type"]:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                i =  (end_date - start_date).days // op["period"]
                result.append({"price": op["payment_amount"]*i})
        return result
    
    def add_regular_operation_type(self, new_type: RegularOperationType) -> None:
        """
        Sets regularOperationType enabled.
        :argument operation_type: regularOperationType
        """
        cur_type = new_type.get()
        for op in self.regular_operations:
            if cur_type["name"] == op["reg_op_type"]:
                op["active"] = True
    
    def add_operation_type(self, operation_type: RegularOperationType) -> None:
        exist = False
        for op in self.regular_operations_types:
            if operation_type.name == op["type"]["name"]:
                exist = True
                break
        if not exist:
            newstr = operation_type.__repr__().replace("'", '"').replace("True", "true").replace("False", "false")
            tmp = json.loads(newstr)
            self.regular_operations_types.append({"id": len(self.regular_operations_types)+1, "type": tmp})

    
    def deactivate_operation_type(self, operation_type: RegularOperationType) -> None:
        """
        Sets regularOperationType disabled.
        :argument operation_type: regularOperationType
        """
        for op in self.regular_operations:
            if op["reg_op_type"] == operation_type.get_name():
                op["activate"] = False
    
    def set_deposit_balance(self, new_balance: int) -> None:
        self.deposit_balance = new_balance