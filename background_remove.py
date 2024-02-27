from PIL import Image
from rembg import remove
import os
 
for root, dirs, files in os.walk('./'): # os.walk는 특정 디렉토리 아래의 모든 디렉토리와 파일의 목록을 얻어 올 수 있도록 
                                        # root는 어떤 디렉토리인지, dirs는 root 아래의 디렉토리 목록, 그리고 files는 root 아래의 파일 목록이다
    for idx, file in enumerate(files):  # enumerate() 함수는 인자로 넘어온 목록을 기준으로 인덱스와 원소를 차례대로 접근하게 해주는 함수입니다.
        fname, ext = os.path.splitext(file) # os(라이브러리).path(모듈).splitext(함수)(filename) --> 확장자만 따로 분류한다
        if ext in ['.jpg','.png','.gif']:
            input = Image.open(file) # load image 
            output = remove(input) # remove background
            output.save('Img' + str(idx) + '.png') # save image






