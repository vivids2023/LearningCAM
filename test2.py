import cv2  # OpenCV(비디오관련) 라이브러리를 가져옵니다.
# import os  # os(파일 및 디렉토리관련) 모듈을 가져옵니다.
import tkinter as tk  # GUI를 만들기 위한 tkinter 모듈을 가져옵니다.
# from tkinter import filedialog  # 파일 대화상자를 사용하기 위해 filedialog를 가져옵니다.
# from PIL import Image, ImageTk  # 이미지 처리를 위한 PIL 라이브러리의 Image 모듈을 가져옵니다.

class CameraApp:
    def __init__(self, window):
        # GUI 창을 초기화합니다.
        self.window = window
        self.window.geometry("640x700")  # 창 크기를 설정합니다.
        self.window.title("Image_Collection")  # 창 제목을 설정합니다.

        # # # 비디오 캡처 객체를 초기화합니다.
        # self.vid = cv2.VideoCapture(0)

        # # 캔버스를 생성하고 비디오 프레임을 표시할 크기를 설정합니다.
        # self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 캔버스를 화면에 배치합니다.
        #self.canvas.place(x=0, y=0)

        # # 녹화 상태를 나타내는 변수를 초기화합니다.
        # self.recording = False

        # # 이미지를 저장할 디렉토리 경로를 저장할 변수를 초기화합니다.
        # self.directory = None

        # # 비디오 녹화를 위한 비디오 라이터 객체를 초기화합니다.
        # self.video_writer = None

        # # 비디오 프레임을 저장할 변수를 초기화합니다.
        # _, self.frame = self.vid.read()

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
        self.btn_select_dir = tk.Button(window, text="Select Directory", width=30)
        self.btn_select_dir.place(x=190, y=560)

        # AVI 파일을 이미지로 변환하는 버튼을 생성하고 화면에 배치합니다.
        self.avi_to_image_bu = tk.Button(window, text="AVI -> Image", width=30)
        self.avi_to_image_bu.place(x=190, y=600)

        # 이미지 캡처 버튼을 생성하고 화면에 배치합니다.
        self.btn_capture = tk.Button(window, text="Image Capture", width=25)
        self.btn_capture.place(x=40, y=650)

        # 녹화 시작/중지 버튼을 생성하고 화면에 배치합니다.
        self.start_stop_button = tk.Button(window, text="Start Recording", width=25)
        self.start_stop_button.place(x=420, y=650)

        # 프레임 업데이트 메서드를 호출하여 비디오 프레임을 업데이트합니다.
        # self.update()


root = tk.Tk()
recorder111 = CameraApp(root)
root.mainloop()        