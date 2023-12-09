import serial
import time
from barcode import get_barcode

# Thiết lập cổng serial để giao tiếp với mạch đọc mã vạch GM65
ser = serial.Serial('COM7', 9600, timeout=1)  # Thay 'COMx' bằng tên cổng serial thích hợp

# Hàm để đọc mã vạch từ mạch đọc mã vạch GM65
def read_barcode():
    ser.write(b'R\r\n')  # Gửi lệnh để đọc mã vạch
    
    barcode_data = ser.readline().decode().strip()  # Đọc dữ liệu từ cổng serial
    return barcode_data

# Hàm để tạo mã vạch từ dữ liệu đọc được
def generate_barcode(data):
    barcode = get_barcode('code128', data)
    barcode_path = 'barcode.png'  # Đường dẫn lưu trữ file ảnh mã vạch
    barcode.save(barcode_path)
    print(f'Mã vạch đã được tạo và lưu tại: {barcode_path}')

# Đọc và tạo mã vạch từ mạch đọc mã vạch GM65
try:
    while True:
        barcode_data = read_barcode()
        if barcode_data:
            print(f'Mã vạch đã đọc được: {barcode_data}')
        print("gjhasgdjhagsdjgajsd")    
except KeyboardInterrupt:
    print('Quá trình đọc mã vạch đã được dừng bởi người dùng.')
    ser.close()


