import classes.const as const
from classes.depositBalance import DepositBalance
from classes.notification import Notification
from classes.paymentsBalance import PaymentsBalance
from classes.regularOperation import RegularOperation
from classes.regularOperationType import RegularOperationType
from classes.dbGatewayInterface import GatewayInterface
from datetime import date, timedelta

class BasicGateway(GatewayInterface):
    def __init__(self):
        # self.first_regular_operation = {"id": 1, "name": "Кредит за машину", "reg_op_type": "Кредит", "payment_amount": -123, "period": 12, "notification_period": 23, "start_date": "2020-01-01", "active": True}
        # self.second_regular_operation = {"id": 2, "name": "Аренда квартиры", "reg_op_type": "Аренда", "payment_amount": 2000, "period": 13, "notification_period": 12, "start_date": "2021-01-01", "active": True}
        # self.third_reqular_operation = {"id": 3, "name": "Тестовый", "reg_op_type": "Тестовый", "payment_amount": 55, "period": 8, "notification_period": 12, "start_date": "2021-01-01", "active": False}

        self.first_regular_operation = {"id": 1, "name": "Кредит", "reg_op_type": "Кредит", "payment_amount": -123, "period": 12, "notification_period": 23, "start_date": "2020-01-01", "active": True}
        self.second_regular_operation = {"id": 2, "name": "Аренда", "reg_op_type": "Аренда", "payment_amount": 2000, "period": 13, "notification_period": 12, "start_date": "2021-01-01", "active": True}
        self.third_reqular_operation = {"id": 3, "name": "Тестовый", "reg_op_type": "Тестовый", "payment_amount": 55, "period": 8, "notification_period": 12, "start_date": "2021-01-01", "active": False}
        self.regular_operations = [ self.first_regular_operation, self.second_regular_operation, self.third_reqular_operation]
        self.deposit_balance = 0
        self.payments_balance = {"days": 30, "payment_amount": 15, "current_payment_limit": 150}

    def get_operation_types(self) -> list:
        """
        Getting all regular operation types with disabled.
        Returns an array of RegularOperationType objects with params:
        :param {list} name
        :param {bool} active
        """
        #TODO maybe return ID too?
        result = []
        for op_type in self.regular_operations:
            new_op_type = RegularOperationType(op_type["name"], const.REG_OP_STATUS_ACTIVE) # тут должен быть тогда другой параметр op_type["reg_op_type"], не op_type["name"]
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
        operation = new_reg.get()
        operation["id"] = len(self.regular_operations) + 1
        operation["active"] = True
        self.regular_operations.append(operation)
        return operation["id"]
    
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
        #TODO добавить проверку, что попали в end date,  И Вообще как это учитывать то ? тупо плюсовать период?
        result = []
        for op in self.regular_operations:
            result.append({"price": op["payment_amount"]})
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
        #TODO тип операции может ли существовать без операции? надо продумать как это хранить и как инициировать тут. Пока решение временное
        # судя из строки 141 businessEntity нельзя...
        self.regular_operations.append({"id": "", "reg_op_type": operation_type.get_name()})
    
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