import time
import threading
import sys
import get_token

import nls
import os

URL="wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN=get_token.get_token()  #参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY=os.getenv("NLS_APP_KEY")     #获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist



TEXT='队友呢队友呢救一下啊'

#以下代码会根据上述TEXT文本反复进行语音合成
class TestTts:
    def __init__(self, tid, test_file):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file
   
    def start(self, text):
        self.__text = text
        self.__f = open(self.__test_file, "wb")
        #self.__th.start()
        self.__test_run()
    
    def test_on_metainfo(self, message, *args):
        #print("on_metainfo message=>{}".format(message))  
        None

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        #print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def test_on_completed(self, message, *args):
        #print("on_completed:args=>{} message=>{}".format(args, message))#
        None


    def __test_run(self):
        #print("thread:{} start..".format(self.__id))
        tts = nls.NlsSpeechSynthesizer(url=URL,
      	      	      	      	       token=TOKEN,
      	      	      	      	       appkey=APPKEY,
      	      	      	      	       on_metainfo=self.test_on_metainfo,
      	      	      	      	       on_data=self.test_on_data,
      	      	      	      	       on_completed=self.test_on_completed,
      	      	      	      	       on_error=self.test_on_error,
      	      	      	      	       on_close=self.test_on_close,
      	      	      	      	       callback_args=[self.__id])
        #print("{}: session start".format(self.__id))
        r = tts.start(self.__text, voice="ailun",aformat="wav")
        #print("{}: tts done with result:{}".format(self.__id, r))

def multiruntest(text,num=500):
    for i in range(0, num):
        name = "thread" + str(i)
        t = TestTts(name, "test_tts.wav")
        t.start(text)

def text2audio(text=TEXT):
    nls.enableTrace(False)
    multiruntest(text=text,num=1)
    return 'TTS完成'

#text2audio()