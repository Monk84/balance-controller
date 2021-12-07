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
        """
        Inserts new regular operation.
        :argument new_reg: RegularOperation
        Returns new id from DB.
        :returns id: int
        """
        # Insert
        return 1

    def change_regular_operation(self, reg):
        """
        Updates regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        return

    def remove_regular_operation(self, reg):
        """
        Disables regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        return
    
    def activate_regular_operation(self, reg):
        """
        Sets regularOperation enabled.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        return
        
    def change_deposit_balance(self, new_balance):
        """
        Updates current deposit balance.
        :argument new_balance: int
        """
        # Update balance
        return


    def get_operations_history_by_operation_type(self, tag, start_date, end_date):
        """
        Gets history of operations between start_date and end_date by tag.
        :argument tag: RegularOperationType
        :argument start_date: date
        :argument end_date: date
        Returns prices.
        :returns result: array with format [{"price": int}, {"price": int}, ...]
        """
        result = [{"price": 123}, {"price": -234}]
        return result

    def add_regular_operation_type(self, new_type):
        """
        Inserts new regularOperationType.
        :argument new_type: regularOperationType
        """
        return

    def get_deposit_balance(self):
        """
        Gets deposit balance.
        :returns result: int
        """
        return 0
        
    def set_deposit_balance(self, new_balance):
        """
        Sets deposit balance.
        :param new_balance: int
        """

    def set_payments_balance(self, new_balance):
        """
        Sets payments balance.
        :param new_balance: int
        """


    def get_active_regular_operations(self):
        """
        Getting an array with active regular operations.
        Array contains objects with fields:
        :param {int} id
        :param {str} name
        :param {str} reg_op_type
        :param {int} payment_amount
        :param {int} period
        :param {int} notification_period
        :param {str} start_date
        """
        active_operations = [{"id": 1, "name": "Кредит за машину", "reg_op_type": "Кредит", "payment_amount": -123, "period": 12, "notification_period": 23, "start_date": "2020-01-01"},
                             {"id": 2, "name": "Аренда квартиры", "reg_op_type": "Аренда", "payment_amount": 2000, "period": 13, "notification_period": 12, "start_date": "2021-01-01"}]
        return active_operations

    def activate_operation_type(self, operation_type):
        """
        Sets regularOperationType enabled.
        :argument operation_type: regularOperationType
        """
        return
        
    def deactivate_operation_type(self, operation_type):
        """
        Sets regularOperationType disabled.
        :argument operation_type: regularOperationType
        """
        return

    def add_operation_type(self, operation_type):
        """
        Inserts new regularOperationType.
        :argument operation_type: regularOperationType
        """
        return

    def get_operation_types(self):
        """
        Getting all regular operation types with disabled.
        Returns an array of objects with params:
        :param {str} name
        :param {bool} active
        """
        result = [{"name": "Аренда", "active": True},
                  {"name": "Кредит", "active": True},
                  {"name": "Тестовый", "active": False}]
        return result