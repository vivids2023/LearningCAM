from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.directory_input = TextInput(text='Enter Directory')
        self.layout.add_widget(self.directory_input)

        self.capture_button = Button(text='Capture')
        self.capture_button.bind(on_press=self.capture)
        self.layout.add_widget(self.capture_button)

        return self.layout

    def capture(self, instance):
        directory = self.directory_input.text.strip()
        if not os.path.exists(directory):
            os.makedirs(directory)

        files_in_directory = os.listdir(directory)
        file_count = len(files_in_directory)

        filename = f"{directory}/image_{file_count:04d}.png"
        print(f"Image saved: {filename}")

if __name__ == '__main__':
    CameraApp().run()