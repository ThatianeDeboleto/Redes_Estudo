  import telnetlib
	import time
	import re
	import subprocess
	import os
	
	resCount=0
	pingCount=0
	
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
	    telnet.write("reboot" +"\n")
	    time.sleep(1)
	    telnet.close()
	    global resCount
	    resCount+=1
	    print 'restart...'
	
	def restartTransmission():
		os.system("taskkill /im Transmission-qt.exe")
		time.sleep(1)
		subprocess.Popen("\"C:\\Program Files\\Transmission\\transmission-qt.exe\"")
	
	def ping():
	    global pingCount
	    pingCount+=1
	    website = "4.2.2.4"
	    try:
	        ping = subprocess.Popen(["ping", website], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	        out, error = ping.communicate()
	        if out:
	            print out
	            if "Reply from " + website in out and not "unreachable" in out:
	                return True
	            else:
	            	return False 
	    except subprocess.CalledProcessError:
	        print "Couldn't get a ping"
	    return False
	
	while True:
	    os.system("cls")
	    print("ping #%d , res #%d" % (pingCount , resCount) )
	
	    try:
	        if not ping():
	            print 'ping not success'
	            restart()
	            time.sleep(99)
	            restartTransmission()
	        else:
	            print 'ping ok'
	    except Exception:
	        time.sleep(10)
	    time.sleep(5)
