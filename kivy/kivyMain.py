from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
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
    def get_reg_op_types(self):
        reg_op_types = API.get_operation_types()
        print(reg_op_types, type(reg_op_types), type(reg_op_types[0]))
        for op_type in reg_op_types:
            # Doesn't work properly. Needs to be finished
            new_button = Button(text=op_type['name'], size_hint_y=None, height=44)
            new_button.bind(on_release=lambda new_button: self.root.select(new_button.text))
            self.ids['reg_op_type'].add_widget(new_button)
        print(self.ids['reg_op_type'].container)
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