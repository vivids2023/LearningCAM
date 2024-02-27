import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.geometry("640x650")
        self.window.title("Image_Collection")

        self.vid = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #self.directory = ""
        #self.capture = cv2.VideoCapture(0)
        #_, self.frame = self.capture.read()
        #self.capture = cv2.VideoCapture(0)
        _, self.frame = self.vid.read()
        self.show_frame()
        
        self.canvas.place(x=0, y=0)

        self.entry_directory = tk.Entry(window, width=80)
        self.entry_directory.insert(0, "Selected Directory : ")  # Default directory name
        self.entry_directory.place(x=20, y=500)

        self.btn_select_dir = tk.Button(window, text="Select Directory", width=40, command=self.select_directory)
        self.btn_select_dir.place(x=170, y=540)

        self.btn_capture = tk.Button(window, text="Image Capture", width=25, command=self.image_capture)
        self.btn_capture.place(x=40, y=590)

        self.btn_video_capture = tk.Button(window, text="Video Capture", width=25, command=self.video_capture)
        self.btn_video_capture.place(x=420, y=590)

        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def select_directory(self):
        # 디렉토리 선택 함수
        self.directory = filedialog.askdirectory()
        #self.entry_directory.delete(0, tk.END)
        #self.entry_directory.config(text=f"Selected Directory: {self.directory}")
        self.entry_directory.insert(tk.END, self.directory)
        print(f"Selected directory: {self.directory}")

    def image_capture(self):
        # Image capture function
        if self.directory:
            serial_number = self.get_next_serial_number()
            if serial_number is not None:
                filename = os.path.join(self.directory, f"{self.directory.split('/')[-1]}_{serial_number:04d}.jpg")
            
            # Convert frame to RGB before saving
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            # Save the image in RGB format
                # cv2.imwrite(filename, frame_rgb)
                cv2.imwrite(filename, frame_bgr)
            
                print(f"Image captured and saved as {filename}")
            else:
                print("Cannot capture image. Directory may not exist.")
        else:
            print("Please select a directory first.")

    # def video_capture(self):
    #     ret, frame = self.vid.read()
    #     if ret:
    #         directory = self.entry_directory.get()
    #         if not os.path.exists(directory):
    #             os.makedirs(directory)

    #         file_name = f"{directory}/captured_picture_{self.serial_number:04d}.jpg"
    #         cv2.imwrite(file_name, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #         print(f"Picture captured successfully: {file_name}")
    #         self.serial_number += 1

    def video_capture(self):
        # Image capture function
        if self.directory:
            serial_number = self.get_next_serial_number_video()
            if serial_number is not None:
                filename = os.path.join(self.directory, f"{self.directory.split('/')[-1]}_{serial_number:04d}.avi")
            
            # Convert frame to RGB before saving
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            # Save the image in RGB format
                # cv2.imwrite(filename, frame_rgb)
                cv2.VideoWriter(filename, frame_bgr)
            
                print(f"Image captured and saved as {filename}")
            else:
                print("Cannot capture image. Directory may not exist.")
        else:
            print("Please select a directory first.")

    def get_next_serial_number(self):
        # 다음 일련번호 얻는 함수
        if os.path.exists(self.directory):
            files = os.listdir(self.directory)
            if files:
                serial_numbers = [int(file.split('_')[-1].split('.')[0]) for file in files if file.startswith(f"{self.directory.split('/')[-1]}_")]
                if serial_numbers:
                    return max(serial_numbers) + 1
                else:
                    return 1
            else:
                return 1
        else:
            return None

    def get_next_serial_number_vid(self):
        # 다음 일련번호 얻는 함수
        if os.path.exists(self.directory):
            files = os.listdir(self.directory)
            avi_files = [file for file in files if file.endswith(".avi")]
            if avi_files:
                serial_numbers = [int(file.split('_')[-1].split('.')[0]) for file in files if file.startswith(f"{self.directory.split('/')[-1]}_")]
                if serial_numbers:
                    return max(serial_numbers) + 1
                else:
                    return 1
            else:
                return 1
        else:
            return None
        
    def show_frame(self):
        # 웹캠 프레임을 보여주는 함수 
        # python에서 BGR로 이미지를 저장하는 이유?  https://blog.xcoda.net/102
        if hasattr(self, 'preview_label'):
            self.preview_label.destroy()

        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = ImageTk.PhotoImage(img)

        #self.preview_label = tk.Label(self.root, image=img)
        #self.preview_label.image = img
        #self.preview_label.pack()

        #self.root.after(10, self.update_frame)
        


        
# if __name__ == "__main__":
root = tk.Tk()
app = CameraApp(root, "Camera App")
root.mainloop()