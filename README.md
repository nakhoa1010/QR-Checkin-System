# QR-Checkin-System

*95Embedded - QR Check in System*
## 1. Giới thiệu tổng quan

Thiết kế hệ thống điểm danh ra vào cho một sự kiện, sử dụng Mã QR kết hợp xác minh bằng khuôn mặt

### Mục Tiêu:

- Tạo hệ thống tạo sự kiện.
- Tạo mã QR cho mỗi cá nhân tham gia sự kiện.
- Xác minh mã QR của cá nhân có tồn tại trong hệ thống hay không. 
- Kết hợp xác minh bằng khuôn mặt.

## 2. Hardware & Software
### Hardware 
|Tên phần cứng|Số Lượng|Mục đích|
|---|:---:|---|
|Raspberry Pi 4|2|Nhân xử lý chính của hệ thống.|
|Màn hình 7 inch HDMI|1|Màn hình hiển thị cho Raspberry Pi 4|
|Module đọc mã QR|1|Đọc mã QR.|
|Camera Raspberry Pi 4 V2|2|Phục vụ xác minh bằng khuôn mặt.|
|Cảm biến hồng ngoại|1|Kiểm tra người ra vào.|
|ESP32|1|Đọc tín hiệu từ cảm biến hồng ngoại.|

### Software 
- **Ngôn ngữ sử dụng**: `Python` (cho Raspberry Pi 4) & `Arduino` (cho ESP32)
- Các thư viện Python chính sử dụng trong Project: 
1. [**QR code**](https://pypi.org/project/qrcode/): tạo mã QRCode
2. [**OpenCV**](https://pypi.org/project/opencv-python/), [**dlib**](https://pypi.org/project/dlib/): phục vụ xác minh gương mặt
3. [**MySQL Connector Python**](https://pypi.org/project/mysql-connector-python/): kết nối với Database

## 3. Triển khai
### Flowchart

![Flowchart](https://github.com/nakhoa1010/QR-Checkin-System/blob/main/pic/flowchart.png?raw=true)

- Đầu tiên, camera ở cổng `In` sẽ kiểm tra khuôn mặt có tồn tại trong hệ thống không, nếu khuôn mặt không tồn tại trong hệ thống khi đi qua cảm biến hồng ngoại sẽ phát thông báo `Vui lòng quét QR`. Nếu như đã tồn tại thì cho phép đi vào.
- Tiếp theo, quét mã QR, nếu mã QR không tồn tại trong hệ thống. Hệ thống sẽ thông báo `QR không tồn tại`. Ngược lại, hệ thống sẽ yêu cầu khách hàng chụp ảnh khuôn mặt và lưu vào database.

### Cấu trúc cơ sở dữ liệu
|ID|QRID|Tên|Giới tính|Facepath|TimeIn|
|---|---|---|---|---|---|
|Số thứ tự|Mã QR của cá nhân tham dự sự kiện|Tên người tham dự|Giới tính|Đường dẫn đến nơi lưu trữ khuôn mặt|Thời gian thực hiện Check In|
### Nhận Diện khuôn mặt bằng OpenCV và dlib

### Kết nối các thành phần
- Khởi tạo cơ sở dữ liệu: [Database](/QR-Checkin-System/main/yourtablename.sql)
- 

## 4. Demo
## 5. Ket qua dat duoc
## 6. Uu, nhuoc & huong phat trien
## 7. Material 

