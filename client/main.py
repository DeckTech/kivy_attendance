from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size=(360,640)


class WindowManager(MDScreenManager):
    pass

class MainScreen(MDScreen):
    pass

class SecondScreen(MDScreen):
    pass

class ProfileScreen(MDScreen):
    pass





class MyApp(MDApp):
    def build(self):

        window = Builder.load_file('app.kv')
        self.title ="DeckTech"
        return window


if __name__ == "__main__":
    MyApp().run()
