from kivy.uix.accordion import ObjectProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from data import Person
from data import File_Handler
import network
import time


Window.size=(360,640)


class WindowManager(MDScreenManager):
    pass

class MainScreen(MDScreen):
    def check_file_exists(self):

        if File_Handler().check_file():
            self.manager.current = "profile"

        else:
            self.manager.current = "second"

        self.manager.transition.direction = 'left'

class SecondScreen(MDScreen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    reg_no = ObjectProperty(None)
    department = ObjectProperty(None)
    user_password = ObjectProperty(None)



    def next(self):
        data = File_Handler()
        check_answers = {
        "first_name":self.first_name.text,
        "last_name":self.last_name.text,
        "reg_no":self.reg_no.text,
        "department": self.department.text,
        "user_password":self.user_password.text
        }

        if data.check_file():
            self.manager.current = "profile"
            self.manager.transition.direction = 'left'

        else:
            Passable = True
            for key,value in check_answers.items():
                if not value:
                    Passable = False
                    break

            if Passable == True:
                person = Person(first_name=self.first_name.text,last_name=self.last_name.text,reg_no=self.reg_no.text,department=self.department.text,password=self.user_password.text)

                data.write_file(person.person_data())
                self.manager.current = "profile"
                self.manager.transition.direction = 'left'
            else:
                self.dialog = MDDialog(
                title="Failed",
                text="Please Enter Data into all the fields correctly",
                size_hint=(0.6, 0.6),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                auto_dismiss=True,
                background_color= (0,0,0,0.5),
                padding= 20
                )
                self.dialog.open()  # Open the dialog








class ProfileScreen(MDScreen):
    pass

class ServerList(MDScreen):
    def load_servers(self):
        network.listen_to_all_servers(network.PORT)
        print(network.servers_found)

        print(network.servers_found)
        time.sleep(2)
        print(network.servers_found)
        time.sleep(2)
        print(network.servers_found)
        time.sleep(2)
        print(network.servers_found)





class MyApp(MDApp):
    def build(self):

        window = Builder.load_file('app.kv')
        self.title ="DeckTech"
        return window


if __name__ == "__main__":
    MyApp().run()
