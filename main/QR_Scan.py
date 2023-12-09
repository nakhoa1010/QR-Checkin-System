import cv2
def GetQR():
    cap = cv2.VideoCapture(0)
    # flip = cv2.flip(cap,0)
    detector=cv2.QRCodeDetector()
    while True:
        ret,frame=cap.read()
        if not ret:
            break
        flip_cam = cv2.flip(frame,1)
        data,one, _=detector.detectAndDecode(flip_cam)
        if data:
            a=data
            break
        cv2.imshow('QRCodeScanner',flip_cam)
        if cv2.waitKey(1)==ord('q'):
            break
    # b=webbrowser.open(str(a))
    
    cap.release()
    cv2.destroyAllWindows()
    return a
if __name__ == "__main__":
    print(GetQR())