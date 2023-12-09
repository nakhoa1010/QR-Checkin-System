import cv2
import numpy as np
import face_recognition
import os
import glob
import retrivedata as data
from picamera2 import Picamera2

path = r"facepath"
images = []
classnames = []
mylist = os.listdir(path)
print(mylist)
count = len(mylist)


for cl in mylist:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])
print(classnames)


def findEndcodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeList = findEndcodings(images)
print("Encodding Complete")
print(len(encodeList))

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

img = picam2.capture_array()
before = os.listdir(path)
len1 = len(before)
while True:
    # success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    after = os.listdir(path)
    len2 = len(after)
    if len2 > len1:
        # Find the new image by comparing the lists
        new_image = set(after) - set(before)
        # Get the full path of the new image
        if new_image:
            new_image_path = os.path.join(path, new_image.pop())
            img_new = cv2.imread(new_image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            file_name, _ = os.path.splitext(os.path.basename(new_image_path))
            classnames.append(file_name)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
            print(classnames)
            print(len(encodeList))
        else:
            print("No new image added to the folder.")
        len1 = len2
    faceLocFrame = face_recognition.face_locations(imgS)
    encodeFrame = face_recognition.face_encodings(imgS, faceLocFrame)

    for encodeFace, faceLoc in zip(encodeFrame, faceLocFrame):
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        faceDis = face_recognition.face_distance(encodeList, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            # print(name)
            mydb = data.connect_database()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT Ten FROM yourtablename WHERE QRID = %s", (name,))
            available = mycursor.fetchall()
            var = list(available[0])
            print(var[0])
        else:
            # if cambien == 0
            # print("Xin vui long quet QR")
            print("Khong co trong danh sach")
    cv2.imshow("frame", img)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
