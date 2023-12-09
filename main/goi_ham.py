import mysql.connector
from datetime import datetime
from gtts import gTTS
from playsound import playsound

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
  elif sex == "Nu":
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
  
  line = "Kính chào" + sex + name
  language = "vi"
  say = gTTS(text = line, lang = language)
  say.save("welcome.mp3")
  # engine.say("Kính chào " + return_sex(sex) + " " + name)
  # engine.say("Xin vui lòng nhìn vào màn hình")
  # engine.runAndWait()
  playsound('welcome.mp3')
  playsound('nhin.mp3')
  
  

def update_data(QRID,img_path):
    newdate = current_time()
    mydb = connect_database()
    mycursor = mydb.cursor()    
    
    mycursor.execute("UPDATE yourtablename SET TimeIn = %s, FacePath = %s WHERE QRID = %s",(newdate,img_path,QRID,))
    mydb.commit()
    print("Thoi gian: ", newdate)




    
    