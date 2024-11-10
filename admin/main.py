import network  # Make sure this is pointing to your network module
import threading
from kivy.uix.accordion import ObjectProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock


class WindowManager(MDScreenManager):
    pass

class MainScreen():
    pass

class SecondScreen():
    pass
class ServerScreen(MDScreen):
    threads = []
    stop_event = threading.Event()
    def start(self):
        """Start the server and transition to the second screen."""
        # Start the server in a separate thread
        thread = threading.Thread(target=self._start_server)
        thread.start()
        self.threads.append(thread)

    def _start_server(self):
        """Handle the server startup in a separate thread."""
        try:
            network.start_server()
        except Exception as e:
            print(f"Error while starting server: {e}")

    def close(self):
        self._stop_server
        self.stop_event.set()

        close_thread = threading.Thread(target=self._stop_server)
        close_thread.start()
        self.threads.append(close_thread)

        for thread in self.threads:
            thread.join()

    def _stop_server(self):
        """Handle the server shutdown in a separate thread."""
        try:
            network.nuke_server()  # Stop the server in the background
        except Exception as e:
            print(f"Error while stopping server: {e}")



class SecondScreen(MDScreen):
    pass

Window.size = (360, 640)


class MyApp(MDApp):
    def build(self):
        window = Builder.load_file('app.kv')
        self.title = "DeckTech"
        return window


if __name__ == "__main__":
    MyApp().run()
