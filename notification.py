

class Notification:  # 11 tests
    def __init__(self, notification_format, notification_type):  # 3 branch
        # проверка инициализирующих аргументов
        if not notification_format or not isinstance(notification_format, str):
            raise TypeError('Expected string as notification format')

        if not notification_type or not isinstance(notification_type, str):
            raise TypeError('Expected string as notification type')

        self.notification_format = notification_format
        self.notification_type = notification_type

    def update(self, notification_format=None, notification_type=None):  # 5 branch
        # проверка инициализирующих аргументов
        if notification_format and not isinstance(notification_format, str):
            raise TypeError('Expected string as notification format')

        if notification_type and not isinstance(notification_type, str):
            raise TypeError('Expected string as notification type')

        if notification_format:
            self.notification_format = notification_format

        if notification_type:
            self.notification_type = notification_type

    def get_notification(self, notification_fields=None):  # 3 branch
        msg = self.notification_type + ': '
        try:
            msg += self.notification_format.format_map(notification_fields)
        except TypeError or KeyError:
            msg = ''

        return msg

