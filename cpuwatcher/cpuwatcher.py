# -*- coding: utf-8 -*-
# ==================================================
# 对 Timer 做以下再封装的目的是：当某个功能需要每隔一段时间被
# 执行一次的时候，不需要在回调函数里对 Timer 做重新安装启动
# ==================================================

from threading import Timer
from datetime import datetime
import os

def exec(command):
    line = []
    p = os.popen(command)
    while True:
        st = p.readline()
        if not st:
            break
        line.append(st)
    return line

class MyTimer( object ):

    def __init__( self, start_time, interval, callback_proc, args=None, kwargs=None ):

        self.__timer = None
        self.__start_time = start_time
        self.__interval = interval
        self.__callback_pro = callback_proc
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

    def exec_callback( self, args=None, kwargs=None ):
        self.__callback_pro( *self.__args, **self.__kwargs )
        self.__timer = Timer( self.__interval, self.exec_callback )
        self.__timer.start()

    def start( self ):
        interval = self.__interval - ( datetime.now().timestamp() - self.__start_time.timestamp() )
        print( interval )
        self.__timer = Timer( interval, self.exec_callback )
        self.__timer.start()

    def cancel( self ):
        self.__timer.cancel() 
        self.__timer = None

class CPUWatcher:

    def __init__(self,pid,filename):
        self.pid = pid
        self.filename = filename
        exec("touch "+ filename)

    def record(self):
        outVector = exec("top -n 3")
        vec = []
        targe = 0
        for i in outVector:
            if "top" in i and "load" in i:
                targe = targe + 1
            if targe > 1:
                vec.append(i)
        print(targe)
        cpualluse = vec[2].split(",")[3]
        pidcpuuse = ""
        for i in vec:
            if str(self.pid) in str(i):
                pidcpuuse = i
                break
        cpuuse = ""
        if len(pidcpuuse.split())>9:
            cpuuse = pidcpuuse.split()[8]
        else:
            cpuuse = pidcpuuse
        now = datetime.now()
        fo = open(self.filename,"a+")
        fo.write(str(now) + "," + cpualluse + ',' + cpuuse + "\r\n")
        fo.close()

if __name__ == "__main__":
    print("Input the Pid of watcher object,please!")
    pid = input()
    print("Input save file path,please!")
    filename = input()
    watcher = CPUWatcher(pid,filename)
    print("CPUWatcher init")
    start = datetime.now()
    tmr = MyTimer(start, 3 , watcher.record)
    print("MyTimer init")
    tmr.start()
    
