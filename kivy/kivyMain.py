from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class StartScreen(Screen):
    pass


class RegularOperationsScreen(Screen):
    pass


class RegularOperationTypesScreen(Screen):
    pass


class StatisticsScreen(Screen):
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