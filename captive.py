#!/usr/bin/python

import os
import sys

os.system("cp -r templates/* /var/www/captive_portal")
os.system('airmon-ng check kill')
os.system('airmon-ng start wlan0')
os.system('hostapd /var/www/captive_portal/hostapd.conf &')
os.system('dnsmasq -C /var/www/captive_portal/dnsmasq.conf -d')
os.system('ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0')
os.system('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1')
