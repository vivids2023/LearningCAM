import cv2  # OpenCV(비디오관련) 라이브러리를 가져옵니다.
import os  # os(파일 및 디렉토리관련) 모듈을 가져옵니다.
import tkinter as tk  # GUI를 만들기 위한 tkinter 모듈을 가져옵니다.
from tkinter import filedialog  # 파일 대화상자를 사용하기 위해 filedialog를 가져옵니다.
from PIL import Image, ImageTk  # 이미지 처리를 위한 PIL 라이브러리의 Image 모듈을 가져옵니다.

class CameraApp:
    def __init__(self, preview):
        # GUI 창을 초기화합니다.
        self.window = preview
        self.window.geometry("640x700")  # 창 크기를 설정합니다.
        self.window.title("Image_Collection")  # 창 제목을 설정합니다.

        # 비디오 캡처 객체를 초기화합니다.
        self.vid = cv2.VideoCapture(0)
                
        # 캔버스를 생성하고 비디오 프레임을 표시할 크기를 설정합니다.
        self.canvas = tk.Canvas(preview, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 캔버스를 화면에 배치합니다.
        self.canvas.place(x=0, y=0)        

        # 녹화 상태를 나타내는 변수를 초기화합니다.
        self.recording = False

        # 비디오 녹화를 위한 비디오 라이터 객체를 초기화합니다.
        self.video_writer = None

        # 프레임 업데이트 메서드를 호출하여 비디오 프레임을 업데이트합니다.
        self.update()


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


root = tk.Tk()
learningCAM = CameraApp(root)
root.mainloop()        