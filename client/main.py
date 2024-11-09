from kivy.uix.accordion import ObjectProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from data import Person
from data import File_Handler

Window.size=(360,640)


class WindowManager(MDScreenManager):
    pass

class MainScreen(MDScreen):
    pass

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
            print("File Present")
            pass
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
