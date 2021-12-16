from classes.notification import Notification
from classes.regularOperation import RegularOperation
import datetime


class DepositBalance:
    def __init__(self, new_balance):
        if not isinstance(new_balance, int):  # 2 tests required - 2 done
            raise TypeError("DepositBalance: expected int for new_balance")
        self.balance = new_balance
        self.limit = 0
        self.notification = Notification("пересечен лимит {limit}", "Баланс счета")

    def get_balance(self):
        return self.balance

    def set_balance(self, new_balance):
        if not isinstance(new_balance, int):  # 2 tests required
            raise TypeError("DepositBalance: expected int for new_balance")
        self.balance = new_balance

    def apply_reg_operation(self, reg_op):  # 4 tests required
        if not isinstance(reg_op, RegularOperation):
            raise TypeError("DepositBalance: expected RegularOperation as reg_op")
        old = self.balance > self.limit
        curr_date = datetime.date.today()
        op_attrs = reg_op.get()
        begin_date = op_attrs['start_date']
        period = op_attrs['period']
        i = 0
        while curr_date > begin_date + period * i:
            i += 1
        if curr_date == begin_date + period * i:
            self.balance += op_attrs['payment_amount']
            if (self.balance > self.limit) != old:
                return True
        return False

    def set_limit(self, new_limit):  # 2 tests required
        if not isinstance(new_limit, int):
            raise TypeError("DepositBalance: expected int as new_limit")
        self.limit = new_limit

    def get_limit(self):
        return self.limit

    def get_notification(self):
        return self.notification.get_notification({'limit': self.limit})

# TODO summary: 12 tests required
