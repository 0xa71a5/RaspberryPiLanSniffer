import os
import time
import SendMail
MachineName="J1"
MachineSshPort=10008
MachineOuterEnable=False
stationCount=0
try:
	f=open("config.txt","r")
	dic={}
	for x in f.readlines():
		if(len(x)>5):
			x=x[:-1]
			x=x.split(":")
			dic[x[0]]=x[1]
	MachineName=dic["MachineName"]
	MachineSshPort=dic["MachineSshPort"]
	if(dic["MachineOuterEnable"]=='0'):MachineOuterEnable=False
	else:MachineOuterEnable=True
except:
	pass

def getdate():
    t=time.localtime(time.time())
    if(t.tm_mon<10):tm_mon='0'+str(t.tm_mon)
    else:tm_mon=str(t.tm_mon)
    if(t.tm_mday<10):tm_mday='0'+str(t.tm_mday)
    else:tm_mday=str(t.tm_mday)
    return str(t.tm_year)+tm_mon+tm_mday
def gettime():
        t=time.localtime(time.time())
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


def scan(ip_range):
    global stationCount
    global specialTask
    outFile=open(getdate()+".txt","a")
    p=os.popen("arp-scan --interface=wlan0 -i 10 "+ip_range).read()
    words=p.split("\n")
    ret=""
    for x in words[2:-4]:
        if(len(x)==0):continue
        item=x.split("\t")
        if(len(item)!=3):continue
        ip_addr=item[0]
        mac_addr=item[1]
        if(mac_addr[:8]=="ac:4b:c8"):continue
        curtime=gettime()
        stationCount+=1
        print ip_addr,mac_addr,curtime
        toWrite=ip_addr+"\t"+mac_addr+"\t"+curtime+"\n"
        outFile.write(toWrite)
    outFile.close()

ipaddr=""
while True:
    a=os.popen("sudo ifconfig").read()
    i1=a.find("wlan0")
    i2=a.find("Scope",i1)
    b=a[i1:i2]
    i1=b.find("223.3")
    i3=b.find("211.")
    if(i1==-1 and i3==-1):
        print "Wait until connecting to seuwlan"
        time.sleep(1)
    else:
        i2=b.find(" ",i1)
        ipaddr=b[i1:i2]
        print "ip addr:",ipaddr
        break
os.system("sudo nohup python simpleServer.py &")
startPoint=True
stationAmountFile=open("stationAmount.txt","a")
while  True:
    stationCount=0
    for x in range(96,128):
            begin="223.3."+str(x)+".1"
            end="223.3."+str(x)+".255"
            scan(begin+"-"+end)
    for x in range(152,160):
            begin="223.3."+str(x)+".1"
            end="223.3."+str(x)+".255"
            scan(begin+"-"+end)
    for x in range(36,40):
            begin="211.65."+str(x)+".1"
            end="211.65."+str(x)+".255"
            scan(begin+"-"+end)
    t=gettime()
    stationAmountFile.write(MachineName+",2017"+str(t)+","+str(stationCount)+"\n")
    stationAmountFile.flush()
