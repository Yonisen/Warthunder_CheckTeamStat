#from pynput.keyboard import Listener
#from pynput.keyboard import Listener
from pynput.keyboard import Controller, GlobalHotKeys
import traceback
#import pressKey
#import time
import configparser
import win32api

def signal1(queue):

    try:
        win32api.LoadKeyboardLayout('00000409',1)    
        keyboard = Controller()
        
        def read_config(name):
            config = configparser.ConfigParser()
            config.read(name, encoding='utf-8')
            conf = []
            conf.append(config.get("Комбинации", "Оленемер клавиатура"))
            conf.append(config.get("Комбинации", "Оленемер мышь"))
            return conf
        conf = read_config("buttons.ini")
        
        def on_activate_t():
            try:

                queue.put("parse")           

            except Exception as e:
                file = open('error.log', 'a')
                file.write('\n\n')
                traceback.print_exc(file=file, chain=True)
                traceback.print_exc()
                file.close()      
                 
        

        xvm = conf[0] or conf[1]
        if xvm == "":
            print("кнопка для оленемера не назначена")
        
        obj = {}
        if conf[0]:
            obj[conf[0]] = on_activate_t
        
        if obj != {}:
            with GlobalHotKeys(obj) as h:
                h.join()
            
    except Exception as e:
        file = open('error.log', 'a')
        file.write('\n\n')
        traceback.print_exc(file=file, chain=True)
        traceback.print_exc()
        file.write(str(e))
        file.close()
