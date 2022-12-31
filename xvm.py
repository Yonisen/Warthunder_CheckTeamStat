import traceback

try:
    
    def signal1(queue):
        try:
        
            import signal1
            signal1.signal1(queue)
            
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()    
            
    def signal3(queue):
        try:
        
            import signal3
            signal3.signal3(queue)
            
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()                
    
    if __name__ == "__main__":
    
        #import time
        #from tkinter import *
        from subprocess import Popen
        from multiprocessing import Queue, Process    
    

        queue = Queue()
        process1 = Process(target=signal1, args=(queue,))
        process1.start()
        process3 = Process(target=signal3, args=(queue,))
        process3.start()        
        
        #comand=["python", 'signal1.py']  
        #Popen(comand)                                                     
        print("Программа ожидает сочетания клавиш")

        # def on_activate_CtrlN():
            # print("n")

        # def on_activate_CtrlM():
            # print('m')

        # def for_canonical(f):
            # return lambda k: f(l.canonical(k))

        # hotkey = keyboard.HotKey(
            # keyboard.HotKey.parse('<ctrl>+n'),
            # on_activate)
        # with keyboard.Listener(
                # on_press=for_canonical(hotkey.press),
                # on_release=for_canonical(hotkey.release)) as l:
            # l.join()  
        # with keyboard.GlobalHotKeys({
            # '<ctrl>+n': on_activate_CtrlN,
            # '<ctrl>+m': on_activate_CtrlM}) as h:
            # h.join()                              
        while True:
            msg = queue.get()
            if msg == "parse":
                print("")
                comand=["python", 'parse_stat.py']
                Popen(comand)                        
            
            
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.close()