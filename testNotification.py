import unittest

import notification


# ----------------- NOTIFICATION TESTING ----------------
class TestsNotification(unittest.TestCase):

    def setUp(self):
        self.notification = notification.Notification('str1', 'str2')

    def test_notification_init(self):
        self.assertEqual(self.notification.notification_type, 'str2')
        self.assertEqual(self.notification.notification_format, 'str1')
        self.assertEqual(self.notification.get_notification(), 'str2: str1')

        with self.assertRaises(TypeError):
            notification.Notification(1, 'string')

        with self.assertRaises(TypeError):
            notification.Notification('string', 1)

    def test_notification_update(self):
        self.notification.update()
        self.assertEqual(self.notification.notification_type, 'str2')
        self.assertEqual(self.notification.notification_format, 'str1')
        self.assertEqual(self.notification.get_notification(), 'str2: str1')
        self.notification.update(notification_type='qwe')
        self.assertEqual(self.notification.notification_type, 'qwe')
        self.assertEqual(self.notification.notification_format, 'str1')
        self.assertEqual(self.notification.get_notification(), 'qwe: str1')
        self.notification.update(notification_format='123')
        self.assertEqual(self.notification.notification_type, 'qwe')
        self.assertEqual(self.notification.notification_format, '123')
        self.assertEqual(self.notification.get_notification(), 'qwe: 123')
        self.notification.update(notification_type='asd', notification_format='456 {key1}')
        self.assertEqual(self.notification.notification_type, 'asd')
        self.assertEqual(self.notification.notification_format, '456 {key1}')
        self.assertEqual(self.notification.get_notification({'key1': 'www'}), 'asd: 456 www')
        self.assertEqual(self.notification.get_notification({'key1': 'www', 2: 'jjj'}), 'asd: 456 www')
        self.assertEqual(self.notification.get_notification(), '')

        with self.assertRaises(TypeError):
            self.notification.update(notification_type=1)
        with self.assertRaises(TypeError):
            self.notification.update(notification_format=1)
        with self.assertRaises(TypeError):
            self.notification.update(notification_type='asd', notification_format=123)

        with self.assertRaises(KeyError):
            self.assertEqual(self.notification.get_notification({'key2': 'www'}), 'asd: 456 www')
        with self.assertRaises(KeyError):
            self.assertEqual(self.notification.get_notification({1: 'www'}), 'asd: 456 www')


def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(TestsNotification('test_notification_init'))
    _suite.addTest(TestsNotification('test_notification_update'))
    return _suite




