
from datetime import date, timedelta
# импорт наших библиотек
import classes.const as const
from classes.regularOperationType import RegularOperationType
from classes.notification import Notification


# описание класса регулярной операции
class RegularOperation:  # 22 tests
    def __init__(self, name, reg_op_type, payment_amount, period, notification_period, start_date):  # 7 branches
        # проверка инициализирующих аргументов
        if not isinstance(name, str):
            raise TypeError('Expected string as regular operation type name')

        if not isinstance(reg_op_type, RegularOperationType):
            raise TypeError('Expected RegularOperationType as regular operation type')

        if not isinstance(payment_amount, int):
            raise TypeError('Expected integer as payment amount')

        if not isinstance(period, timedelta):
            raise TypeError('Expected timedelta as period')

        if not isinstance(notification_period, timedelta):
            raise TypeError('Expected timedelta as notification period')

        if not isinstance(start_date, date):
            raise TypeError('Expected date as start date')

        self.name = name
        self.reg_op_type = reg_op_type
        self.payment_amount = self.reg_op_type.get_op_type() * abs(payment_amount)
        self.period = period
        self.notification_period = notification_period
        self.start_date = start_date
        self.status = self.reg_op_type.get_status()

        op_type = const.OP_TYPE_INCOME_STR if self.reg_op_type.get_op_type() == const.OP_TYPE_INCOME else const.OP_TYPE_EXPENSE_STR
        self.notification = Notification('in the amount {payment_amount}, date - {date}', op_type)

    def update(self, name=None, reg_op_type=None, payment_amount=None, period=None, notification_period=None):  # 11 branches
        # проверка инициализирующих аргументов
        if name and not isinstance(name, str):
            raise TypeError('Expected string as regular operation type name')

        if reg_op_type and not isinstance(reg_op_type, RegularOperationType):
            raise TypeError('Expected RegularOperationType as regular operation type')

        if payment_amount and not isinstance(payment_amount, int):
            raise TypeError('Expected integer as payment amount')

        if period and not isinstance(period, timedelta):
            raise TypeError('Expected timedelta as period')

        if notification_period and not isinstance(notification_period, timedelta):
            raise TypeError('Expected timedelta as notification period')

        if name:
            self.name = name

        if reg_op_type:
            self.reg_op_type = reg_op_type
            self.payment_amount = self.reg_op_type.get_op_type() * abs(self.payment_amount)
            op_type = const.OP_TYPE_INCOME_STR if self.reg_op_type.get_op_type() == const.OP_TYPE_INCOME else const.OP_TYPE_EXPENSE_STR
            self.notification.update(notification_type=op_type)

        if payment_amount:
            self.payment_amount = payment_amount
            self.payment_amount = self.reg_op_type.get_op_type() * abs(self.payment_amount)

        if period:
            self.period = period

        if notification_period:
            self.notification_period = notification_period

    def delete(self):  # 1 branch
        self.status = const.REG_OP_STATUS_INACTIVE

    def add(self):  # 1 branch
        self.status = const.REG_OP_STATUS_ACTIVE

    def get_notification(self):  # 1 branch
        date_today = date.today().strftime('%d:%m:%y')
        return self.notification.get_notification({'payment_amount': self.payment_amount, 'date': date_today})

    def get(self):  # 1 branch
        meta_data = {
            'name': self.name,
            'reg_op_type': self.reg_op_type,
            'payment_amount': self.payment_amount,
            'period': self.period,
            'notification_period': self.notification_period,
            'start_date': self.start_date,
            'status': self.status,
        }
        return meta_data

