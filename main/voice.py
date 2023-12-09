from gtts import gTTS
import playsound


tts = gTTS('Xin vui lòng nhìn vào màn hình', lang='vi')
tts.save('nhin.mp3')