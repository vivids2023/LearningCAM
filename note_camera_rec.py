import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Use the default camera (usually the built-in camera)
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_start_stop = tk.Button(window, text="Start Recording", width=15, command=self.toggle_recording)
        self.btn_start_stop.pack(pady=10)

        self.btn_select_dir = tk.Button(window, text="Select Directory", width=15, command=self.select_directory)
        self.btn_select_dir.pack(pady=10)

        self.entry_directory = tk.Entry(window, width=40)
        self.entry_directory.insert(0, "recorded_videos")  # Default directory name
        self.entry_directory.pack(pady=10)

        self.is_recording = False
        self.out = None

        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.update()
        self.window.mainloop()

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        directory = self.entry_directory.get()
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = f"{directory}/recorded_video.avi"

        # VideoWriter_fourcc: FourCC is a 4-byte code used to specify the video codec
        # XVID is a commonly used codec, but you can change it based on your preference
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_size = (int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.out = cv2.VideoWriter(file_name, fourcc, 20.0, frame_size)

        print(f"Recording started: {file_name}")
        self.btn_start_stop.config(text="Stop Recording")
        self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            self.out.release()
            print("Recording stopped")
            self.btn_start_stop.config(text="Start Recording")
            self.is_recording = False

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_directory.delete(0, tk.END)
            self.entry_directory.insert(0, directory)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the RGB frame to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
            if self.is_recording:
                # Write the RGB frame to the video file
                self.out.write(frame_rgb)

        self.window.after(10, self.update)

    def exit_app(self):
        self.stop_recording()
        self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera App")