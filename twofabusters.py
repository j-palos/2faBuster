import time
import subprocess
import shlex

from captive import captive


REDDIT = 'python3 reddit.py'

r = None
apd = None
dnsmasq = None


def stop():
    try:
        apd.kill()
    except AttributeError:
        pass

    try:
        dnsmasq.kill()
    except AttributeError:
        pass

    try:
        r.kill()
    except AttributeError:
        pass

def main():
    r = subprocess.Popen(shlex.split(REDDIT))
    time.sleep(1)

    try:
        apd, dnsmasq = captive()
        while True:
            r_dead = r.poll() is not None
            apd_dead = apd.poll() is not None
            dnsmasq_dead = dnsmasq.poll() is not None
            if r_dead or apd_dead or dnsmasq_dead:
                stop()
            time.sleep(1)
    except KeyboardInterrupt:
        stop()


if __name__ == '__main__':
    main()

