import datetime
from datetime import date, timedelta
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, AliasProperty
import sys
sys.path.append("..")
from classes.businessEntity import BusinessEntity

API = BusinessEntity()


class StartScreen(Screen):
    balance = 0

    def on_enter(self):
        Clock.schedule_once(self.initting)

    def initting(self, dt):
        self.get_balance()

    def get_balance(self):
        self.balance = API.get_balance()
        print('startscreen: balance %d' % self.balance)
        return str(self.balance)




class BalanceScreen(Screen):
    balance = NumericProperty(0)

    def on_enter(self):
        Clock.schedule_once(self.initting)

    def initting(self, dt):
        self.get_balance()

    def change_balance(self, new_balance):
        self.balance = int(new_balance)
        print('changing balance: %d' % self.balance)
        API.change_deposit_balance(self.balance)

    def get_balance(self):
        self.balance = API.get_balance()
        print('balance: get_balance %d' % self.balance)
        return str(self.balance)

    balstr = AliasProperty(get_balance, None, bind=['balance'])

class RegularOperationsScreen(Screen):

    pass


class RegularOperationTypesScreen(Screen):
    pass


class StatisticsScreen(Screen):
    API.get_operation_types()
    reg_op_types_statistics = [x.name for x in API.regularOperationTypes]
    total_income = 0
    total_spend = 0 
    total = 0
    def get_statistics(self, reg_op_type_stat, start_date, end_date):
        final_op_stat = None
        final_start_date = None
        final_end_date = None 
        
        final_start_date = start_date if isinstance(start_date, str) else None
        final_end_date = start_date if isinstance(end_date, str) else None
        for op_type in API.regularOperationTypes:
            if op_type.name == reg_op_type_stat:
                final_op_stat = op_type
                break
        if final_start_date and final_end_date and final_op_stat:
            try:
                res = API.form_statistics_by_period(reg_op_type_stat, start_date, end_date)
                print(res)
            except:
                print("Wrong")
            self.total_income = res["total_income"]
            self.total_spend = res["total_spend"]
            self.total = self.total_income - self.total_spend
            print("self.total_income ", self.total_income)
            print("self.total_income ", self.total_income)
            print("self.total_income ", self.total_income)




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
