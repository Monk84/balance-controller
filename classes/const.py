
# возможные типы операций: зачисление/платеж
OP_TYPE_INCOME = 1
OP_TYPE_EXPENSE = -1
OP_TYPE_INCOME_STR = 'Enrollment'
OP_TYPE_EXPENSE_STR = 'Payment'

# возможные статусы операций: активный/неактивный
REG_OP_STATUS_ACTIVE = True
REG_OP_STATUS_INACTIVE = False

# regular operation fields keys
REG_OP_KEYS = [
    'name',
    'reg_op_type',
    'payment_amount',
    'period',
    'notification_period',
    'start_date',
    'status',
]