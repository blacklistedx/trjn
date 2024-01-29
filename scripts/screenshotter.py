import base64
import win32api
import win32con
import win32gui
import win32gui
import time #(Enables 5 second intervals between screenshots)

def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN) 
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='screenshot'):
    hdesktop = win32gui.GetDesktopWindow()      #Gets a handle on entire screen
    width, height, left, top = get_dimensions() #Gets screen dimensions

    desktop_dc = win32gui.GetWindowDC(hdesktop) #Standard steps when working with screenshots and windows API
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()        #

    screenshot = win32ui.CreateBitmap()         #Creates bitmap object to be saved as
    screenshot.CreateCompatibleBitmap(img_dc, width, height)    #Grabs the object to se memory device to point at bitmap device
    mem_dc.SelectObject(screenshot)                             #Calls screenshot object
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)    #Stores in created bitmap memory
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()

    return img

if __name__ == '__main__':
    time.sleep(5)
    screenshot()

