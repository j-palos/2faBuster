import subprocess
import shlex
import time


def captive():
    subprocess.run(shlex.split('airmon-ng check kill'))
    subprocess.run(shlex.split('killall network-manager wpa_supplicant dnsmasq'))
    subprocess.run(shlex.split('airmon-ng start wlan0'))
    apd = subprocess.Popen(shlex.split('hostapd ./hostapd.conf'))
    time.sleep(1)
    dnsmasq = subprocess.Popen(shlex.split('dnsmasq -C ./dnsmasq.conf -d'))
    subprocess.run(shlex.split('ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0'))
    subprocess.run(shlex.split('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1'))

    return apd, dnsmasq


if __name__ == '__main__':
    captive()

