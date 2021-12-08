import classes.const as const


# описание класса типа регулярной операции
class RegularOperationType:  # 8 tests
    def __init__(self, name, op_type):  # 3 branch
        """
        regular operation type initialization
        :param name: str
        :param op_type: bool
        """
        # проверка инициализирующих аргументов
        if name is None or not isinstance(name, str):
            raise TypeError('Expected string as regular operation type name')

        if op_type is None or not isinstance(op_type, bool):
            raise TypeError('Expected boolean as operation type')

        self.name = name
        self.type = const.OP_TYPE_INCOME if op_type else const.OP_TYPE_EXPENSE
        self.status = const.REG_OP_STATUS_ACTIVE

    def delete(self):  # 1 branch
        """
        Deleting regular operation type means inactivating it.
        :return: None
        """
        self.status = const.REG_OP_STATUS_INACTIVE

    def add(self):  # 1 branch
        """
        Adding regular operation type means activating it.
        :return: None
        """
        self.status = const.REG_OP_STATUS_ACTIVE

    def get_op_type(self):  # 1 branch
        """
        get operation type
        :return: int
        """
        return self.type

    def get_name(self):  # 1 branch
        """
        get regular operation type name
        :return: str
        """
        return self.name

    def get_status(self):  # 1 branch
        """
        get regular operation type status
        :return: bool
        """
        return self.status

    def __repr__(self):
        return str({'name': self.name, 'op_type': self.type, 'status': self.status})

