import tkinter as tk
import QR_Scan as scan
import retrivedata as check
import takeimage 


datain = scan.GetQR()
# datain = "EventA-abc125xyz"
# check.check(datain)

check_var = check.check_available(datain)

# print(check_var)
if check_var == None:
    print("QR khong ton tai trong he thong.")
else:
    print("QR ton tai trong he thong.")
    check.check(datain)
