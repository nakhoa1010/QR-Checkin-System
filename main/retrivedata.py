import mysql.connector
import cv2
from datetime import datetime
import takeimage as takeimage



def get_image_name(QRID):
  image_name = QRID + '.jpg'
  return image_name

def current_time():
  now = datetime.now()
  dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
  return dt_string

def return_status(flag):
  if flag == 0:
    return "vao lan dau"
  elif flag == 1:
    return "da ra giua gio"

def return_sex(sex):
  if sex == "Nam":
    return "ông"  
  elif sex == "Nữ":
    return "bà"

def connect_database():
  mydb = mysql.connector.connect(
    host="103.18.6.82",
    user="pck2uro1ax0t_sub",
    password="sub@Nakhoa_1010",
    database="pck2uro1ax0t_sub"
  )
  return mydb

def check_available(QRID): 
  mydb = connect_database()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT ID FROM yourtablename WHERE QRID = %s",(QRID,))
  available = mycursor.fetchone()
  return available
  
def check(datain):
  mydb = connect_database()
  
  QRID = datain
  
  mycursor = mydb.cursor()
  mycursor.execute("SELECT GioiTinh, Ten, TimeIn, FacePath FROM yourtablename WHERE QRID = %s",(QRID,))
  myresult = mycursor.fetchall()
  result = list(myresult[0])
  
  
  sex = result[0]  
  name = result[1]
  timein = result[2]
  facepath = result[3]
  # print ("Ho Va Ten: ",name,"\nGioiTinh: ",sex,"\nTrang thai: ",check_status(flag),"\nHinh anh:",facepath,"Thoi gian vao: ",timein)
  takeimage.engine.say("Kính chào " + return_sex(sex) + " " + name)
  takeimage.engine.runAndWait()
  print("Quy khach",return_status(facepath))
  if (facepath == None):
    
    #__Chen code chup hinh vao day_
    
    
    while takeimage.done == 0:  # Continue looping until img_path has a non-empty value
      img_path = takeimage.capture(get_image_name(QRID))

    
    print('Created ' + get_image_name(QRID) + ' image.')
    print('Save to: ' + img_path)
    #______________________________
    newdate = current_time()
      
    mycursor.execute("UPDATE yourtablename SET TimeIn = %s, FacePath = %s WHERE QRID = %s",(newdate,img_path,QRID,))
    mydb.commit()
    print("Thoi gian: ", newdate)
    
  else:
    print("Thoi gian vao lan dau: ", timein)

  takeimage.engine.say("Check in thành công")
  takeimage.engine.runAndWait()
if __name__ == "__main__":
  check('EventA-abc124xyz')