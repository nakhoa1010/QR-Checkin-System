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
|[Màn hình 7 inch HDMI](https://shopee.vn/M%C3%A0n-h%C3%ACnh-7-inch-IPS-HDMI-1024X600-i.29514670.16478114938)|1|Màn hình hiển thị cho Raspberry Pi 4|
|[Module đọc mã QR](https://hshop.vn/products/mach-gm65-1d-2d-qr-barcode-reader-scanner-module)|1|Đọc mã QR.|
|[Camera Raspberry Pi 4 V2](https://hshop.vn/products/camera-raspberry-pi-v2-8mp)|2|Phục vụ xác minh bằng khuôn mặt.|
|[Cảm biến hồng ngoại](https://hshop.vn/products/cam-bien-vat-can-hong-ngoai-e3f-ds100c4-adjustable-ir-infrared-proximity-sensor)|1|Kiểm tra người ra vào.|
|[ESP32](https://icdayroi.com/kit-rf-thu-phat-wifi-ble-esp32-wroom-32u-devkitc)|1|Đọc tín hiệu từ cảm biến hồng ngoại.|

### Software 
- **Ngôn ngữ sử dụng**: `Python` (cho Raspberry Pi 4) & `Arduino` (cho ESP32)
- Các thư viện Python chính được sử dụng trong Project:
- Project được chia thành 3 bài toán chính là:
1. Quét mã QR và chụp ảnh khuôn mặt (python)
- [**MySQL Connector Python**](https://pypi.org/project/mysql-connector-python/): kết nối với Database
- [**QR code**](https://pypi.org/project/qrcode/): tạo mã QRCode
- Multiprocessing: Chạy nhiều tiến trình song song
2. Xác minh khuôn mặt (python)
- [**face-recognition**](https://github.com/ageitgey/face_recognition): thuật toán nhận diện khuôn mặt
- [**OpenCV**](https://pypi.org/project/opencv-python/), [**dlib**](https://pypi.org/project/dlib/): thư viện hỗ trợ cho face-recognition
- [**MySQL Connector Python**](https://pypi.org/project/mysql-connector-python/): kết nối với Database
- MQTT: Giao thức kết nối ESP32 với Raspberry Pi, ở đây sử dụng để gửi messenge
3. Cảm biến hồng ngoại (Arduino)
- MQTT: Giao thức kết nối ESP32 với Raspberry Pi, ở đây sử dụng để nhận messenge


## 3. Triển khai

### Flowchart

![Flowchart](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/flowchart.png?raw=true)

- Đầu tiên, camera ở cổng `In` sẽ kiểm tra khuôn mặt có tồn tại trong hệ thống không, nếu khuôn mặt không tồn tại trong hệ thống khi đi qua cảm biến hồng ngoại sẽ phát thông báo `Vui lòng quét QR`. Nếu như đã tồn tại thì cho phép đi vào.
- Tiếp theo, quét mã QR, nếu mã QR không tồn tại trong hệ thống. Hệ thống sẽ thông báo `QR không tồn tại`. Ngược lại, hệ thống sẽ yêu cầu khách hàng chụp ảnh khuôn mặt và lưu vào database.

### Sơ đồ kết nối ngoại vi

Tổng quan

![Hardware](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/hardware.png?raw=true)


Sơ đồ kết nối các thành phần

![sodothanhphan](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/sodoketnoi.png?raw=true)

### Các thành phần chính

#### 1. Cấu trúc cơ sở dữ liệu
|Tên dữ liệu|ID|QRID|Tên|Giới tính|Facepath|TimeIn|
|---|---|---|---|---|---|---|
|Giải thích|Số thứ tự|Mã QR của cá nhân tham dự sự kiện|Tên người tham dự|Giới tính|Đường dẫn đến nơi lưu trữ khuôn mặt|Thời gian thực hiện Check In|
|Ví dụ|1|EventA-abc123xyz|Nguyễn Anh Khoa|Nam|facepath/EventA-abc123xyz|2023-11-07 11:06:37|

File SQL khởi tạo cơ sở dữ liệu: [Database](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/main/yourtablename.sql)

#### 2. Tạo mã QR: [QR_Generator](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/main/QR_Generator.py)


#### 3. Xây dựng thuật toán

a. Quét QR và chụp ảnh khuôn mặt

> Để xuất frame ảnh ra màn hình một cách liên tục và đồng thời chạy các công việc khác mà không bị gián đoạn, project sử dụng `multiprocessing` trong Python. Thư viện hỗ trợ chạy nhiều process cùng lúc và song song với nhau. Trong bài toán này, project sử dụng 3 process chính như sau :

![3process](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/3process.png?raw=true)

`Process 1`: Xuất frame ảnh ra màn hình và chụp ảnh khuôn mặt.

- Sau khi lấy frame ảnh từ camera thì sẽ xác định vị trí khuôn mặt có trong ảnh bằng cách sử dụng haarcascade. Sau đó, vẽ ô vuông màu xanh lá quanh khuôn mặt nhờ vào vị trí vừa xác định.
- Xuất ảnh ra màn hình
- Nếu nhận được giá trị từ process 2 thì sẽ chụp ảnh khuôn mặt có trong ảnh.


`Process 2`: Quét QR và kiểm tra khuôn mặt có nhìn vào camera hay không

- Đầu tiên quét mã QR, sau đó sẽ gửi tín hiệu cho process 3
- Tạo biến count để đếm số lần khách hàng nhìn vào camera.
- Nếu khách hàng nhìn vào camera thì count sẽ tăng lên 1, ngược lại khi khách hàng không nhìn vào camera thì count sẽ bằng 0.
- Nếu khách hàng nhìn vào camera 5 lần thì sẽ gửi tín hiệu cho process 1 để chụp ảnh khuôn mặt


`Process 3`: Dùng để voice thông báo
- Process 3 sẽ đợi tín hiệu của process 2
- Sau khi nhận tín hiệu của process 2 thì process 3 sẽ thực hiện voice “Kính chào “giới tính” + “tên” ”

b. Xác minh khuôn mặt

![facedetect](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/facedetect.png?raw=true)

- Đầu tiên kết nối MQTT với chuỗi subscription giống với ESP32 để nhận giá trị từ ESP32. Nếu: 

```python
def on_message(client, userdata, msg):
    if(msg.payload.decode("utf-8") == "0"):
        if flag == 1:
            engine.say("Xin vui lòng quét QR")
            engine.runAndWait()
```
-
    - Giá trị là `1`: __không có người đi qua__. 
    - Giá trị là `0`: __có người đi qua__. 
    - Giá trị là `0` và biến `flag = 0`: có người đi qua nhưng người đó đã quét mã QR. 
    - Giá trị là `0` và biến `flag = 1`: có người đi qua nhưng người đó chưa quét mã QR --> lập tức hệ thống sẽ cảnh báo.
- Sau đó encode tất cả các ảnh trong folder và lưu vào một mảng `ListEncode`.
- Mở camera và bắt đầu vòng lặp While.
- Nếu số lượng ảnh trong folder lúc sau lớn hơn số lượng lúc đầu có nghĩa là ảnh mới vừa được thêm vào folder. Sau đó sẽ encode ảnh mới và lưu encode đó vào `ListEncode`.
- Encode khuôn mặt có trong frame ảnh gọi là `EncodeFrame`.

```python
while True:
    success, img = cap.read()
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
```

- So sánh `EncodeFrame` với các giá trị encode có trong mảng `ListEncode` và lưu kết quả vào biến `matchIndex`.
```python
for encodeFace, faceLoc in zip(encodeFrame, faceLocFrame):
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        faceDis = face_recognition.face_distance(encodeList, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            print(name)
            mydb = data.connect_database()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT Ten FROM yourtablename WHERE QRID = %s", (name,))
            available = mycursor.fetchall()
            var = list(available[0])
            print(var[0])
            flag = 0
        else:
            flag = 1
            print("Khong co trong danh sach")
```
- Nếu:
    - `matchIndex` khác rỗng thì xuất tên và `flag = 0`.
    - `matchIndex` bằng rỗng thì `flag = 1`.

c. Phát hiện có vật cản đi qua

ESP32 kết nối wifi và MQTT với chuỗi subscription giống với Raspberry Pi. Nếu có người đi qua ESP32 sẽ gửi tín hiệu là `0`, ngược lại ESP32 sẽ gửi tín hiệu là `1`.

> [!IMPORTANT]
> ESP32 chỉ có thể sử dụng Wifi băng tần 2.4Ghz

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

> [!NOTE]
> Dùng lệnh `dmesg | grep tty` để lấy chính xác tên cổng Serial trên Raspberry Pi 4. ![serialport](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/serialport.png?raw=true)



## 4. Demo
[Link Demo](https://youtube.com/)
## 5. Kết quả đạt được

### Ưu điểm
- Hệ thống hoạt động đúng mục tiêu

### Nhược điểm
- Tốc độ thực thi chưa nhanh

## 6. Hướng phát triển tiếp theo
- [ ] Làm giao diện UI/UX



