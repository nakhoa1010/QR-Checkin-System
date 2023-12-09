# QR-Checkin-System

*95Embedded - QR Check in System*
## 1. Giới thiệu tổng quan

Thiết kế hệ thống điểm danh ra vào cho một sự kiện, sử dụng Mã QR kết hợp xác minh bằng khuôn mặt

### Mục tiêu:

- Tạo hệ thống tạo sự kiện.
- Tạo mã QR cho mỗi cá nhân tham gia sự kiện.
- Xác minh mã QR của cá nhân có tồn tại trong hệ thống hay không. 
- Kết hợp xác minh bằng khuôn mặt.

## 2. Hardware & Software

### Hardware 
|Tên phần cứng|Số Lượng|Mục đích|
|:---:|:---:|:---:|
|Raspberry Pi 4|2|Nhân xử lý chính của hệ thống.|
|Màn hình 7 inch HDMI|1|Màn hình hiển thị cho Raspberry Pi 4|
|Module đọc mã QR|1|Đọc mã QR.|
|Camera Raspberry Pi 4 V2|2|Phục vụ xác minh bằng khuôn mặt.|
|Cảm biến hồng ngoại|1|Kiểm tra người ra vào.|
|ESP32|1|Đọc tín hiệu từ cảm biến hồng ngoại.|

### Software 
- **Ngôn ngữ sử dụng**: `Python` (cho Raspberry Pi 4) & `Arduino` (cho ESP32)
- Các thư viện Python chính được sử dụng trong Project: 
1. [**QR code**](https://pypi.org/project/qrcode/): tạo mã QRCode
2. [**face-recognition**](https://github.com/ageitgey/face_recognition): thuật toán nhận diện khuôn mặt
3. [**OpenCV**](https://pypi.org/project/opencv-python/), [**dlib**](https://pypi.org/project/dlib/): thư viện hỗ trợ cho face-recognition
4. [**MySQL Connector Python**](https://pypi.org/project/mysql-connector-python/): kết nối với Database

## 3. Triển khai

### Flowchart

![Flowchart](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/flowchart.png?raw=true)

- Đầu tiên, camera ở cổng `In` sẽ kiểm tra khuôn mặt có tồn tại trong hệ thống không, nếu khuôn mặt không tồn tại trong hệ thống khi đi qua cảm biến hồng ngoại sẽ phát thông báo `Vui lòng quét QR`. Nếu như đã tồn tại thì cho phép đi vào.
- Tiếp theo, quét mã QR, nếu mã QR không tồn tại trong hệ thống. Hệ thống sẽ thông báo `QR không tồn tại`. Ngược lại, hệ thống sẽ yêu cầu khách hàng chụp ảnh khuôn mặt và lưu vào database.

### Sơ đồ kết nối ngoại vi
![Hardware](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/hardware.png?raw=true)


### Các thành phần chính

#### 1. Cấu trúc cơ sở dữ liệu
|Tên dữ liệu|ID|QRID|Tên|Giới tính|Facepath|TimeIn|
|---|---|---|---|---|---|---|
|Giải thích|Số thứ tự|Mã QR của cá nhân tham dự sự kiện|Tên người tham dự|Giới tính|Đường dẫn đến nơi lưu trữ khuôn mặt|Thời gian thực hiện Check In|
|Ví dụ|1|EventA-abc123xyz|Nguyễn Anh Khoa|Nam|facepath/EventA-abc123xyz|2023-11-07 11:06:37|

File SQL khởi tạo cơ sở dữ liệu: [Database](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/main/yourtablename.sql)

#### 2. Tạo mã QR: [QR_Generator](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/main/QR_Generator.py)


#### 3. Nhận diện khuôn mặt bằng face-recognition

Dựa trên [face-recognition](https://github.com/ageitgey/face_recognition) sủ dụng model Harcascade frontface của OpenCV
```python
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
```

Sử dụng thêm model 68 điểm khuôn mặt
```python
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
``` 
để xác nhận khuôn mặt có nhìn vào camera hay không 
```python
while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            playsound('nhin.mp3')
        else:
            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                if (len(shape[36:48]) >= 6) & (len(shape[48:68]) >= 20):  # Số lượng điểm đánh dấu mắt ít nhất là 6
                    check = 1
                else:
                    playsound('nhin.mp3')
```

#### 4. Đọc mã QR từ cảm biến sử dụng thư viện serial
```python
import serial
```
```python 
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
```

## 4. Demo
[Link Demo](https://youtube.com/)
## 5. Kết quả đạt được

## 6. Hướng phát triển tiếp theo
- [ ] Làm giao diện UI/UX

## 7. Material 

