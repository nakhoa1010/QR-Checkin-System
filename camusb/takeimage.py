import cv2
import time
import dlib
from imutils import face_utils
import pyttsx3
import os
import shutil
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Faster but less accurate
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

check = 0
done = 0
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 100)  # Set the speech rate

def capture(image_name):
    global check, done  # Declare check and done as global variables

    cap = cv2.VideoCapture(0)  # 0 for default webcam
    

    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            engine.say("Xin vui lòng nhìn vào camera")
            engine.runAndWait()
        else:
            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                if (len(shape[36:48]) >= 6) & (len(shape[48:68]) >= 20):  # Số lượng điểm đánh dấu mắt ít nhất là 6
                    check = 1
                else:
                    engine.say("Xin vui lòng nhìn vào camera")
                    engine.runAndWait()

        cv2.imshow('frame', frame)
        
        if check == 1:
            save_path = "facepath\\" + image_name
            cv2.imwrite(save_path, frame)
            done = 1
            # path2 = "\\\\192.168.1.26\\shared\\" + image_name
            # shutil.copy2(save_path,path2)
            break
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return save_path
# if __name__ == "__main__":
#     print('save to: ' + capture('ID001.jpg'))
