import os
import time
import SendMail
import commands

def getdate():
    t=time.localtime(time.time()+3600*8)
    if(t.tm_mon<10):tm_mon='0'+str(t.tm_mon)
    else:tm_mon=str(t.tm_mon)
    if(t.tm_mday<10):tm_mday='0'+str(t.tm_mday)
    else:tm_mday=str(t.tm_mday)
    return str(t.tm_year)+tm_mon+tm_mday
def gettime():
        t=time.localtime(time.time()+3600*8)
        if(t.tm_mon<10):tm_mon='0'+str(t.tm_mon)
        else:tm_mon=str(t.tm_mon)
        if(t.tm_mday<10):tm_mday='0'+str(t.tm_mday)
        else:tm_mday=str(t.tm_mday)
        hour=t.tm_hour
        if(hour<10):tm_hour='0'+str(hour)
        else:tm_hour=str(hour)
        if(t.tm_min<10):tm_min='0'+str(t.tm_min)
        else:tm_min=str(t.tm_min)
        if(t.tm_sec<10):tm_sec='0'+str(t.tm_sec)
        else:tm_sec=str(t.tm_sec)
        return tm_mon+tm_mday+tm_hour+tm_min+tm_sec
#SendMail.SendMail("497425817@qq.com","test","qqq")
#time.sleep(200)
a=""
while len(a)==0:
	#a=os.popen("ifconfig").read()
	st,a=commands.getstatusoutput("sudo ifconfig")
	print a
	time.sleep(5)
i1=a.find("wlan0")
i2=a.find("Scope",i1)
b=a[i1:i2]
i1=b.find("223.3")
i2=b.find("211.65")
if(i1==-1 and i2==-1):
	time.sleep(1)
	if(open("halt.txt","r").read().find("1")!=-1):
		open("/home/pi/sniff/reboot.log","a").write("Reboot... at "+gettime()+" with content:"+a+" length:"+str(len(a))+"\n")
		print "Sleep 200s and reboot"
		time.sleep(200)
		os.system("sudo reboot")
