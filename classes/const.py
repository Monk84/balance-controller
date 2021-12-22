
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
# Возможные настройки периодичности и напоминаний
periods = {
    "Каждый день": 1,
    "Каждую неделю": 7,
    "Каждый месяц": 30,
    "Каждый год": 365
}
periods_inverse = {
    1: "Каждый день",
    7: "Каждую неделю",
    30: "Каждый месяц",
    365: "Каждый год"
}
notification_periods = {
    "За месяц": 30,
    "За неделю": 7,
    "За день": 1,
    "В тот же день": 0,
    "Через день": -1
}
notification_periods_inverse = {
    30: "За месяц",
    7: "За неделю",
    1: "За день",
    0: "В тот же день",
    -1: "Через день"
}