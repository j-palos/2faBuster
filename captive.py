#!/usr/bin/python

import os
import sys

def writeCaptivePortal():
    f = open("/etc/nginx/sites-enabled/captive_portal","w")
    f.write("server{\n")
    f.write("    listen 80;\n")
    f.write("    root /var/www/captive_portal;\n")
    f.write("    location / {\n")
    f.write("        if (!-f $request_filename){\n")
    f.write("            return 302 $scheme://192.168.1.1/index.html;\n")
    f.write("        }\n")
    f.write("    }\n")
    f.write("}\n")
    f.close()

os.system("cp -r templates/* /var/www/captive_portal")
os.system('airmon-ng check kill')
os.system('airmon-ng start wlan0')
os.system('rm /tmp/hostapd.conf')
writehostapd()
os.system('hostapd /var/www/captive_portal/hostapd.conf &')
os.system('rm /tmp/dnsmasq.conf')
writeDnsmasq()
os.system('dnsmasq -C /var/www/captive_portal/dnsmasq.conf -d')
os.system('ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0')
os.system('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1')
os.system('mkdir /var/www/captive_portal')
os.system('rm /etc/nginx/sites-enabled/*')
writeCaptivePortal()
os.system('service nginx reload')
os.system('service nginx restart')
