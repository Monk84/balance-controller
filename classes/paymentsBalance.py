from classes.notification import Notification
import datetime


class PaymentsBalance:
    def __init__(self, new_limit, new_period):  # 3 tests required
        if not isinstance(new_limit, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
        if not isinstance(new_period, datetime.timedelta):
            raise TypeError("PaymentBalance: expected timedelta for new_period")
        self.limit = new_limit
        self.period = new_period
        self.current_value = 0
        self.notification = Notification("пересечен лимит {limit}", "Баланс платежей")

    def update(self, new_limit=None, new_period=None):  # 7 tests required
        if new_limit and not isinstance(new_limit, int):
            raise TypeError("PaymentBalance: expected int for new_limit")
        if new_period and not isinstance(new_period, datetime.timedelta):
            raise TypeError("PaymentBalance: expected timedelta for new_period")

        if new_limit:
            self.limit = new_limit
        if new_period:
            self.period = new_period

    def get_limit(self):
        return self.limit

    def apply_reg_operations(self, reg_ops):  # 8 tests required
        if not isinstance(reg_ops, list):
            raise TypeError("PaymentBalance: expected list(RegularOperation) for reg_ops")
        curr_date = datetime.date.today()
        old = self.current_value > self.limit  # save it to check relation later
        for op in reg_ops:
            op_attrs = op.get()
            begin_date = op_attrs['start_date']
            period = op_attrs['period']
            period_min = curr_date - self.period  # starting date of check
            i = 0
            while period_min > begin_date + period * i:
                i += 1
            if period_min > begin_date + period * (i - 1) and (period_min - (begin_date + period * (i - 1))).days == 1:
                self.current_value -= op_attrs['payment_amount']
            while curr_date > begin_date + period * i:
                i += 1
            if curr_date == begin_date + period * i:
                self.current_value += op_attrs['payment_amount']
        if (self.current_value > self.limit) != old:
            return True
        return False

    def get_notification(self):
        return self.notification.get_notification({'limit': self.limit})

# TODO summary: 21 tests required
