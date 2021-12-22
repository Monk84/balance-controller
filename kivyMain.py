import datetime
from datetime import date, timedelta
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from classes.businessEntity import BusinessEntity
from classes.const import notification_periods, notification_periods_inverse, periods, periods_inverse

API = BusinessEntity()


class StartScreen(Screen):
    pass


class RegularOperationsScreen(Screen):
    reg_ops = []
    index_to_id = {}

    def on_enter(self):
        self.reg_ops = []
        self.index_to_id = {}
        self.ids["reg_ops_list"].clear_widgets()
        active_reg_ops = API.show_operations()
        for i in range(len(active_reg_ops)):
            op = active_reg_ops[i]
            self.reg_ops.append(op[1]['operation'])
            self.index_to_id[str(i+1)] = op[1]['id']
            btn = Button(text=str(i+1)+"."+op[1]['operation'].name)
            btn.bind(on_press=self.move_to_reg_op_type)
            self.ids["reg_ops_list"].add_widget(btn)
        return

    def move_to_reg_op_type(self, instance):
        self.manager.current = "reg_op_change"
        reg_op_index = instance.text[:instance.text.find(".")]
        reg_op_change = self.manager.get_screen("reg_op_change")
        reg_op_change.reg_op_id = self.index_to_id[reg_op_index]
        reg_op_change.reg_op = self.reg_ops[int(reg_op_index)-1]
    pass


class ChangeRegularOperationScreen(Screen):
    reg_op_id = 0
    reg_op = None
    reg_op_types = []

    def on_enter(self):
        API.get_operation_types()
        self.reg_op_types = [x.name for x in API.regularOperationTypes]
        self.ids["reg_op_type"].values = self.reg_op_types
        # set reg_op data
        self.ids["reg_op_name"].text = self.reg_op.name
        self.ids["reg_op_type"].text = self.reg_op.reg_op_type.name
        self.ids["reg_op_sum"].text = str(self.reg_op.payment_amount)
        self.ids["reg_op_period"].text = periods_inverse[self.reg_op.period.days]
        self.ids["reg_op_notification"].text = notification_periods_inverse[self.reg_op.notification_period.days]
        return

    def update_reg_op(self, reg_op_name, reg_op_type, reg_op_sum, reg_op_period, reg_op_notification):
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
                API.change_regular_operation(self.reg_op_id,
                                             reg_op_name,
                                             reg_op_type,
                                             reg_op_sum,
                                             timedelta(reg_op_period),
                                             timedelta(reg_op_notification))
                self.manager.current = "main"

        except:
            pass
    pass


class RegularOperationTypesScreen(Screen):
    pass


class StatisticsScreen(Screen):
    API.get_operation_types()
    reg_op_types_statistics = [x.name for x in API.regularOperationTypes]
    total_income = 0
    total_spend = 0 
    total = 0
    
    def on_enter(self):
        self.ids["total_income"].text = str(self.total_income)
        self.ids["total_spend"].text = str(self.total_spend)
        self.ids["total"].text = str(self.total)

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
            except:
                print("Wrong")
            self.total_income = res["total_income"]
            self.total_spend = res["total_spend"]
            self.total = self.total_income - self.total_spend

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
