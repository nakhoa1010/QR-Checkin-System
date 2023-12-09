import multiprocessing 
from multiprocessing import Process, Manager
import cv2
import dlib
from imutils import face_utils
import serial
import time
import goi_ham as gh
from picamera2 import Picamera2
detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')



def process1(queue, flag, count, check, string_var):
    
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()
    
    while True:
        frame = picam2.capture_array()
        # framecopy = frame.copy()
        if flag.value == 0:
            cv2.rectangle(frame, (0, 0), (200, 200), (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (0, 0), (200, 200), (0, 255, 0), 2)
        
        cv2.imshow("Frame", frame)
        if count.value >= 20:
            save_path = "facepath/" + str(string_var[0]) + ".jpg"
            cv2.imwrite(save_path, frame)
            gh.update_data(str(string_var[0]), save_path)
            count.value = 0
            check.value = 0
        queue.put(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

def process2(queue, flag, count, check, string_var):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)  # Thiết lập timeout ở đây
    try:
        while True:
            barcode_data = ser.readline().decode().strip()
            if barcode_data:
                print(f'Mã vạch đã đọc được: {barcode_data}')
                check_var = gh.check_available(barcode_data)
                if check_var == None:
                    print("QR khong ton tai trong he thong.")
                else:
                    print("QR ton tai trong he thong.") 
                    check.value = 1
                    gh.check(barcode_data)
                    string_var[:] = [barcode_data]
            while check.value == 1:
                if not queue.empty():
                    frame = queue.get()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                        minNeighbors=5, minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE)

                    if len(rects) == 0:
                        flag.value = 0
                        count.value = 0
                    else:
                        for (x, y, w, h) in rects:
                            rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                            shape = predictor(gray, rect)
                            shape = face_utils.shape_to_np(shape)
                            
                            if (len(shape[36:48]) >= 6) and (len(shape[48:68]) >= 20):
                                flag.value = 1
                                count.value += 1
                            else:
                                flag.value = 0
                                count.value = 0
                    print(count.value)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
    finally:
        ser.close()  # Close the serial connection when done
if __name__ == "__main__":
    with Manager() as manager:
        flag = multiprocessing.Value('i', 0)  
        count = multiprocessing.Value('i', 0)
        check = multiprocessing.Value('i', 0)
        string_var = manager.list([""])
        queue = multiprocessing.Queue()

        p1 = multiprocessing.Process(target=process1, args=(queue, flag, count, check, string_var))
        p2 = multiprocessing.Process(target=process2, args=(queue, flag, count, check, string_var))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        print("Tiến trình đã kết thúc")
