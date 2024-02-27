import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title("Image_Collection")

        self.video_source = 0  # Use the default camera (usually the built-in camera)
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_capture = tk.Button(window, text="Capture", width=10, command=self.capture)
        self.btn_capture.pack(padx=10, pady=10)

        self.btn_select_dir = tk.Button(window, text="Select Directory", width=15, command=self.select_directory)
        self.btn_select_dir.pack(pady=10)

        self.entry_directory = tk.Entry(window, width=40)
        self.entry_directory.insert(0, "captured_pictures")  # Default directory name
        self.entry_directory.pack(pady=10)

        self.serial_number = 1

        self.update()
        self.window.mainloop()

    def capture(self):
        ret, frame = self.vid.read()
        if ret:
            directory = self.entry_directory.get()
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = f"{directory}/captured_picture_{self.serial_number:04d}.jpg"
            cv2.imwrite(file_name, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print(f"Picture captured successfully: {file_name}")
            self.serial_number += 1

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_directory.delete(0, tk.END)
            self.entry_directory.insert(0, directory)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def exit_app(self):
        self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera App")