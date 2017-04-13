# -*- coding: utf-8 -*-
import urllib2
import urllib
import commands
def SendIpToServer():
    MachineName="Jx"
    MachineSshPort=10001
    MachineIp="0.0.0.0"
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
        MachineIp=commands.getoutput("sudo ifconfig wlan0|grep \"inet addr\"|awk '{print $2}'| awk -F: '{print $2}'")
    except:
        pass
    try:
        postdata={"password":"456789","MachineName":MachineName,"MachineIp":MachineIp}
        req=urllib2.Request("http://223.3.80.188/ip",data=urllib.urlencode(postdata))
        ret=urllib2.urlopen(req).read()
        print ret
    except:
        pass
SendIpToServer()
