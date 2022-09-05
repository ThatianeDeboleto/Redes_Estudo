import getpass
import telnetlib

HOST = "192.168.10.1"
User = input("enter username: ")
Password = getpass.getpass()

tn=telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(User.encode("ascii")+ b"\n")
if Password:
    tn.read_until(b"Password: ")
    tn.write(Password.encode('ascii')+ b"\n")
    
tn.write(b"enable\n")
tn.write(b"cisco\n")    #enable password
tn.write(b"config terminal\n")
tn.write(b"exit\n")

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import getpass
import telnetlib

HOST="192.168.10.1"
User= input("enter username: ")
Password= getpass.getpass()

tn=telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(User.encode("ascii")+ b"\n")
if Password:
    tn.read_until(b"Password: ")
    tn.write(Password.encode('ascii')+ b"\n")
    
tn.write(b"enable\n")
tn.write(b"cisco\n")    #senha
tn.write(b"config terminal\n")
tn.write(b"inter loopback 0\n")
tn.write(b"ip add 1.1.1.1 255.255.255.255\n")
tn.write(b"no shut\n")
tn.write(b"exit\n")
tn.write(b"wr\n")

print (tn.read_all().decode("ascii"))

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import telnetlib
import time
import re
import subprocess
import os

resCount = 0
pingCount = 0


def restart():
    hostserver = "192.168.1.1"
    newline = "\n"
    username = "root" + newline
    password = "admin" + newline
    telnet = telnetlib.Telnet(hostserver)
    telnet.read_until("login: ")
    telnet.write(username)
    telnet.read_until("Password: ")
    telnet.write(password)
    time.sleep(1)
    telnet.write("reboot" + "\n")
    time.sleep(1)
    telnet.close()
    global resCount
    resCount += 1
    print
    'restart...'


def restartTransmission():
    os.system("taskkill /im Transmission-qt.exe")
    time.sleep(1)
    subprocess.Popen("\"C:\\Program Files\\Transmission\\transmission-qt.exe\"")


def ping():
    global pingCount
    pingCount += 1
    website = "4.2.2.4"
    try:
        ping = subprocess.Popen(["ping", website], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        if out:
            print
            out
            if "Reply from " + website in out and not "unreachable" in out:
                return True
            else:
                return False
    except subprocess.CalledProcessError:
        print
        "Couldn't get a ping"
    return False


while True:
    os.system("cls")
    print("ping #%d , res #%d" % (pingCount, resCount))

    try:
        if not ping():
            print
            'ping not success'
            restart()
            time.sleep(99)
            restartTransmission()
        else:
            print
            'ping ok'
    except Exception:
        time.sleep(10)
    time.sleep(5)
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def myfile():
    
    192.168.10.1    #ip of switch 1
    192.168.10.2    #ip of switch 2
    192.168.10.3    #ip of switch 3
    192.168.10.4    #ip of switch 4
    192.168.10.5    #ip of switch 5
    
    
# Different file for code
import getpass
import telnetlib

HOST="local host"
User= input("enter username: ")
Password= getpass.getpass()

f = open("myfile")

for ip in f:
    ip = ip.strip()
    print ("configuring switch"+ (ip))
    HOST = ip
    
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(User.encode("ascii") + b"\n")
    
    if Password:
        tn.read_until(b"Password: ")
        tn.write(Password.encode('ascii') + b"\n")
        
    tn.write(b"enable\n")
    tn.write(b"cisco\n")    #enable password
    tn.write(b"config terminal\n")
    for n in range(1, 11):
        tn.write(b"vlan " + str(n).encode("ascii") + b"\n")
        tn.write(b"name VLAN" + str(n).encode("ascii") + b"\n")
    tn.write(b"end\n")    
    tn.write(b"exit\n")
    tn.write(b"wr\n")
    print (tn.read_all().decode("ascii"))
