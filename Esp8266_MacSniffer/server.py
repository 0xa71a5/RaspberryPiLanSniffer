from socket import *
import binascii
import thread
import struct
import time
frameCount=0
def connectionHandler(conn,addr):
    global frameCount
    try:
        payloadLength=0
        stationName="test.txt"
        f=open(stationName,"a")
        while True:
            content=conn.recv(1000)
            if(len(content)==0):break
            #print "len",len(content)
            if(content[:4]=="flag"):
                flag=content[4]
                if(flag=='L'):#payload size
                    conn.sendall("ok")
                    content=conn.recv(1000)
                    payloadLength,=struct.unpack("<I",content)
                    print "PayloadLength:",payloadLength
                    conn.sendall("ok")
                elif(flag=='N'):#station node name
                    conn.sendall("ok")
                    content=conn.recv(1000)
                    stationName=content
                    print "Station Name:",stationName
                    f.close()
                    f=open(stationName+".txt","a")
                    conn.sendall("ok")
                elif(flag=='T'):#query for time
                    timeInt4=int(time.time())
                    toSendTimeValue=struct.pack("<I",timeInt4)
                    conn.sendall(toSendTimeValue)
                    print "Send out time"
            else:
                #print addr,">>>",binascii.b2a_hex(content)
                writeLoops=len(content)/20
                for x in range(0,writeLoops):
                    partContent=content[x*20:x*20+20]
                    itemMac1,itemMac2,rssi,useless,recvtime=struct.unpack("<6s6sb3sI",partContent)
                    mac1=binascii.b2a_hex(itemMac1)
                    mac2=binascii.b2a_hex(itemMac2)
                    parMac1=mac1[0:2]+":"+mac1[2:4]+":"+mac1[4:6]+":"+mac1[6:8]+":"+mac1[8:10]+":"+mac1[10:12]
                    parMac2=mac2[0:2]+":"+mac2[2:4]+":"+mac2[4:6]+":"+mac2[6:8]+":"+mac2[8:10]+":"+mac2[10:12]
                    recvtime=time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(recvtime))
                    print frameCount,parMac1,parMac2,rssi,recvtime
                    f.write(parMac1+","+parMac2+","+str(rssi)+","+str(recvtime)+"\n")
                    f.flush()
                    frameCount=frameCount+1
        conn.close()
        f.close()
    except Exception as e:
        print e
s=socket()
s.bind(("223.3.78.79",7777))
s.listen(100)
print "Begin!"
while True:
    con,addr=s.accept()
    thread.start_new_thread(connectionHandler,(con,addr))
    print "New connnection from",addr
