from gtts import gTTS
from playsound import playsound
import time
import sys
import tempfile

def main():
    if len(sys.argv) == 1:
        print("Please enter text to play")
        print("Usage: playfromtext <text>")
        sys.exit()
    tmp_f = tempfile.NamedTemporaryFile()
    now = time.localtime()
    current_time = time.strftime("%d_%m_%H_%M_%S", now)

    audio = "{}_audio{}".format(tmp_f.name,current_time)
    language = "en"
    extension = ".mp3"
    fileA = audio + extension

    test = ""
    for i in range(1,len(sys.argv)):
        test += sys.argv[i] + " "
    sp = gTTS(text = test, lang = language,slow=False)
    sp.save(fileA)
    playsound(fileA)

    print("In case you want the audio file, the path is: {}".format(fileA))