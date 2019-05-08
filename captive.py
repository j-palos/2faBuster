import subprocess
import shlex
import time


captive_log = 'logs/captive.log'


def captive():
    with open(captive_log, 'a') as l:
        subprocess.run(shlex.split('airmon-ng check kill'), stdout=l, stderr=l)
        subprocess.run(shlex.split('killall network-manager wpa_supplicant dnsmasq'), stdout=l, stderr=l)
        subprocess.run(shlex.split('airmon-ng start wlan0'), stdout=l, stderr=l)
        apd = subprocess.Popen(shlex.split('hostapd ./hostapd.conf'), stdout=l, stderr=l)
        time.sleep(1)
        dnsmasq = subprocess.Popen(shlex.split('dnsmasq -C ./dnsmasq.conf -d'), stdout=l, stderr=l)
        subprocess.run(shlex.split('ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0'), stdout=l, stderr=l)
        subprocess.run(shlex.split('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1'), stdout=l, stderr=l)

    return apd, dnsmasq


if __name__ == '__main__':
    captive()

