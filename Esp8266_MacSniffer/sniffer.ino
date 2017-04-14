#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <Ticker.h>
#define led 16
// External library files of Espressif SDK
extern "C" {
#include "user_interface.h"
#include "ets_sys.h"
#include "osapi.h"
#include "gpio.h"
#include "os_type.h"
#include "mem.h"
#include "user_config.h"
}

// Delay times
// Delay of loop function in milli seconds
# define __delay__ 10
// Delay of channel changing in seconds
# define __dlay_ChannelChange__ 0.1

typedef struct MacPair
{
  uint8_t mac1[6];
  uint8_t mac2[6];
  int8_t rssi;
  int8_t index[3];
  uint32_t time;
}MacPair;

typedef struct Payload
{
  MacPair item[1500];
}Payload;

typedef union{
  char timeByte[4];
  uint32_t timeValue;
}TimeElement;

uint32_t OnlineTimeOffset=0;
uint32_t RecordTime=0;
uint16_t itemIndex=0;
uint16_t maxItemIndex=1500;
Payload ToSend;
int isWork=5;



//Ticker for channel hopping
Ticker ts; 
// Function for printing the MAC address i of the MAC header
String dataToSend="";
char data;
String RawInput(String out);
void loginToSeuWlan();
void printMAC(uint8_t *buf, uint8 i)
{
  Serial.printf("\t%02X:%02X:%02X:%02X:%02X:%02X", buf[i+0], buf[i+1], buf[i+2], buf[i+3], buf[i+4], buf[i+5]);
}
// Promiscuous callback function: is executed whenever package is received by ESP 8266
void promisc_cb(uint8_t *buf, uint16_t len)
{
  int8_t rssi=buf[0];
  uint8_t *buffi=buf+12;
    if(isWork==4)//串口输入4   打印所有当前已经连接的connection mac
  {
    uint8_t *buffi=buf+12;
    if(len==60)
    {
      if(itemIndex<maxItemIndex)
      {
        char data=0;
        data=buffi[0];
        uint8 new_channel = wifi_get_channel()%12 + 1; 
        Serial.printf("ch:%d ",new_channel);
        printMAC(buffi, 4); // Print address 1
        printMAC(buffi,10); // Print address 2
        memcpy(&ToSend.item[itemIndex].mac1,&buffi[4],6);
        memcpy(&ToSend.item[itemIndex].mac2,&buffi[10],6);
        ToSend.item[itemIndex].rssi=rssi;
        ToSend.item[itemIndex].time=OnlineTimeOffset+millis()/1000-RecordTime;
        itemIndex++;
        Serial.printf(" rssi:%d\n",rssi);
      }
      else
      {
        isWork=5;
        Serial.printf("Fifo Full,turn to sending status\n");
      }
    }
  }
}

// Change the WiFi channel
void channelCh(void) 
{ 
  if(isWork==4)
  {
    // Change the channels by modulo operation
    uint8 new_channel = wifi_get_channel()%12 + 1; 
    //Serial.printf("** Hop to %d **\n", new_channel); 
    wifi_set_channel(new_channel); 
  }
} 


void setup_promisc()
{
  wifi_set_opmode(STATION_MODE);
  wifi_promiscuous_enable(0);
  wifi_set_promiscuous_rx_cb(promisc_cb);//注册混杂模式的接收函数promisc_cb，在数据包接收时被调用
  wifi_promiscuous_enable(1);
  Serial.printf("Promisc mode\n");
  ts.attach(__dlay_ChannelChange__, channelCh);   
}

void setup() {
  Serial.begin(250000);
  pinMode(led,OUTPUT);
  digitalWrite(led,1);
  delay(1000);
  isWork=6;
}

void loop() {
  if(isWork==5||isWork==6)//从串口输入e来触发执行一些事情
  {
    wifi_set_opmode(STATION_MODE);
    wifi_promiscuous_enable(0);
    if(WiFi.isConnected())
    {
      Serial.print("Already connected!  ");
      Serial.println(WiFi.localIP()); 
      delay(10);
    }
    else
    {
       WiFi.begin("seu-wlan");    //连接seuwlan
       Serial.print("Connecting to wifi seu-wlan");
      while (WiFi.status() != WL_CONNECTED)
        {
          delay(500);
          Serial.print(".");
        }
       Serial.print("Connected, IP address: ");
       Serial.println(WiFi.localIP()); 
    }

    WiFiClient client1;
    if (client1.connect("223.3.78.79", 7777))
    {
        Serial.println("Connected！");
        client1.print("flagN");
        while(client1.available()==0);
        while(client1.available()!=0)
        client1.read();

        client1.print("seuwlan12");
        while(client1.available()==0);
        while(client1.available()!=0)
        client1.read();

        TimeElement webTime;
        client1.print("flagT");
        while(client1.available()==0);
        webTime.timeByte[0]=client1.read();
        webTime.timeByte[1]=client1.read();
        webTime.timeByte[2]=client1.read();
        webTime.timeByte[3]=client1.read();
        OnlineTimeOffset=webTime.timeValue;
        RecordTime=millis()/1000;
     if(isWork==5)
     {
       String tmp;
       for(int j=0;j<maxItemIndex;j++)
       {
         char *dataPtr=(char *)(&ToSend.item[j]);
         tmp="";
         for(int i=0;i<20;i++)
         {
          tmp+=dataPtr[i];
         }
         client1.print(tmp);
       }
     }
       Serial.println("Communication End");
    }
    else
    {
      Serial.println("Connection failed");
    }
    isWork=4;
    setup_promisc();
    itemIndex=0;
  }
  if(Serial.available()!=0)
  {
    data=Serial.read();
    if(data=='4')
    {
      setup_promisc();
      isWork=4;
     }
    else if(data=='e')
      isWork=5;
    else
      isWork=3;
  }
}
