import qrcode
datain = input('Nhap QRID: ')
img = qrcode.make(datain)
type(img)  # qrcode.image.pil.PilImage
img.save(datain +  ".jpg")
print("Save to: " + datain + ".jpg")
