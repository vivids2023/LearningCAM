import cv2  # OpenCV(비디오관련) 라이브러리를 가져옵니다.
import os  # os(파일 및 디렉토리관련) 모듈을 가져옵니다.
import tkinter as tk  # GUI를 만들기 위한 tkinter 모듈을 가져옵니다.
from tkinter import filedialog  # 파일 대화상자를 사용하기 위해 filedialog를 가져옵니다.
from PIL import Image, ImageTk  # 이미지 처리를 위한 PIL 라이브러리의 Image 모듈을 가져옵니다.

class CameraApp:
    def __init__(self, window):
        # GUI 창을 초기화합니다.
        self.window = window
        self.window.geometry("640x700")  # 창 크기를 설정합니다.
        self.window.title("Image_Collection")  # 창 제목을 설정합니다.

        # 비디오 캡처 객체를 초기화합니다.
        self.vid = cv2.VideoCapture(0)

        # 캔버스를 생성하고 비디오 프레임을 표시할 크기를 설정합니다.
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 녹화 상태를 나타내는 변수를 초기화합니다.
        self.recording = False

        # 이미지를 저장할 디렉토리 경로를 저장할 변수를 초기화합니다.
        self.directory = None

        # 비디오 녹화를 위한 비디오 라이터 객체를 초기화합니다.
        self.video_writer = None

        # 비디오 프레임을 저장할 변수를 초기화합니다.
        _, self.frame = self.vid.read()

        # 캔버스를 화면에 배치합니다.
        self.canvas.place(x=0, y=0)

        # 상태 텍스트 박스를 생성하고 화면에 배치합니다.
        self.status = tk.Label(window, text="STATUS", width=8)
        self.status.place(x=0, y=500)

        # 상태 엔트리 박스를 생성하고 화면에 배치합니다.
        self.status1 = tk.Entry(window, width=75)
        self.status1.place(x=73, y=500)

        # 디렉토리 레이블을 생성하고 화면에 배치합니다.
        self.entry_directory = tk.Label(window, text="DIRECTORY", width=8)
        self.entry_directory.place(x=5, y=530)

        # 디렉토리 엔트리 박스를 생성하고 화면에 배치합니다.
        self.entry_directory1 = tk.Entry(window, width=75)
        self.entry_directory1.place(x=73, y=530)

        # 디렉토리 선택 버튼을 생성하고 화면에 배치합니다.
        self.btn_select_dir = tk.Button(window, text="Select Directory", width=30, command=self.select_directory)
        self.btn_select_dir.place(x=190, y=560)

        # AVI 파일을 이미지로 변환하는 버튼을 생성하고 화면에 배치합니다.
        self.avi_to_image_bu = tk.Button(window, text="AVI -> Image", width=30, command=self.avi_to_image)
        self.avi_to_image_bu.place(x=190, y=600)

        # 이미지 캡처 버튼을 생성하고 화면에 배치합니다.
        self.btn_capture = tk.Button(window, text="Image Capture", width=25, command=self.image_capture)
        self.btn_capture.place(x=40, y=650)

        # 녹화 시작/중지 버튼을 생성하고 화면에 배치합니다.
        self.start_stop_button = tk.Button(window, text="Start Recording", width=25, command=self.toggle_recording)
        self.start_stop_button.place(x=420, y=650)

        # 프레임 업데이트 메서드를 호출하여 비디오 프레임을 업데이트합니다.
        self.update()

        # 창 닫기 이벤트를 처리합니다.
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  

    def select_directory(self):   # 디렉토리 선택 함수 
        # 사용자가 디렉토리를 선택하면 해당 경로를 저장하고 표시합니다.
        self.status1.delete(0, tk.END) 
        self.status1.insert(0, "Select Directory")
        self.directory = filedialog.askdirectory()
        self.entry_directory1.delete(0, tk.END)
        self.entry_directory1.insert(tk.END, self.directory)
        print(f"Selected directory: {self.directory}") 
        self.status1.delete(0, tk.END) 
        self.status1.insert(0, "Selected Directory")

    def toggle_recording(self):   # 토글버튼 동영상녹화 함수
        # 디렉토리가 선택되었는지 확인하고 녹화를 시작 또는 중지합니다.
        if self.directory:
            serial_number = self.get_next_serial_number_vid()
            filename = f"REC_{self.directory.split('/')[-1]}_{serial_number:04d}.avi"
            filename1 = None
            if serial_number is not None:
                if not self.recording:
                    if self.directory:
                        self.recording = True
                        self.start_stop_button.config(text="Stop Recording")
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        self.video_writer = cv2.VideoWriter(os.path.join(self.directory, filename), fourcc, 20.0, (640, 480))
                        print(f"{os.path.join(self.directory, filename)}....Recording")
                        self.status1.delete(0, tk.END)
                        self.status1.insert(0, "Recording")
                else:
                    self.recording = False
                    self.start_stop_button.config(text="Start Recording")
                    if self.video_writer:
                       self.video_writer.release()
                       print("Record Done")
                       self.status1.delete(0, tk.END)
                       self.status1.insert(0, "Record Done")
            else:
                print("Cannot capture Video. Directory may not exist")
                self.status1.delete(0, tk.END)
                self.status1.insert(0, "Cannot capture Video. Directory may not exist")
        else:
            print("Please select a directory first")
            self.status1.delete(0, tk.END)
            self.status1.insert(0, "Please select a directory first")

    def image_capture(self):   # 이미지 캡쳐 함수
        # 디렉토리가 선택되었는지 확인하고 이미지를 캡처하고 저장합니다.
        self.status1.delete(0, tk.END) 
        self.status1.insert(0, "Image Capturing")
        if self.directory:
            _, self.frame = self.vid.read()
            serial_number = self.get_next_serial_number()
            if serial_number is not None:
                filename = os.path.join(self.directory, f"{self.directory.split('/')[-1]}_{serial_number:04d}.png")
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                cv2.imwrite(filename, frame_bgr)
                print(f"Image captured and saved as {filename}")
                self.status1.delete(0, tk.END) 
                self.status1.insert(0, f"Image captured and saved as {filename}")
            else:
                print("Cannot capture image. Directory may not exist")
                self.status1.delete(0, tk.END) 
                self.status1.insert(0, "Cannot capture image. Directory may not exist")
        else:
            print("Please select a directory first")
            self.status1.delete(0, tk.END) 
            self.status1.insert(0, "Please select a directory first")

    def get_next_serial_number(self):      # 이미지파일 다음 일련번호 얻는 함수
        # 디렉토리에서 이미지 파일의 다음 일련번호를 가져옵니다.
        if os.path.exists(self.directory):
            files = os.listdir(self.directory)
            image_files = [file for file in files if file.endswith(".png")]
            if image_files:
                serial_numbers = [int(file.split('_')[-1].split('.')[0]) for file in image_files if file.startswith(f"{self.directory.split('/')[-1]}_")]
                if serial_numbers:
                    return max(serial_numbers) + 1
                else:
                    return 1
            else:
                return 1
        else:
            return None

    def get_next_serial_number_vid(self):     # 동영상파일 다음 일련번호 얻는 함수
        # 디렉토리에서 동영상 파일의 다음 일련번호를 가져옵니다.
        if os.path.exists(self.directory):
            files = os.listdir(self.directory)
            avi_files = [file for file in files if file.endswith(".avi")]
            if avi_files:
                serial_numbers = [int(file.split('_')[-1].split('.')[0]) for file in avi_files if file.startswith(f"{self.directory.split('/')[-1]}_")]
                if serial_numbers:
                    return max(serial_numbers) + 1
                else:
                    return 1
            else:
                return 1
        else:
            return None

    def update(self):    # canvas에 프리뷰화면 표출 함수
        # 비디오 프레임을 업데이트하고 캔버스에 표시합니다.
        ret, frame = self.vid.read()
        if self.recording and self.video_writer:
            self.video_writer.write(frame)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)

            self.canvas.delete("all")

            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

            self.canvas.image = img

        self.window.after(10, self.update)

    def extract_frames(self, video_path, output_folder, dirpathname):
        # 동영상 파일에서 프레임을 추출하여 이미지로 저장합니다.
        cap = cv2.VideoCapture(video_path)
        os.makedirs(dirpathname+ "/" +output_folder, exist_ok=True)
        makeframe = (dirpathname+ "/" +output_folder)
        print(makeframe)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_name = f"frame_{frame_count}.png"
            frame_path = os.path.join(makeframe, frame_name)
            cv2.imwrite(frame_path, frame)
            frame_count += 1
        cap.release()
    
    def avi_to_image(self):
        # 사용자로부터 AVI 파일을 선택하고 프레임을 추출하여 이미지로 저장합니다.
        self.status1.delete(0, tk.END) 
        self.status1.insert(0, f"select video file...")
        video_path = filedialog.askopenfilename(title="Select video file", filetypes=[("Video files", "*.mp4;*.avi")])
        if not video_path:
            print("No video file selected")
            self.status1.delete(0, tk.END) 
            self.status1.insert(0, "No video file selected")
            return
        dirpathname = os.path.dirname(video_path)
        output_folder = os.path.splitext(os.path.basename(video_path))[0]
        self.extract_frames(video_path, output_folder, dirpathname)
        print(f"Frames extracted and saved in '{output_folder}' folder.")
        self.status1.delete(0, tk.END) 
        self.status1.insert(0, f"saved file in {dirpathname}/{output_folder} folder")

    def on_closing(self):   # 프로그램 종료시 리소스 릴리즈 함수
        # 프로그램을 종료할 때 비디오 캡처 객체를 해제합니다.
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

# if __name__ == "__main__":
root = tk.Tk()
recorder = CameraApp(root)
root.mainloop()