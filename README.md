# RaspberryPiLanSniffer
An arp sniffer project based on raspberry pi.

Config raspberry pi:
0. Make dir "/home/pi/sniff" and modify config.txt

1. Connect to seu-wlan
    sudo wpa_cli
    add_network
    set_network x ssid "seu-wlan"
    set_network x key_mgmt NONE
    enable_network 0
    save_config

2. Modify /etc/rc.local
    add command below before "exit 0"
    (sleep 15;cd /home/pi/sniff/;sudo python auto.py)&

3. Modify crontab:
    sudo crontab -e
    # m h  dom mon dow   command
    */15 * * * * cd /home/pi/sniff;python auto_detect.py
    */3 * * * * cd /home/pi/sniff;python sendip.py

4. Change time zone to Asia Shanghai
