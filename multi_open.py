# coding:utf-8

import win32gui,win32process
import ConfigParser  
import threading
import os, time
import shutil

# 配置程序路径
config = {
    'console' : 'disable', #disable/enable
    #'workdir' : r'E:\svn_code\gf510k\client\gfsl\src\branches\android\v2.0.20171103_tcyapp'.replace('\\', '/'), 
    'workdir' : r'E:\svn_code\gf510k\client\gfsl\src\trunk'.replace('\\', '/'),     #lua脚本路径
    'exePath' : r'E:\svn_code\gf510k\client\gfsl\src\runtime\MCRuntime.exe'.replace('\\', '/') #MCRuntime.exe路径
}

# 配置用户名密码
user_list = [
    {'username':'chenej01', 'password':'666554xa'},
    {'username':'chenej02', 'password':'666554xa'},
    {'username':'chenej03', 'password':'666554xa'},
    {'username':'chenej04', 'password':'666554xa'},
]

def getHight(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return bottom - top
    
def MyCallback(hwnd, windows):  
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == windows['pid'] and getHight(hwnd) > 0:
        #print 'find!'
        #print hwnd
        windows['hwnd'] = hwnd
        return False
    return True
    
def GetMainHwnd(procId):  
    windows = {'pid':procId}
    while True: # until findIt
        try:
            win32gui.EnumWindows(MyCallback, windows)
        except Exception, e: #MyCallback return Flase will cause EnumWindows raise an exception, catch it, and means it's time to break
            break        
    
    return windows['hwnd']

class IniConfig():
    def __init__(self, iniPath):
        self._config = ConfigParser.ConfigParser()
        self._config.read(iniPath)
        self.oriName = self._config.get("user","name")
        self.oriPass = self._config.get("user","password")
        self.iniPath = iniPath
    
    def cvtPath(self, exePath):
        '''convert ExePath to INI File path'''
        return exePath.replace('MCRuntime.exe', 'windows.ini')
        
    def saveIni(self):
        self._config.write(open(self.iniPath, 'w'))
    
    def saveOriInfo(self):
        self._config.set("user","name", self.oriName)  
        self._config.set("user","password",self.oriPass) 
        self.saveIni()
    
    def writeUserAndPass(self, name, password):
        self._config.set("user","name", name)  
        self._config.set("user","password", password)  
        self.saveIni()
        
lock = threading.Lock()

def startProcessThread(exePath, config):
    handle = win32process.CreateProcess(exePath, '-console ' + config['console'] + ' -workdir ' + config['workdir'],\
                                    None , None , 0 ,win32process. CREATE_NO_WINDOW , None , config['workdir'] ,win32process.STARTUPINFO())
    return handle
    
def startProcess(config):
    handle = win32process.CreateProcess(config['exePath'], '-console ' + config['console'] + ' -workdir ' + config['workdir'],\
                                    None , None , 0 ,win32process. CREATE_NO_WINDOW , None , config['workdir'] ,win32process.STARTUPINFO())
    return handle

def adjustPosition(handle, count):
    procId = handle[2]
    hwnd = GetMainHwnd(procId)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    hight = bottom - top
    #print 'hight:', hight
    Xoff = (count % 2) * width
    Yoff = (1 if (count % 4) > 1 else 0) * (hight - 160)
    #print 'Xoff', Xoff
    #print 'Yoff', Yoff
    win32gui.MoveWindow(hwnd, 0  + Xoff, 0 + Yoff, width, hight + 20, True)

def getConfigInstance():
    ObjConfig = IniConfig(config['exePath'].replace('MCRuntime.exe', 'windows.ini'))
    return ObjConfig

def getConfigInstanceByPath(strPath):
    ObjConfig = IniConfig(strPath + '/windows.ini')
    return ObjConfig

def copyRuntimeDir(oridir, nCount):
    for i in range(0, nCount):
        cvtstr = convertExePath2IniPathBySeq(oridir, i)
        if os.path.exists(cvtstr) == False:
            oriPath, name = os.path.split(oridir)
            shutil.copytree(oriPath, cvtstr)
            
def convertExePath2IniPathBySeq(exePath, seq):
    oripath, filename = os.path.split(exePath)
    cvtstr = exePath.replace('/' + filename, str(seq))
    return cvtstr
    
    
def startAllProcess(ObjConfig, user_list):
    copyRuntimeDir(config['exePath'], len(user_list))
    count = 0
    for i in range(0, len(user_list)):
        startOneProcess(i, count, ObjConfig, user_list)
        count += 1
        print 'count:', count
        
def startAllProcessThread(user_list):
    copyRuntimeDir(config['exePath'], len(user_list))
    count = 0
    for i in range(0, len(user_list)):
        ObjConfig = getConfigInstanceByPath(convertExePath2IniPathBySeq(config['exePath'], i))
        t = threading.Thread(target=startOneProcess, args=(i, count, ObjConfig, user_list))
        t.start()
        count += 1
        print 'count:', count
    
def startOneProcess(seq, count, ObjConfig, user_list):
    if seq < 0 or seq >= len(user_list):
        print u'没有这个序号'
        return None
    lock.acquire()
    ObjConfig.writeUserAndPass(user_list[seq]['username'], user_list[seq]['password'])
    handle = startProcessThread(convertExePath2IniPathBySeq(config['exePath'], seq) + '/MCRuntime.exe', config)
    lock.release()
    adjustPosition(handle, count)
    
if __name__ == '__main__':
    tips='''\
=====================================================================
|                      模拟器多开工具 v1.0 by chenej                |
=====================================================================
'''
    
    ObjConfig = getConfigInstance()
    startAllProcessThread(user_list)
    ObjConfig.saveOriInfo()
        
