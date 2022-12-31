import traceback
import numpy as np

try:
    def findstat(queue, queue1, diffNumber):
        
        driver = 0
        
        try:
        
            import undetected_chromedriver as uc
            from bs4 import BeautifulSoup
            from selenium.common.exceptions import NoSuchElementException, TimeoutException
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By 
            driver = uc.Chrome()
            wait = WebDriverWait(driver, timeout=60, poll_frequency=0.1, ignored_exceptions=[NoSuchElementException])
            while True:
                i = queue.get()
                if i[0] == 'exit':
                    quit()
                #i [name, team, winrate, kd, timeIstr, timesShturm]
                url = 'https://warthunder.ru/ru/community/userinfo/?nick=' + i[0]
                try:
                    driver.get(url)
                    wait.until(EC.presence_of_element_located((By.ID, "bodyRoot")))
                except Exception as e:
                    if type(e)==TimeoutException:
                        i = np.append(i, 50)
                        i = np.append(i, 0)
                        i = np.append(i, "N/A")
                        i = np.append(i, "N/A")
                        #print(i)
                        queue1.put(i)
                        continue
                soup = BeautifulSoup(driver.page_source, "html.parser")
                #print(soup)
                #allNews = soup.findAll('a', class_='lenta')
                #elements1=soup.find_all(attrs={"class":{"ownershipPeriods-from"}})
                #user-stat__list-row
                #soup.select('li:nth-of-type(3)')
                divs = soup.findAll('div', class_='user-stat__list-row')
                if len(divs) == 0:
                    i = np.append(i, 50)
                    i = np.append(i, 0)
                    i = np.append(i, "N/A")
                    i = np.append(i, "N/A")
                    #print(i)
                    queue1.put(i)
                    continue           
                wins = divs[0].select('li:nth-of-type(2)')
                battles = divs[0].select('li:nth-of-type(3)')
                
                wins = wins[diffNumber].text
                if wins == "N/A":
                    wins = 0
                battles = battles[diffNumber].text
                if battles == "N/A" or battles == "0":
                    battles = 1
                #print(battles)
                #print(wins)
                winrate = round(int(wins)/int(battles)*100, 2)
                if winrate == 0:
                    winrate = 50
                
                awins = divs[0].select('li:nth-last-of-type(3)')   
                twins = divs[0].select('li:nth-last-of-type(2)')
                mwins = divs[0].select('li:nth-last-of-type(1)')
                
                awins = awins[diffNumber].text
                if awins == "N/A":
                    awins = 0 
                twins = twins[diffNumber].text
                if twins == "N/A":
                    twins = 0 
                mwins = mwins[diffNumber].text
                if mwins == "N/A":
                    mwins = 0      
                sumwins = int(awins)+int(twins)+int(mwins)
                kd = round(sumwins/int(battles), 2) 
                
                timeIstr = divs[1].select('li:nth-of-type(6)')
                timesShturm = divs[1].select('li:nth-of-type(8)')
                
                timeIstr = timeIstr[diffNumber].text
                timesShturm = timesShturm[diffNumber].text
                
                i = np.append(i, winrate)
                i = np.append(i, kd)
                i = np.append(i, timeIstr)
                i = np.append(i, timesShturm)
                #print(i)
                queue1.put(i)
                
        except Exception as e:
            print(e)
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()


    if __name__ == "__main__":

        from tkinter import *
        from tkinter import ttk
        import re
        from multiprocessing import Queue, Process, cpu_count
        #import math
        import os
        from pathlib import Path
        #import win32api, win32con, pywintypes, win32com.client, pythoncom
        import win32gui
        #from threading import Timer
        #import time

        #from selenium import webdriver


        def dexor(data, key):
            d_data = bytearray(len(data))
            key_length = len(key)
            for i, c in enumerate(data):
                d_data[i] = (c ^ key[i % key_length])
            return d_data
        
        paths = sorted(Path("../.game_logs").iterdir(), key=os.path.getmtime)    
        clogFile = open(paths[len(paths)-1], 'rb')
        #clogFile = open('5.clog', 'rb')
        keyFile =  open("key.bin", 'rb')

        data = bytearray(clogFile.read())
        key = bytearray(keyFile.read())
        clogFile.close()
        keyFile.close()

        dexorData = dexor(data, key)
        dexoredText = dexorData.decode('utf-8', 'ignore')
        dexoredTexts = dexoredText.split('Load mission')
        #print(len(dexoredTexts))
        dexoredText=dexoredTexts[len(dexoredTexts)-1]
        #print(dexoredText)
        diffObj = {
        'arcade': 1,
        'realistic': 2,
        'hardcore': 3
        }
        diff = re.search(r'MISSION \S+ STARTED at difficulty (\w+)' , dexoredText)
        diffNumber = diffObj[diff[1]]
        names = re.findall(r'MULP onStateChanged\(\) MULP p\d+ n=\'(\S+)\' NOT_EXISTS->IN_LOBBY_NOT_READY t=(\d)', dexoredText)

        #MULP p24 n=\'ycb_\' NOT_EXISTS->IN_LOBBY_NOT_READY t=2
        #MULP p24 n='ycb_' NOT_EXISTS->IN_LOBBY_NOT_READY t=2
        #MULP p12 n=\'Oliver_231\' NOT_EXISTS->IN_LOBBY_NOT_READY t=1
        #Pygmetanker (80435814) joined to room
        #MISSION eastern_europe_Bttl STARTED at difficulty realistic
        #print(names[0][0])
        #print(len(names))

        team1 = []
        team2 = []
        teams = []
        #k1=0
        for i in names:
            teams.append([i[0], i[1]])
            #k1+=1
            #if k1>=3:
                #break
        # for i in names:
            # if i[1] == '2':
                # team2.append([i[0]])
            # else:
                # team1.append([i[0]])
        print(diff[1])
        teams = np.array(teams)
        queue = Queue()
        queue1 = Queue()
        cpus = cpu_count()
        file = open('cpus.txt', 'r')
        number = file.read()
        if number != "" and number != "0":
            cpus = int(number)
        file.close()
        for i in teams:
            queue.put(i)   
        for i in range(cpus):
            if i == len(teams):
                break
            process = Process(target=findstat, args=(queue, queue1, diffNumber))
            process.start()
        counter = 0
        while True:
            i = queue1.get()
            print(i)
            if i[1] == '2':
                team2.append(i)
            else:
                team1.append(i)
            counter+=1
            if counter == len(teams):
                for i in range(cpus):
                    queue.put(["exit"])
                break
        team1winrate = 0
        team1kd = 0
        team1kdlen = 0
        for i in range(len(team1)):
            winrate = team1[i][2]
            winrate = float(winrate)    
            team1winrate+=winrate
            kd = float(team1[i][3])
            team1[i][3] = kd
            if kd != 0:
                team1kd+=kd
            else: team1kdlen+=1
        team1winrate=round(team1winrate/len(team1), 2)
        if team1kd !=0:
            team1kd=round(team1kd/(len(team1)-team1kdlen), 2)
        
        team2winrate = 0
        team2kd = 0
        team2kdlen = 0
        for i in range(len(team2)):
            winrate = team2[i][2]
            winrate = float(winrate)    
            team2winrate+=winrate
            kd = float(team2[i][3])
            team2[i][3] = kd
            if kd != 0:
                team2kd+=kd
            else: team2kdlen+=1
        team2winrate=round(team2winrate/len(team2), 2)
        #print(team2winrate)
        if team2kd!=0:
            team2kd=round(team2kd/(len(team2)-team2kdlen), 2)
        #print(team2kd)
        #print(team1)
        #print(team2)

        data_type = [('name', np.dtype('U100')), ('team', np.dtype('U100')),('winrate', np.dtype('U100')), ('kd', float), ('time', np.dtype('U100')), ('time1', np.dtype('U100'))]
        team1forSort = np.core.records.fromarrays(np.array(team1).transpose(),
        names='col1, col2, col3, col4, col5, col6',
        formats = 'U100, U100, U100, f8, U100, U100')
        team2forSort = np.core.records.fromarrays(np.array(team2).transpose(),
        names='col1, col2, col3, col4, col5, col6',
        formats = 'U100, U100, U100, f8, U100, U100')
        team1forSort = np.array(team1forSort, dtype = data_type)
        team2forSort = np.array(team2forSort, dtype = data_type)
        #print(team1forSort)
        #print(team2forSort)
        team1 = np.sort(team1forSort, order = 'kd')[::-1]
        team2 = np.sort(team2forSort, order = 'kd')[::-1]

        def selectWindow(event):
            try:
                toplist = []
                winlist = []
                def enum_callback(hwnd, results):
                    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

                win32gui.EnumWindows(enum_callback, toplist)
                wt = [(hwnd, title) for hwnd, title in winlist if 'war thunder' in title.lower()]
                # just grab the first window that matches
                if wt !=[]:
                    wt = wt[0]
                    #pythoncom.CoInitializeEx(0)
                    #shell = win32com.client.Dispatch("WScript.Shell")
                    #shell.SendKeys('%')                
                    # use the window handle to set focus
                    win32gui.SetForegroundWindow(wt[0])  
            except Exception as e:
                file = open('error.log', 'a')
                file.write('\n\n')
                traceback.print_exc(file=file, chain=True)
                traceback.print_exc()
                file.close()                
        
        root = Tk()
        root.geometry(f'1250x800+{int(root.winfo_screenwidth()/2-625)}+{int(root.winfo_screenheight()/2-400)}')
        root.bind("<Button-1>",selectWindow)
        root.bind("<Button-2>",selectWindow)
        root.bind("<Button-3>",selectWindow)  
        label1 = Label(root, text=f'{diff[1]}', font=('Roboto','14'), fg='gray')
        label1.master.overrideredirect(True)
        label1.master.lift()
        label1.master.wm_attributes("-topmost", True)
        
        # hWindow = pywintypes.HANDLE(int(label1.master.frame(), 16)) 
        # exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
        # win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)        
        
        label1.pack()
        sign = 0
        if team1winrate>team2winrate:
            sign = '>'
        elif team1winrate==team2winrate:
            sign = '='
        else:
            sign = '<'
        label2 = Label(root, text=f'{team1winrate} {sign} {team2winrate}', font=('Roboto','19', 'bold'), fg='black')
        label2.master.overrideredirect(True)
        label2.master.lift()
        label2.master.wm_attributes("-topmost", True)
        
        # hWindow = pywintypes.HANDLE(int(label2.master.frame(), 16)) 
        # exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
        # win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)        
        
        label2.pack()
        if team1kd>team2kd:
            sign = '>'
        elif team1kd==team2kd:
            sign = '='
        else:
            sign = '<'    
        label3 = Label(root, text=f'{team1kd} {sign} {team2kd}', font=('Roboto','17'), fg='black')
        label3.master.overrideredirect(True)
        label3.master.lift()
        label3.master.wm_attributes("-topmost", True)

        # hWindow = pywintypes.HANDLE(int(label3.master.frame(), 16)) 
        # exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
        # win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        
        label3.pack()
        
        
        
        columns = ("nickname", "fighter", "attacker", "% winrate", "Kills per Battle")
        tree = ttk.Treeview(columns=columns, show="headings")
        tree.master.overrideredirect(True)
        tree.master.lift()
        tree.master.wm_attributes("-topmost", True)
        
        # hWindow = pywintypes.HANDLE(int(tree.master.frame(), 16)) 
        # exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
        # win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)        
        
        tree.pack(fill=Y, expand=1, side=LEFT)
        tree.heading("nickname", text="Ник", anchor=W)
        tree.heading("fighter", text="Истребитель", anchor=W)
        tree.heading("attacker", text="Штурмовик", anchor=W)
        tree.heading("% winrate", text="% Побед", anchor=W)
        tree.heading("Kills per Battle", text="Фраги на бой", anchor=W)
        tree.column("#1", stretch=NO, width=140, anchor=W)
        tree.column("#2", stretch=NO, width=100, anchor=W)
        tree.column("#3", stretch=NO, width=100, anchor=W)
        tree.column("#4", stretch=NO, width=85, anchor=W)
        tree.column("#5", stretch=NO, width=105, anchor=W)
        for i in range(len(team1)):
            tree.insert("", END, values=(team1[i][0], team1[i][4], team1[i][5], team1[i][2], team1[i][3]))
            
            
        columns1 = ("Kills per Battle", "% winrate", "attacker", "fighter", "nickname")
        tree1 = ttk.Treeview(columns=columns1, show="headings")
        tree1.master.overrideredirect(True)
        tree1.master.lift()
        tree1.master.wm_attributes("-topmost", True)
        
        # hWindow = pywintypes.HANDLE(int(tree1.master.frame(), 16)) 
        # exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TRANSPARENT
        # win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)        
        
        tree1.pack(fill=Y, expand=1, side=RIGHT)
        tree1.heading("nickname", text="Ник", anchor=W)
        tree1.heading("fighter", text="Истребитель", anchor=W)
        tree1.heading("attacker", text="Штурмовик", anchor=W)
        tree1.heading("% winrate", text="% Побед", anchor=W)
        tree1.heading("Kills per Battle", text="Фраги на бой", anchor=W)
        tree1.column("#1", stretch=NO, width=105, anchor=W)
        tree1.column("#2", stretch=NO, width=85, anchor=W)
        tree1.column("#3", stretch=NO, width=100, anchor=W)
        tree1.column("#4", stretch=NO, width=100, anchor=W)
        tree1.column("#5", stretch=NO, width=140, anchor=W)
        for i in range(len(team2)):
            tree1.insert("", END, values=(team2[i][3], team2[i][2], team2[i][5], team2[i][4], team2[i][0]))     
        
        def close():      
            quit()
        
        btn1 = ttk.Button(text="X", command=close, width=3)
        btn1.master.overrideredirect(True)
        btn1.master.lift()
        btn1.master.wm_attributes("-topmost", True)
        btn1.place(x=1250-33, y=3)

        # timeout = 0
        # t = Timer(timeout, selectWindow)
        # t.start()    
            
        root.mainloop()    
        #print(team1)
        #print(team2)
                   
        #options = uc.ChromeOptions()
        #options.add_argument("--no-startup-window")

        #driver = webdriver.Chrome()

            
        #findstat(team1)
        #findstat(team2) 

        # print(element)
        # driver.get('https://warthunder.ru/ru/community/userinfo/?nick=_ICU_Paimon')
        # element = wait.until(EC.presence_of_element_located((By.ID, "bodyRoot")))
        # print(element)
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.close()