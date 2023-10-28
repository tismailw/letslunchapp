from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior

class HomeScreen(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class SignupScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

GUI = Builder.load_file("main.kv")
class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        # get the screen manager from the kv file
        screen_manager = self.root.ids['screen_manager'] # root: the main widget in the layout
        screen_manager.transition = NoTransition()  # You can change the direction to "right", "up", "down", etc.
        screen_manager.current = screen_name
        #screen_manager = self.root.ids

MainApp().run()