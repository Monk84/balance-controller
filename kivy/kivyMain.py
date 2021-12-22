import datetime
from datetime import date, timedelta
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from classes.businessEntity import BusinessEntity

API = BusinessEntity()


class StartScreen(Screen):
    pass


class RegularOperationsScreen(Screen):

    pass


class RegularOperationTypesScreen(Screen):
    pass


class StatisticsScreen(Screen):
    pass


class SecretMenuScreen(Screen):
    pass


class AddRegularOperationScreen(Screen):
    reg_op_types = []

    def on_enter(self):
        # getting reg op types
        API.get_operation_types()
        self.reg_op_types = [x.name for x in API.regularOperationTypes]
        self.ids["reg_op_type"].values = self.reg_op_types

    # get notification periods
    def add_reg_op(self, reg_op_name, reg_op_type, reg_op_sum, reg_op_period, reg_op_notification):
        periods = {
            "Каждый день": 1,
            "Каждую неделю": 7,
            "Каждый месяц": 30,
            "Каждый год": 365
        }
        notification_periods = {
            "За месяц": 30,
            "За неделю": 7,
            "За день": 1,
            "В тот же день": 0,
            "Через день": -1
        }
        try:
            reg_op_sum = int(reg_op_sum)
            reg_op_period = periods[reg_op_period]
            reg_op_notification = notification_periods[reg_op_notification]
            for op_type in API.regularOperationTypes:
                if op_type.name == reg_op_type:
                    reg_op_type = op_type
                    break
        except:
            pass
        try:
            if reg_op_name != '' and reg_op_type != "Выберите тип регулярной операции" and isinstance(reg_op_sum, int) \
                    and isinstance(reg_op_period, int) and isinstance(reg_op_notification, int):
                API.add_regular_operation(reg_op_name,
                                          reg_op_type,
                                          reg_op_sum,
                                          timedelta(reg_op_period),
                                          timedelta(reg_op_notification),
                                          datetime.date.today())
                self.manager.current = "main"

        except:
            pass

    pass


class ScreenManager(ScreenManager):
    # Описывает переходы между экранами
    pass


# Вся конфигурация UI в файле
kv = Builder.load_file("config.kv")


class MainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    app = MainApp()
    app.run()
