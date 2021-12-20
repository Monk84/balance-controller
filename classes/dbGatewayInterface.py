import classes.const as const
from classes.depositBalance import DepositBalance
from classes.notification import Notification
from classes.paymentsBalance import PaymentsBalance
from classes.regularOperation import RegularOperation
from classes.regularOperationType import RegularOperationType


class GatewayInterface:
    def add_regular_operation(self, new_reg) -> int:
        """
        Inserts new regular operation.
        :argument new_reg: RegularOperation
        Returns new id from DB.
        :returns id: int
        """
        pass
        # Insert
        # return 1

    def change_regular_operation(self, reg) -> None:
        """
        Updates regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        pass
        # return

    def remove_regular_operation(self, reg) -> None:
        """
        Disables regular operation.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        pass
        # return
    
    def activate_regular_operation(self, reg) -> None:
        """
        Sets regularOperation enabled.
        :argument reg: object with format {"id": int, "operation": RegularOperation}
        """
        pass
        # return
        
    def change_deposit_balance(self, new_balance) -> None:
        #TODO need to create history in db
        """
        Updates current deposit balance.
        :argument new_balance: int
        """
        pass
        # Update balance
        # return


    def get_operations_history_by_operation_type(self, tag, start_date, end_date) -> list:
        """
        Gets history of operations between start_date and end_date by tag.
        :argument tag: RegularOperationType 
        :argument start_date: date
        :argument end_date: date
        Returns prices.
        :returns result: array with format [{"price": int}, {"price": int}, ...]
        """
        pass
        # result = [{"price": 123}, {"price": -234}]
        # return result

    def add_regular_operation_type(self, new_type) -> None:
        """
        Inserts new regularOperationType.
        :argument new_type: regularOperationType
        """
        pass
        # return

    def get_deposit_balance(self) -> DepositBalance:
        """
        Gets deposit balance.
        :returns result: int
        """
        pass
        # return 0
        
    def set_deposit_balance(self, new_balance) -> None:
        """
        Sets deposit balance.
        :param new_balance: int
        """
        pass

    def set_payments_balance(self, new_balance) -> None:
        """
        Sets payments balance.
        :param new_balance: int
        """
        pass

    def get_active_regular_operations(self) -> list: # or list of the objects
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
        pass
        # active_operations = [{"id": 1, "name": "Кредит за машину", "reg_op_type": "Кредит", "payment_amount": -123, "period": 12, "notification_period": 23, "start_date": "2020-01-01"},
        #                      {"id": 2, "name": "Аренда квартиры", "reg_op_type": "Аренда", "payment_amount": 2000, "period": 13, "notification_period": 12, "start_date": "2021-01-01"}]
        # return active_operations

    def activate_operation_type(self, operation_type) -> None:
        """
        Sets regularOperationType enabled.
        :argument operation_type: regularOperationType
        """
        pass
        # return
        
    def deactivate_operation_type(self, operation_type) -> None:
        """
        Sets regularOperationType disabled.
        :argument operation_type: regularOperationType
        """
        pass
        # return

    def add_operation_type(self, operation_type) -> None:
        """
        Inserts new regularOperationType.
        :argument operation_type: regularOperationType
        """
        # return
        pass

    def get_operation_types(self) -> list:
        """
        Getting all regular operation types with disabled.
        Returns an array of objects with params:
        :param {str} name
        :param {bool} active
        """
        pass
        # result = [{"name": "Аренда", "active": True},
        #           {"name": "Кредит", "active": True},
        #           {"name": "Тестовый", "active": False}]
        # return result
    
    def get_payments_balance(self) -> PaymentsBalance: 
        # TODO go through the history of payments and sum the payment amount
        """
        Getting the payments balance for the period
        :param {int} days
        :param {int} payment_amount
        :param {int} current_payment_limit
        """
        pass
        # result = {"days": 30, "payment_amount": 15, "current_payment_limit": 150}
        # return result